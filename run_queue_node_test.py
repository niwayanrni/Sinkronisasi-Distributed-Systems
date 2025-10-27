import asyncio
from aiohttp import web, ClientSession
import redis.asyncio as aioredis
import json
from hashlib import sha256

REDIS_QUEUE_PREFIX = "distributed_queue:"

class QueueNode:
    def __init__(self, node_id, redis_url="redis://localhost"):
        self.node_id = node_id
        self.redis = None
        self.redis_url = redis_url

    async def connect_redis(self):
        self.redis = await aioredis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
        print(f"[{self.node_id}] Connected to Redis")

    def get_queue_name(self):
        return REDIS_QUEUE_PREFIX + self.node_id

    async def enqueue(self, message):
        queue_name = self.get_queue_name()
        await self.redis.rpush(queue_name, json.dumps(message))
        print(f"[{self.node_id}] Enqueued: {message}")

    async def dequeue(self):
        queue_name = self.get_queue_name()
        msg = await self.redis.lpop(queue_name)
        if msg:
            data = json.loads(msg)
            print(f"[{self.node_id}] Dequeued: {data}")
            return data
        else:
            print(f"[{self.node_id}] Queue empty")
            return None

    async def handle_enqueue(self, request):
        data = await request.json()
        await self.enqueue(data)
        return web.json_response({"status": "ok"})

    async def handle_dequeue(self, request):
        msg = await self.dequeue()
        return web.json_response({"message": msg})

    def get_app(self):
        app = web.Application()
        app.router.add_post("/enqueue", self.handle_enqueue)
        app.router.add_get("/dequeue", self.handle_dequeue)
        return app

async def test_node():
    node = QueueNode("node1")
    await node.connect_redis()
    await node.enqueue({"task": "hello"})
    await node.dequeue()

async def main():
    node = QueueNode("node1")
    await node.connect_redis()
    app = node.get_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8000)
    await site.start()
    print("[node1] HTTP server running on http://localhost:8000")

    await test_node()

    while True:
        await asyncio.sleep(3600)

asyncio.run(main())
