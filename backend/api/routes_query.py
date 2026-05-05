"""
API Routes — RAG Query Endpoints
Handles question answering with conflict detection.
"""
import os
import time
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(tags=["Query"])


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, description="The question to ask")
    api_key: str | None = Field(None, description="Google Gemini API key (optional if already set)")


class ApiKeyRequest(BaseModel):
    api_key: str = Field(..., min_length=10, description="Google Gemini API key")


DEMO_QUERIES = [
    {
        "question": "How has patient satisfaction changed over Q1?",
        "description": "Compares satisfaction surveys against complaint logs",
        "expected_conflicts": True,
    },
    {
        "question": "What is the state of surgical outcomes this quarter?",
        "description": "Examines surgical success rates vs complication reports",
        "expected_conflicts": True,
    },
    {
        "question": "Is staff morale improving or declining?",
        "description": "Analyzes nursing reports against turnover data",
        "expected_conflicts": True,
    },
    {
        "question": "What is the hospital's financial health in Q1?",
        "description": "Revenue growth vs budget overruns analysis",
        "expected_conflicts": True,
    },
    {
        "question": "Are infection rates increasing or decreasing?",
        "description": "Infection control quarterly report analysis",
        "expected_conflicts": False,
    },
    {
        "question": "What did the board discuss in the March meeting?",
        "description": "Board meeting minutes review",
        "expected_conflicts": False,
    },
]


@router.post("/query")
async def run_query(request: QueryRequest):
    """Run a RAG query with conflict detection."""
    from backend.main import app_state

    if not app_state["vector_store"]:
        raise HTTPException(status_code=503, detail="Vector store not initialized. Please wait for startup.")

    # Determine API key
    api_key = request.api_key or app_state.get("api_key")
    if not api_key:
        raise HTTPException(status_code=400, detail="No API key provided. Set one via /api/set-api-key or include in request.")

    # Set env var for langchain
    os.environ["GOOGLE_API_KEY"] = api_key

    # Build or reuse chain
    from backend.config import LLM_MODEL
    if app_state.get("chain") is None or app_state.get("chain_model") != LLM_MODEL:
        from backend.rag_pipeline import build_chain
        try:
            app_state["chain"] = build_chain(api_key)
            app_state["chain_model"] = LLM_MODEL
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to build LLM chain: {str(e)}")

    # Execute query
    start_time = time.time()
    try:
        from backend.rag_pipeline import query_with_conflict_detection
        result = query_with_conflict_detection(
            chain=app_state["chain"],
            vector_store=app_state["vector_store"],
            question=request.question,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

    elapsed = round(time.time() - start_time, 2)

    # Store in history
    history_entry = {
        "question": request.question,
        "timestamp": datetime.now().isoformat(),
        "elapsed_seconds": elapsed,
        "confidence": result["confidence"],
        "conflict_count": result["conflicts"]["conflict_count"],
        "source_count": len(result["sources"]),
    }
    app_state["query_history"].insert(0, history_entry)
    # Keep only last 50
    app_state["query_history"] = app_state["query_history"][:50]

    result["elapsed_seconds"] = elapsed
    return result


@router.post("/set-api-key")
async def set_api_key(request: ApiKeyRequest):
    """Store the Gemini API key for subsequent requests."""
    from backend.main import app_state
    app_state["api_key"] = request.api_key
    os.environ["GOOGLE_API_KEY"] = request.api_key

    # Rebuild chain with new key
    app_state["chain"] = None

    return {"status": "ok", "message": "API key set successfully"}


@router.get("/api-key-status")
async def api_key_status():
    """Check if an API key is set."""
    from backend.main import app_state
    return {"is_set": app_state.get("api_key") is not None}


@router.get("/demo-queries")
async def get_demo_queries():
    """Return list of demo queries."""
    return {"queries": DEMO_QUERIES}
