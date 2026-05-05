"""
API Routes — Document Management Endpoints
Handles document listing, content viewing, and re-ingestion.
"""
import os
from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Documents"])


@router.get("/documents")
async def list_documents():
    """List all documents in the sample_documents directory with metadata."""
    from backend.config import SAMPLE_DOCS_DIR, SUPPORTED_EXTENSIONS
    from backend.ingestion import extract_department

    if not os.path.exists(SAMPLE_DOCS_DIR):
        return {"documents": [], "total": 0}

    documents = []
    for filename in sorted(os.listdir(SAMPLE_DOCS_DIR)):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            continue

        filepath = os.path.join(SAMPLE_DOCS_DIR, filename)
        file_size = os.path.getsize(filepath)

        # Read first 500 chars for department detection
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                preview = f.read(500)
        except Exception:
            preview = ""

        department = extract_department(filename, preview)

        documents.append({
            "filename": filename,
            "doc_id": os.path.splitext(filename)[0],
            "department": department,
            "doc_type": ext.replace(".", "").upper(),
            "file_size": file_size,
            "file_size_display": f"{file_size / 1024:.1f} KB",
        })

    return {"documents": documents, "total": len(documents)}


@router.get("/documents/{doc_id}")
async def get_document(doc_id: str):
    """Get full content of a specific document."""
    from backend.config import SAMPLE_DOCS_DIR, SUPPORTED_EXTENSIONS

    # Try to find the file with any supported extension
    for ext in SUPPORTED_EXTENSIONS:
        filename = f"{doc_id}{ext}"
        filepath = os.path.join(SAMPLE_DOCS_DIR, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                return {
                    "doc_id": doc_id,
                    "filename": filename,
                    "content": content,
                    "length": len(content),
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error reading document: {str(e)}")

    raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found")


@router.post("/documents/reingest")
async def reingest_documents():
    """Re-ingest all documents from the sample_documents folder."""
    from backend.main import app_state
    from backend.ingestion import ingest_documents

    try:
        app_state["vector_store"] = ingest_documents()
        if app_state["vector_store"]:
            # Reset chain since vector store changed
            app_state["chain"] = None
            count = app_state["vector_store"]._collection.count()
            return {"status": "ok", "message": f"Re-ingested successfully. {count} chunks indexed."}
        else:
            raise HTTPException(status_code=500, detail="Ingestion returned no vector store")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Re-ingestion failed: {str(e)}")


@router.get("/documents/stats/overview")
async def document_stats():
    """Get document and chunk statistics."""
    from backend.main import app_state
    from backend.config import SAMPLE_DOCS_DIR, SUPPORTED_EXTENSIONS

    stats = {
        "total_documents": 0,
        "total_chunks": 0,
        "departments": {},
        "doc_types": {},
    }

    # Count source files
    if os.path.exists(SAMPLE_DOCS_DIR):
        for filename in os.listdir(SAMPLE_DOCS_DIR):
            ext = os.path.splitext(filename)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                stats["total_documents"] += 1
                doc_type = ext.replace(".", "").upper()
                stats["doc_types"][doc_type] = stats["doc_types"].get(doc_type, 0) + 1

    # Count chunks from vector store
    if app_state["vector_store"]:
        try:
            collection = app_state["vector_store"]._collection
            stats["total_chunks"] = collection.count()

            # Get department distribution from metadata
            all_data = collection.get(include=["metadatas"])
            if all_data and all_data.get("metadatas"):
                for meta in all_data["metadatas"]:
                    dept = meta.get("department", "Unknown")
                    stats["departments"][dept] = stats["departments"].get(dept, 0) + 1
        except Exception:
            pass

    return stats
