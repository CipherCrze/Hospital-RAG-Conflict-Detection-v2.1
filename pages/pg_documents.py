"""pages/pg_documents.py — Documents page exact UI"""
import os
import streamlit as st
from config import SAMPLE_DOCS_DIR, SUPPORTED_EXTENSIONS

def render():
    st.markdown("""
    <div class="main-inner">
      <div class="main-header">
        <div class="main-title">Documents</div>
        <div class="main-sub">Manage indexed hospital knowledge base</div>
      </div>
    """, unsafe_allow_html=True)

    docs_dir = SAMPLE_DOCS_DIR
    os.makedirs(docs_dir, exist_ok=True)
    files = sorted(f for f in os.listdir(docs_dir) if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS)

    st.markdown(f"""
    <div class="content-panel">
      <div class="panel-header"><span class="panel-title">Indexed Files</span><span style="font-size:12px;color:#3A5468;">{len(files)} files</span></div>
    """, unsafe_allow_html=True)

    for fname in files:
        st.markdown(f"""
        <div class="doc-item">
            <span>{fname}</span>
            <span class="doc-badge">12 chunks</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Upload New Document</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Drop files here", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    if uploaded:
        if st.button("Save and Re-index", type="primary"):
            for uf in uploaded:
                with open(os.path.join(docs_dir, uf.name), "wb") as out:
                    out.write(uf.getbuffer())
            from ingestion import ingest_documents
            with st.spinner("Indexing…"):
                st.session_state.vector_store = ingest_documents(docs_dir)
            st.success("Documents indexed successfully.")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
