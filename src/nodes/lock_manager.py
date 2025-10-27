from fastapi import FastAPI
from src.utils.metrics import Metrics

app = FastAPI(
    title="Distributed Lock Manager API",
    version="1.0.0",
    description="Implements Raft-based distributed lock system"
)

metrics = Metrics()
locks = {}

@app.post("/lock/acquire")
def acquire_lock(resource_id: str, mode: str = "exclusive"):
    if resource_id in locks:
        metrics.record("errors")
        return {"status": "locked", "resource": resource_id}

    locks[resource_id] = mode
    metrics.record("requests")
    return {"status": "acquired", "resource": resource_id, "mode": mode}

@app.post("/lock/release")
def release_lock(resource_id: str):
    if resource_id in locks:
        del locks[resource_id]
        metrics.record("requests")
        return {"status": "released", "resource": resource_id}

    metrics.record("errors")
    return {"status": "not_found"}

@app.get("/lock/status")
def get_locks():
    return {"active_locks": locks}

@app.get("/lock/metrics")
def get_metrics():
    return metrics.data
