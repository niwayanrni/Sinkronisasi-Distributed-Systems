import yaml
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html

try:
    from src.nodes.lock_manager import lock_router
    print("✅ lock_manager imported")
except Exception as e:
    print("❌ lock_manager import failed:", e)

try:
    from src.nodes.queue_node import queue_router
    print("✅ queue_node imported")
except Exception as e:
    print("❌ queue_node import failed:", e)

try:
    from src.nodes.cache_node import cache_router
    print("✅ cache_node imported")
except Exception as e:
    print("❌ cache_node import failed:", e)


app = FastAPI(
    title="Distributed Sync System API",
    version="1.0.0",
    description="""
    Sistem Sinkronisasi Terdistribusi yang mensimulasikan komponen:
    - **Distributed Lock Manager** (Raft-based)
    - **Distributed Queue System** (Consistent Hashing)
    - **Distributed Cache Coherence** (MESI/MOESI)
    """
)


try:
    with open("docs/api_spec.yaml", "r") as f:
        openapi_yaml = yaml.safe_load(f)

    def custom_openapi():
        return openapi_yaml

    app.openapi = custom_openapi
except FileNotFoundError:
    pass

app.include_router(lock_router, prefix="/lock", tags=["Distributed Lock Manager"])
app.include_router(queue_router, prefix="/queue", tags=["Distributed Queue System"])
app.include_router(cache_router, prefix="/cache", tags=["Distributed Cache Coherence"])


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/docs", include_in_schema=False)
async def swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Distributed Sync System API Docs",
    )
