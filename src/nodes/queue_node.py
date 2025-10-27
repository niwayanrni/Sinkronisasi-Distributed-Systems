from fastapi import FastAPI
from fastapi import APIRouter
from src.utils.metrics import Metrics
import hashlib

app = FastAPI(
    title="Distributed Queue Node API",
    version="1.0.0",
    description="API untuk Distributed Queue Node"
)

router = APIRouter()
metrics = Metrics()

# Simulasi hash ring sederhana untuk konsistensi
hash_ring = {}
queues = {}

def get_node_for_key(key: str):
    hashed = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    node = hashed % 3  # 3 nodes misalnya
    return f"node-{node}"

@router.post("/enqueue")
def enqueue(key: str, message: dict):
    node = get_node_for_key(key)
    if node not in queues:
        queues[node] = []
    queues[node].append(message)
    metrics.record("requests")
    return {"status": "enqueued", "node": node, "message": message}

@router.get("/dequeue")
def dequeue(node: str):
    if node in queues and queues[node]:
        msg = queues[node].pop(0)
        metrics.record("requests")
        return {"status": "dequeued", "message": msg}
    metrics.record("errors")
    return {"status": "empty", "node": node}

@router.get("/status")
def queue_status():
    return {"queues": queues}

@router.get("/metrics")
def queue_metrics():
    return metrics.data

# Daftarkan router ke app
app.include_router(router)

# Jalankan langsung jika file dijalankan secara manual
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.nodes.queue_node:app", host="0.0.0.0", port=8082, reload=True)
