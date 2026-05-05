"""app.py — Main Application Entry Point with Exact Clinical UI"""
import os, sys
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Hospital RAG", page_icon="H", layout="wide", initial_sidebar_state="expanded")

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path: sys.path.insert(0, ROOT)

from theme import inject
st.markdown(inject(), unsafe_allow_html=True)

# Defaults
st.session_state.setdefault("api_key", os.environ.get("GOOGLE_API_KEY", ""))
st.session_state.setdefault("query_history", [])
st.session_state.setdefault("top_k", 8)
st.session_state.setdefault("llm_temp", 0.2)
st.session_state.setdefault("page", "dashboard")

from config import CHROMA_PERSIST_DIR

# Departments
DEPTS = [
    {"id": "ED", "name": "Emergency", "hex": "#D94F3D", "class": "ed"},
    {"id": "FN", "name": "Finance",   "hex": "#607080", "class": "fn"},
    {"id": "AD", "name": "Admin",     "hex": "#7B5EA7", "class": "ad"},
    {"id": "QX", "name": "Quality",   "hex": "#2E9E6B", "class": "qx"},
    {"id": "IC", "name": "Infection", "hex": "#E09B2D", "class": "ic"},
    {"id": "SG", "name": "Surgical",  "hex": "#4DB8FF", "class": "sg"},
]
st.session_state.setdefault("active_dept", DEPTS[2])  # Admin default

@st.cache_resource(show_spinner="Loading document index…")
def _get_vs(persist_dir):
    from ingestion import load_vector_store
    return load_vector_store(persist_dir)

@st.cache_resource(show_spinner="Connecting to Gemini…")
def _get_chain(api_key, temp):
    import config as _c; _c.LLM_TEMPERATURE = temp
    from rag_pipeline import build_chain
    return build_chain(api_key)

chroma_path = Path(CHROMA_PERSIST_DIR)
_vs, _chain = None, None
if chroma_path.exists() and any(chroma_path.iterdir()):
    try: _vs = _get_vs(CHROMA_PERSIST_DIR)
    except Exception as e: st.warning(f"Vector store: {e}")

api_key = st.session_state.get("api_key", "")
if api_key:
    try: _chain = _get_chain(api_key, st.session_state.get("llm_temp", 0.2))
    except: pass

# ── Sidebar ──
with st.sidebar:
    dept = st.session_state.active_dept
    
    st.markdown('<div class="sidebar-logo">Hospital RAG</div>', unsafe_allow_html=True)
    
    # Navigation
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    NAV = [
        ("dashboard", "Dashboard", '<svg class="nav-icon" viewBox="0 0 16 16" fill="currentColor"><rect x="1" y="1" width="6" height="6" rx="1"/><rect x="9" y="1" width="6" height="6" rx="1"/><rect x="1" y="9" width="6" height="6" rx="1"/><rect x="9" y="9" width="6" height="6" rx="1"/></svg>'),
        ("documents", "Documents", '<svg class="nav-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="1" width="10" height="13" rx="1"/><line x1="4.5" y1="5" x2="10.5" y2="5"/><line x1="4.5" y1="8" x2="10.5" y2="8"/><line x1="4.5" y1="11" x2="8" y2="11"/></svg>'),
        ("query", "Query & Analysis", '<svg class="nav-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="7" cy="7" r="4.5"/><line x1="10.5" y1="10.5" x2="14" y2="14"/></svg>'),
        ("settings", "Settings", '<svg class="nav-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="8" r="2.5"/><path d="M8 1v2M8 13v2M1 8h2M13 8h2M3.05 3.05l1.41 1.41M11.54 11.54l1.41 1.41M3.05 12.95l1.41-1.41M11.54 4.46l1.41-1.41"/></svg>')
    ]
    for key, label, svg in NAV:
        active = "active" if st.session_state.page == key else ""
        # We wrap the Streamlit button in a relative div, and style the button to be invisible over our HTML
        html = f"""
        <div class="click-wrapper">
            <a class="sidebar-nav-item {active}">{svg} {label}</a>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        st.markdown('<div class="invisible-btn">', unsafe_allow_html=True)
        if st.button(" ", key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Active Profile
    st.markdown('<div class="section-label">Active Profile</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="profile-badge">
      <div class="badge-initials" style="background:{dept['hex']}">{dept['id']}</div>
      <div>
        <div class="badge-name">{dept['name']}</div>
        <div class="badge-sub">Hospital RAG v2.0</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Switch Profile
    st.markdown('<div class="section-label">Switch Profile</div>', unsafe_allow_html=True)
    
    for i in range(0, len(DEPTS), 3):
        row_depts = DEPTS[i:i+3]
        cols = st.columns(3)
        for col, d in zip(cols, row_depts):
            with col:
                active_cls = "active" if d['id'] == dept['id'] else ""
                st.markdown(f"""
                <div class="click-wrapper">
                    <div class="dept-btn {d['class']} {active_cls}">
                        <div class="dept-code">{d['id']}</div>
                        <div class="dept-name">{d['name']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="invisible-btn">', unsafe_allow_html=True)
                if st.button(" ", key=f"dept_{d['id']}", use_container_width=True):
                    st.session_state.active_dept = d
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # API Key
    st.markdown('<div class="api-section"><div class="api-label">Gemini 2.5 Flash API Key</div></div>', unsafe_allow_html=True)
    new_key = st.text_input("key", value=api_key, type="password", placeholder="Enter key...", label_visibility="collapsed")
    if new_key.strip() != api_key:
        st.session_state.api_key = new_key.strip()
        os.environ["GOOGLE_API_KEY"] = new_key.strip()
        st.cache_resource.clear()
        st.rerun()


# ── Main Content ──
page = st.session_state.page

if page == "dashboard":
    from pages.pg_dashboard import render
    render(_vs)
elif page == "query":
    from pages.pg_query import render
    render(_vs, _chain, api_key)
elif page == "documents":
    from pages.pg_documents import render
    render()
elif page == "settings":
    from pages.pg_settings import render
    render()
