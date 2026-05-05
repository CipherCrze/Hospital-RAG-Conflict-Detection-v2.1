"""
API Routes — Analytics & Metrics Endpoints
Provides dashboard data, department breakdowns, and query history.
"""
from fastapi import APIRouter

router = APIRouter(tags=["Analytics"])


@router.get("/analytics/overview")
async def analytics_overview():
    """Get high-level analytics for the dashboard."""
    from backend.main import app_state
    from backend.config import SAMPLE_DOCS_DIR
    import os

    overview = {
        "total_documents": 0,
        "total_chunks": 0,
        "total_queries": len(app_state.get("query_history", [])),
        "total_conflicts_detected": 0,
        "avg_confidence": 0,
        "system_status": "operational",
        "vector_store_loaded": app_state["vector_store"] is not None,
        "api_key_set": app_state.get("api_key") is not None,
    }

    # Count docs
    if os.path.exists(SAMPLE_DOCS_DIR):
        from backend.config import SUPPORTED_EXTENSIONS
        for f in os.listdir(SAMPLE_DOCS_DIR):
            if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS:
                overview["total_documents"] += 1

    # Count chunks
    if app_state["vector_store"]:
        try:
            overview["total_chunks"] = app_state["vector_store"]._collection.count()
        except Exception:
            pass

    # Aggregate from query history
    history = app_state.get("query_history", [])
    if history:
        overview["total_conflicts_detected"] = sum(h.get("conflict_count", 0) for h in history)
        scores = [h["confidence"]["score"] for h in history if "confidence" in h]
        if scores:
            overview["avg_confidence"] = round(sum(scores) / len(scores), 1)

    return overview


@router.get("/analytics/departments")
async def department_analytics():
    """Get department-level analytics."""
    from backend.main import app_state

    departments = {}

    if app_state["vector_store"]:
        try:
            collection = app_state["vector_store"]._collection
            all_data = collection.get(include=["metadatas"])

            if all_data and all_data.get("metadatas"):
                for meta in all_data["metadatas"]:
                    dept = meta.get("department", "Unknown")
                    source = meta.get("source", "Unknown")

                    if dept not in departments:
                        departments[dept] = {
                            "department": dept,
                            "chunk_count": 0,
                            "documents": set(),
                        }
                    departments[dept]["chunk_count"] += 1
                    departments[dept]["documents"].add(source)

        except Exception:
            pass

    # Convert sets to lists for JSON serialization
    result = []
    for dept_data in departments.values():
        dept_data["documents"] = list(dept_data["documents"])
        dept_data["document_count"] = len(dept_data["documents"])
        result.append(dept_data)

    # Sort by chunk count descending
    result.sort(key=lambda x: x["chunk_count"], reverse=True)

    return {"departments": result}


@router.get("/analytics/query-history")
async def query_history():
    """Get recent query history."""
    from backend.main import app_state
    return {
        "history": app_state.get("query_history", []),
        "total": len(app_state.get("query_history", [])),
    }
