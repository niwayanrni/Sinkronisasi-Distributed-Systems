from fastapi import FastAPI
from fastapi import APIRouter
from src.utils.metrics import Metrics

app = FastAPI(
    title="Distributed Cache Node API",
    version="1.0.0",
    description="API untuk Cache Node"
)

router = APIRouter()
metrics = Metrics()

cache_store = {}

@router.post("/set")
def set_cache(key: str, value: str):
    cache_store[key] = value
    metrics.record("requests")
    return {"status": "ok", "key": key, "value": value}

@router.get("/get")
def get_cache(key: str):
    if key in cache_store:
        metrics.record("requests")
        return {"status": "ok", "key": key, "value": cache_store[key]}
    metrics.record("errors")
    return {"status": "not found", "key": key}

@router.get("/status")
def cache_status():
    return {"cache": cache_store}

@router.get("/metrics")
def cache_metrics():
    return metrics.data


app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.nodes.cache_node:app", host="0.0.0.0", port=8083, reload=True)
