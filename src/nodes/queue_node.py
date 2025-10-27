import asyncio
import aioredis
import json
from hashlib import sha256
from aiohttp import web
from src.utils.metrics import increment_metric

REDIS_QUEUE_PREFIX = "distributed_queue:"

class QueueNode:
    def __init__(self, node_id, peers=None, redis_url="redis://localhost"):
        self.node_id = node_id
        self.peers = peers or []
        self.redis = None
        self.redis_url = redis_url

    async def connect_redis(self):
        self.redis = await aioredis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)

    def get_node_for_key(self, key):
        hash_val = int(sha256(key.encode()).hexdigest(), 16)
        all_nodes = sorted(self.peers + [self.node_id])
        idx = hash_val % len(all_nodes)
        return all_nodes[idx]

    async def enqueue(self, key, message):
        target_node = self.get_node_for_key(key)
        if target_node != self.node_id:
            # Forward to responsible node via HTTP
            async with aiohttp.ClientSession() as session:
                url = f"http://{target_node}/enqueue"
                await session.post(url, json={"key": key, "message": message})
        else:
            # Store in Redis
            queue_name = REDIS_QUEUE_PREFIX + self.node_id
            await self.redis.rpush(queue_name, json.dumps(message))
            increment_metric("messages_enqueued")

    async def dequeue(self):
        queue_name = REDIS_QUEUE_PREFIX + self.node_id
        msg = await self.redis.lpop(queue_name)
        if msg:
            increment_metric("messages_dequeued")
            return json.loads(msg)
        return None

    # --- aiohttp server handlers ---
    async def handle_enqueue(self, request):
        data = await request.json()
        key = data["key"]
        message = data["message"]
        await self.enqueue(key, message)
        return web.json_response({"status": "ok"})

    async def handle_dequeue(self, request):
        msg = await self.dequeue()
        return web.json_response({"message": msg})

    def get_app(self):
        app = web.Application()
        app.router.add_post("/enqueue", self.handle_enqueue)
        app.router.add_get("/dequeue", self.handle_dequeue)
        return app
