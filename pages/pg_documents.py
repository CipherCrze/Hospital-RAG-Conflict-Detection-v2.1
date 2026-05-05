"""Documents page with upload, indexing, and resolution guidance."""
from __future__ import annotations

import html
import os
import re
from pathlib import Path

import streamlit as st

from config import CHUNK_SIZE, SAMPLE_DOCS_DIR, SUPPORTED_EXTENSIONS


def _safe_filename(name: str) -> str:
    stem = Path(name).stem.strip() or "document"
    suffix = Path(name).suffix.lower()
    safe_stem = re.sub(r"[^A-Za-z0-9._ -]+", "_", stem).strip(" ._-")
    safe_stem = safe_stem or "document"
    return f"{safe_stem[:90]}{suffix}"


def _file_preview(path: Path) -> str:
    try:
        if path.suffix.lower() == ".txt":
            return path.read_text(encoding="utf-8", errors="ignore")[:600]
        from ingestion import load_document

        pages = load_document(str(path))
        return "\n".join(page["text"] for page in pages)[:600]
    except Exception:
        return ""


def _document_rows(docs_dir: Path) -> list[dict]:
    from ingestion import extract_department

    rows = []
    for path in sorted(docs_dir.iterdir(), key=lambda p: p.name.lower()):
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        preview = _file_preview(path)
        size = path.stat().st_size
        rows.append(
            {
                "name": path.name,
                "department": extract_department(path.name, preview),
                "type": path.suffix.replace(".", "").upper(),
                "size": f"{size / 1024:.1f} KB",
                "chunks": max(1, (len(preview) or size) // max(CHUNK_SIZE, 1) + 1),
            }
        )
    return rows


def _save_uploads(uploaded_files, docs_dir: Path) -> list[str]:
    saved = []
    for uploaded_file in uploaded_files:
        filename = _safe_filename(uploaded_file.name)
        if Path(filename).suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        target = docs_dir / filename
        target.write_bytes(uploaded_file.getbuffer())
        saved.append(filename)
    return saved


def _render_guidance(rows: list[dict], has_api_key: bool):
    indexed_count = len(rows)
    dept_count = len({row["department"] for row in rows})

    suggestions = [
        "Name uploads with department, quarter, and source system so conflicts are easier to trace.",
        "Re-index immediately after upload before running new queries.",
        "When two reports disagree, compare reporting period, denominator, and owning department first.",
    ]
    if not has_api_key:
        suggestions.insert(0, "Add a Gemini API key before running conflict-aware analysis.")
    if indexed_count == 0:
        suggestions.insert(0, "Upload at least one PDF, DOCX, or TXT file to build the knowledge base.")
    elif dept_count < 3:
        suggestions.append("Add documents from more departments to improve cross-source conflict detection.")

    cards = "".join(
        f"""
        <div class="tip-card">
          <div class="tip-index">{i}</div>
          <div>{html.escape(text)}</div>
        </div>
        """
        for i, text in enumerate(suggestions[:5], 1)
    )

    st.markdown(
        f"""
        <div class="content-panel tips-panel">
          <div class="panel-header">
            <span class="panel-title">Resolution Tips</span>
            <span class="panel-meta">{indexed_count} indexed files</span>
          </div>
          <div class="tips-list">{cards}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="content-panel suggestion-panel">
          <div class="panel-header"><span class="panel-title">Suggested Follow-up Queries</span></div>
          <div class="suggestion-list">
            <div class="suggestion-item">Which documents disagree on patient satisfaction for Q1?</div>
            <div class="suggestion-item">Which source should be authoritative for surgical infection metrics?</div>
            <div class="suggestion-item">Summarize unresolved conflicts by department and recommended owner.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render():
    docs_dir = Path(SAMPLE_DOCS_DIR)
    docs_dir.mkdir(parents=True, exist_ok=True)
    rows = _document_rows(docs_dir)
    supported = ", ".join(ext.upper().replace(".", "") for ext in SUPPORTED_EXTENSIONS)

    st.markdown(
        """
        <div class="main-inner">
          <div class="main-header">
            <div class="main-title">Documents</div>
            <div class="main-sub">Upload, index, and resolve evidence conflicts across hospital files</div>
          </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.45, 0.85], gap="large")

    with left:
        st.markdown(
            f"""
            <div class="content-panel upload-panel">
              <div class="panel-header">
                <span class="panel-title">Upload Documents</span>
                <span class="panel-meta">{html.escape(supported)}</span>
              </div>
              <div class="upload-copy">
                Add hospital reports, logs, SOPs, or board notes. Files are saved into the sample document library and can be re-indexed for RAG queries.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        uploaded = st.file_uploader(
            "Upload documents",
            type=[ext.replace(".", "") for ext in SUPPORTED_EXTENSIONS],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        if uploaded:
            uploaded_names = ", ".join(_safe_filename(file.name) for file in uploaded)
            st.markdown(
                f'<div class="upload-summary">{html.escape(uploaded_names)}</div>',
                unsafe_allow_html=True,
            )

        save_col, info_col = st.columns([0.36, 0.64], gap="medium")
        with save_col:
            save = st.button(
                "Save and re-index",
                type="primary",
                use_container_width=True,
                disabled=not uploaded,
            )
        with info_col:
            st.markdown(
                '<div class="inline-hint">Re-indexing refreshes the vector store used by Query & Analysis.</div>',
                unsafe_allow_html=True,
            )

        if save and uploaded:
            saved = _save_uploads(uploaded, docs_dir)
            if not saved:
                st.error("No supported files were saved.")
            else:
                from ingestion import ingest_documents

                with st.spinner("Saving and rebuilding the document index..."):
                    vector_store = ingest_documents(str(docs_dir))
                    st.session_state.vector_store = vector_store
                    st.cache_resource.clear()
                st.success(f"Saved and indexed {len(saved)} file(s): {', '.join(saved)}")
                st.rerun()

        total_chunks = sum(row["chunks"] for row in rows)
        st.markdown(
            f"""
            <div class="content-panel doc-table">
              <div class="panel-header">
                <span class="panel-title">Indexed Files</span>
                <span class="panel-meta">{len(rows)} files - about {total_chunks} chunks</span>
              </div>
            """,
            unsafe_allow_html=True,
        )

        if not rows:
            st.markdown(
                '<div class="empty-state">No documents indexed yet. Upload hospital files to begin.</div>',
                unsafe_allow_html=True,
            )
        else:
            for row in rows:
                st.markdown(
                    f"""
                    <div class="doc-item modern-doc-item">
                      <div>
                        <div class="doc-name">{html.escape(row["name"])}</div>
                        <div class="doc-meta">{html.escape(row["department"])} - {row["type"]} - {row["size"]}</div>
                      </div>
                      <span class="doc-badge">{row["chunks"]} chunks</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        _render_guidance(rows, bool(st.session_state.get("api_key")))

    st.markdown("</div>", unsafe_allow_html=True)
