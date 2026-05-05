"""
Hospital Management System — FastAPI Backend
Serves the RAG Conflict Detection API and hosts the frontend.
"""
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Ensure the project root is in the path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.api.routes_query import router as query_router
from backend.api.routes_documents import router as documents_router
from backend.api.routes_analytics import router as analytics_router

# Shared state for the app
app_state = {
    "vector_store": None,
    "chain": None,
    "api_key": None,
    "query_history": [],
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize vector store on startup."""
    print("[STARTUP] Initializing Hospital Management System...")
    from backend.config import CHROMA_PERSIST_DIR, SAMPLE_DOCS_DIR
    chroma_path = Path(CHROMA_PERSIST_DIR)

    if chroma_path.exists() and any(chroma_path.iterdir()):
        print("[STARTUP] Loading existing vector store...")
        from backend.ingestion import load_vector_store
        app_state["vector_store"] = load_vector_store()
        print("[STARTUP] Vector store loaded.")
    else:
        print("[STARTUP] No existing vector store found. Ingesting documents...")
        from backend.ingestion import ingest_documents
        app_state["vector_store"] = ingest_documents()
        if app_state["vector_store"]:
            print("[STARTUP] Documents ingested successfully.")
        else:
            print("[STARTUP] WARNING: Failed to ingest documents.")

    yield

    print("[SHUTDOWN] Shutting down...")


app = FastAPI(
    title="Hospital Management System",
    description="RAG-powered hospital document analysis with conflict detection",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(query_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")

# Serve frontend static files
frontend_dir = os.path.join(PROJECT_ROOT, "frontend")


@app.get("/")
async def serve_frontend():
    """Serve the frontend SPA."""
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Hospital Management System API", "docs": "/docs"}


# Mount static files AFTER explicit routes so they don't shadow them
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


from pydantic import BaseModel
class KeyPayload(BaseModel):
    api_key: str

@app.post("/api/config/key")
async def set_api_key(payload: KeyPayload):
    """Accept Gemini API key from the frontend."""
    app_state["api_key"] = payload.api_key
    os.environ["GOOGLE_API_KEY"] = payload.api_key
    app_state["chain"] = None  # rebuild on next query
    return {"status": "ok"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    has_store = app_state["vector_store"] is not None
    return {
        "status": "healthy" if has_store else "degraded",
        "vector_store": "loaded" if has_store else "not_loaded",
        "api_key_set": app_state["api_key"] is not None,
    }
