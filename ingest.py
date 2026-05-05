"""
ingest.py — Document Ingestion Pipeline

Loads PDFs and TXT hospital reports, splits them into 800-character
chunks with 200-character overlap, embeds each chunk using
all-MiniLM-L6-v2, and stores the result in ChromaDB with SHA-256
deduplication (upsert semantics — safe to re-run on an existing DB).

Documents are stored in the ./documents/ directory.
ChromaDB is persisted to ./chroma_db/
"""
import os
import hashlib
import sys
import io

# Fix Windows console encoding
if sys.stdout and hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

import fitz  # PyMuPDF
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ── Configuration (mirrors config.py constants) ──────────────────────
BASE_DIR         = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR    = os.path.join(BASE_DIR, "documents")
CHROMA_PERSIST   = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME  = "hospital_docs"
CHUNK_SIZE       = 800
CHUNK_OVERLAP    = 200
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"


# ── Helpers ────────────────────────────────────────────────────────────

def extract_text(filepath: str) -> str:
    """Extract raw text from a PDF or plain-text file."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        pages = []
        doc = fitz.open(filepath)
        for page in doc:
            pages.append(page.get_text())
        doc.close()
        return "\n".join(pages)
    else:  # .txt and fallback
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()


# ── Core ingestion function ────────────────────────────────────────────

def ingest_documents(directory: str = None):
    """
    Full ingestion pipeline: load → chunk → embed → store.

    Args:
        directory: Path to directory containing hospital documents.
                   Defaults to ./documents/

    Returns:
        chromadb.Collection — the populated ChromaDB collection.
    """
    if directory is None:
        directory = DOCUMENTS_DIR

    print(f"[INGEST] Loading documents from: {directory}")
    print("=" * 50)

    # Embedding model
    embed_model = SentenceTransformer(EMBEDDING_MODEL)

    # Text splitter — 800-char chunks, 200-char overlap
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    # ChromaDB client — persisted to disk
    client = chromadb.PersistentClient(path=CHROMA_PERSIST)
    col = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    total_chunks = 0
    supported = {".pdf", ".txt"}

    for fname in sorted(os.listdir(directory)):
        fpath = os.path.join(directory, fname)
        ext   = os.path.splitext(fname)[1].lower()
        if ext not in supported:
            continue

        print(f"  [LOAD] {fname}")
        text   = extract_text(fpath)
        chunks = splitter.split_text(text)

        for i, chunk_text in enumerate(chunks):
            # SHA-256 hash used as the chunk ID — guarantees deduplication
            cid = hashlib.sha256(chunk_text.encode()).hexdigest()[:16]
            emb = embed_model.encode(chunk_text).tolist()

            # upsert is idempotent — safe to re-run on existing collection
            col.upsert(
                ids=[cid],
                embeddings=[emb],
                documents=[chunk_text],
                metadatas=[{"source": fname, "chunk_index": i}],
            )
            total_chunks += 1

    print(f"\n  [OK] Total chunks stored: {total_chunks}")
    print(f"  [OK] ChromaDB persisted to: {CHROMA_PERSIST}")
    return col


def load_collection():
    """Load an existing ChromaDB collection (no re-ingestion)."""
    client = chromadb.PersistentClient(path=CHROMA_PERSIST)
    return client.get_collection(name=COLLECTION_NAME)


if __name__ == "__main__":
    col = ingest_documents()
    print(f"\n[VERIFY] Collection '{COLLECTION_NAME}' — {col.count()} total documents")
    print("  [OK] Ingestion complete!")
