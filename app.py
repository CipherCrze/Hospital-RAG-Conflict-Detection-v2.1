"""
Hospital RAG Dashboard v2 — matches clinical mockup design.
Sidebar: logo · nav · profile badge · dept switcher · API key · stats · theme
Main: Overview / Query & Analysis / Documents tabs
"""
import os, sys
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Hospital RAG", page_icon="H",
                   layout="wide", initial_sidebar_state="expanded")

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from theme import inject
theme = st.session_state.setdefault("theme", "dark")
st.markdown(inject(theme), unsafe_allow_html=True)

# ── Defaults ──────────────────────────────────────────────────────────
st.session_state.setdefault("api_key", os.environ.get("GOOGLE_API_KEY", ""))
st.session_state.setdefault("query_history", [])
st.session_state.setdefault("top_k", 8)
st.session_state.setdefault("llm_temp", 0.2)
st.session_state.setdefault("page", "overview")

from config import SAMPLE_DOCS_DIR, CHROMA_PERSIST_DIR

# Department definitions with semantic colors
DEPTS = [
    {"id": "ED", "name": "Emergency",     "full": "Emergency Dept",           "hex": "#D94F3D"},
    {"id": "FN", "name": "Finance",       "full": "Finance",                  "hex": "#607080"},
    {"id": "AD", "name": "Admin",         "full": "Administration",           "hex": "#7B5EA7"},
    {"id": "QX", "name": "Quality",       "full": "Quality & Patient Exp.",   "hex": "#2E9E6B"},
    {"id": "IC", "name": "Infection",     "full": "Infection Control",        "hex": "#E09B2D"},
    {"id": "SG", "name": "Surgical",      "full": "Surgical",                 "hex": "#4DB8FF"},
]
st.session_state.setdefault("active_dept", DEPTS[2])  # Admin default

# ── Cached resources ──────────────────────────────────────────────────
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


# ════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════
with st.sidebar:
    dept = st.session_state.active_dept
    acc  = "#4DB8FF" if theme == "dark" else "#1A6FA8"
    surf = "#111820" if theme == "dark" else "#F4F7F9"
    bord = "#1E2D3D" if theme == "dark" else "#DDE4EA"
    muted= "#7A9BB5" if theme == "dark" else "#607080"
    txt  = "#E8F0F7" if theme == "dark" else "#1C2B36"

    # ── Logo ──────────────────────────────────────────────────────
    st.markdown(f'<div class="sb-logo">Hospital RAG</div>', unsafe_allow_html=True)

    # ── Navigation ────────────────────────────────────────────────
    cur = st.session_state.page
    NAV = [
        ("overview",  "Dashboard"),
        ("query",     "Query & Analysis"),
        ("documents", "Documents"),
    ]
    for key, label in NAV:
        active = cur == key
        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

    # ── Active Profile badge ──────────────────────────────────────
    st.markdown('<span class="sb-label">Active Profile</span>', unsafe_allow_html=True)
    st.markdown(
        f"""<div class="profile-badge">
          <div class="badge-circle" style="background:{dept['hex']}">{dept['id']}</div>
          <div>
            <div class="badge-name">{dept['full']}</div>
            <div class="badge-sub">Hospital RAG v2.0</div>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    # ── Department switcher grid ──────────────────────────────────
    st.markdown('<span class="sb-label">Switch Profile</span>', unsafe_allow_html=True)
    rows = [DEPTS[i:i+3] for i in range(0, len(DEPTS), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, d in zip(cols, row):
            is_active = d["id"] == dept["id"]
            bg = f"{d['hex']}22" if is_active else surf
            bw = "2px" if is_active else "1.5px"
            with col:
                st.markdown(
                    f"""<div style="border:{bw} solid {d['hex']};border-radius:6px;
                    padding:5px 4px;text-align:center;background:{bg};margin-bottom:3px">
                      <div style="font-size:11px;font-weight:600;color:{d['hex']};
                           font-family:'DM Mono',monospace">{d['id']}</div>
                      <div style="font-size:9px;color:{muted};margin-top:1px">{d['name']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                if st.button("", key=f"dept_{d['id']}", use_container_width=True,
                             help=d["full"]):
                    st.session_state.active_dept = d
                    st.rerun()

    st.markdown(f"<hr style='border-color:{bord};margin:.6rem 0'>", unsafe_allow_html=True)

    # ── API Key ───────────────────────────────────────────────────
    st.markdown('<span class="sb-label">Gemini 2.5 Flash API Key</span>', unsafe_allow_html=True)
    new_key = st.text_input("key", value=api_key, type="password",
                            placeholder="AIza…", label_visibility="collapsed")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Apply", key="key_apply", use_container_width=True, type="primary"):
            st.session_state.api_key = new_key.strip()
            os.environ["GOOGLE_API_KEY"] = new_key.strip()
            st.cache_resource.clear(); st.rerun()
    with c2:
        if st.button("Clear", key="key_clear", use_container_width=True):
            st.session_state.api_key = ""
            os.environ.pop("GOOGLE_API_KEY", None)
            st.cache_resource.clear(); st.rerun()

    # Key status
    if api_key:
        st.markdown(
            f"<div style='font-size:11px;font-family:DM Mono,monospace;"
            f"color:#00D68F;margin:.3rem 0 .6rem'>{api_key[:8]}{'·'*10}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='font-size:11px;color:#FF5C5C;margin:.3rem 0 .6rem'>"
            "No key — queries disabled</div>",
            unsafe_allow_html=True,
        )

    st.markdown(f"<hr style='border-color:{bord};margin:.4rem 0 .6rem'>", unsafe_allow_html=True)

    # ── Stats mini-grid ───────────────────────────────────────────
    qs = st.session_state.get("query_history", [])
    chunks = 0
    if _vs:
        try: chunks = _vs._collection.count()
        except: pass
    n_conflicts = sum(1 for q in qs if q.get("has_conflicts"))
    avg_conf = f"{sum(q.get('confidence',0) for q in qs)/len(qs):.0f}%" if qs else "—"

    st.markdown(
        f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:.8rem">
          <div class="stat-card stat-blue" style="padding:10px 12px;border-radius:8px">
            <div class="stat-value" style="font-size:20px">{chunks}</div>
            <div class="stat-label">Chunks</div></div>
          <div class="stat-card stat-green" style="padding:10px 12px;border-radius:8px">
            <div class="stat-value" style="font-size:20px">{len(qs)}</div>
            <div class="stat-label">Queries</div></div>
          <div class="stat-card stat-red" style="padding:10px 12px;border-radius:8px">
            <div class="stat-value" style="font-size:20px">{n_conflicts}</div>
            <div class="stat-label">Conflicts</div></div>
          <div class="stat-card stat-amber" style="padding:10px 12px;border-radius:8px">
            <div class="stat-value" style="font-size:20px">{avg_conf}</div>
            <div class="stat-label">Avg Conf.</div></div>
        </div>""",
        unsafe_allow_html=True,
    )

    # ── Theme toggle ──────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Dark", key="sb_dark", use_container_width=True,
                     type="primary" if theme == "dark" else "secondary"):
            st.session_state.theme = "dark"; st.rerun()
    with c2:
        if st.button("Light", key="sb_light", use_container_width=True,
                     type="primary" if theme == "light" else "secondary"):
            st.session_state.theme = "light"; st.rerun()


# ════════════════════════════════════════════════════════════════════
# MAIN — tab router
# ════════════════════════════════════════════════════════════════════
page = st.session_state.page

if page == "overview":
    from pages.pg_dashboard import render
    render(_vs, theme)

elif page == "query":
    from pages.pg_query import render
    render(_vs, _chain, api_key, theme)

elif page == "documents":
    from pages.pg_documents import render
    render(theme)
