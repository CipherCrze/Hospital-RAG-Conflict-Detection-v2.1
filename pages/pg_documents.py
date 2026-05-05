"""pages/pg_documents.py — Document management and upload page."""
import os, shutil, tempfile
import streamlit as st
from config import SAMPLE_DOCS_DIR, CHROMA_PERSIST_DIR, SUPPORTED_EXTENSIONS


def render(theme):
    st.markdown('<div class="page-title">Documents</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Manage hospital documents — upload new files or re-index existing ones</div>', unsafe_allow_html=True)

    # Determine active docs directory
    docs_dir = st.session_state.get("active_docs_dir", SAMPLE_DOCS_DIR)
    os.makedirs(docs_dir, exist_ok=True)

    tab1, tab2 = st.tabs(["Indexed Documents", "Upload New Documents"])

    # ── Tab 1: Indexed docs ──────────────────────────────────────────
    with tab1:
        files = sorted(f for f in os.listdir(docs_dir)
                       if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS)

        st.markdown(f"**{len(files)} document(s)** in `{os.path.basename(docs_dir)}/`")

        if not files:
            st.info("No documents found. Upload files using the Upload tab.")
        else:
            for fname in files:
                fpath = os.path.join(docs_dir, fname)
                size_kb = os.path.getsize(fpath) // 1024
                ext = os.path.splitext(fname)[1].upper().replace(".", "")
                col_a, col_b, col_c = st.columns([5, 1, 1])
                with col_a:
                    st.markdown(
                        f'<div class="card" style="padding:.7rem 1rem;margin-bottom:.4rem;">'
                        f'<strong>{fname}</strong>'
                        f'<span style="font-size:.72rem;opacity:.5;margin-left:.8rem">{ext} · {size_kb} KB</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                with col_b:
                    with open(fpath, "rb") as f:
                        st.download_button("Download", data=f, file_name=fname, key=f"dl_{fname}", use_container_width=True)
                with col_c:
                    if st.button("Delete", key=f"del_{fname}", use_container_width=True):
                        os.remove(fpath)
                        st.session_state.vector_store = None
                        st.toast(f"Deleted {fname}. Re-index to update.")
                        st.rerun()

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="main-btn">', unsafe_allow_html=True)
            if st.button("Re-index All Documents", use_container_width=True):
                with st.spinner("Ingesting documents — this may take a minute…"):
                    try:
                        from ingestion import ingest_documents
                        ingest_documents(docs_dir)
                        st.cache_resource.clear()  # invalidate cached vector store
                        st.success(f"Indexed {len(files)} document(s). Reloading…")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Ingestion failed: {e}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            if st.button("Clear Vector Store", use_container_width=True):
                if os.path.exists(CHROMA_PERSIST_DIR):
                    shutil.rmtree(CHROMA_PERSIST_DIR)
                st.session_state.vector_store = None
                st.session_state.chain = None
                st.warning("Vector store cleared. Re-index to restore.")
                st.rerun()

    # ── Tab 2: Upload ────────────────────────────────────────────────
    with tab2:
        st.markdown("Upload PDF, DOCX, or TXT files to add them to the knowledge base.")
        uploaded = st.file_uploader(
            "Drop files here",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        if uploaded:
            col_p, col_s = st.columns(2)
            with col_p:
                st.markdown('<div class="main-btn">', unsafe_allow_html=True)
                if st.button("Save and Re-index", use_container_width=True):
                    saved = []
                    for uf in uploaded:
                        dest = os.path.join(docs_dir, uf.name)
                        with open(dest, "wb") as out:
                            out.write(uf.getbuffer())
                        saved.append(uf.name)

                    with st.spinner(f"Indexing {len(saved)} new file(s)…"):
                        try:
                            from ingestion import ingest_documents
                            vs = ingest_documents(docs_dir)
                            st.session_state.vector_store = vs
                            st.session_state.chain = None
                            st.success(f"✓ Saved and indexed: {', '.join(saved)}")
                        except Exception as e:
                            st.error(f"Ingestion failed: {e}")
                st.markdown('</div>', unsafe_allow_html=True)
            with col_s:
                if st.button("Save Only (no re-index)", use_container_width=True):
                    for uf in uploaded:
                        dest = os.path.join(docs_dir, uf.name)
                        with open(dest, "wb") as out:
                            out.write(uf.getbuffer())
                    st.success(f"Saved {len(uploaded)} file(s). Re-index when ready.")

            st.markdown("**Preview:**")
            for uf in uploaded:
                st.markdown(
                    f'<div class="card" style="padding:.6rem 1rem;margin-bottom:.4rem;">'
                    f'📎 <strong>{uf.name}</strong> — {uf.size//1024} KB</div>',
                    unsafe_allow_html=True,
                )
