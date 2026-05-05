"""pages/pg_dashboard.py — Overview page using clinical design system."""
import streamlit as st
from datetime import datetime


def render(vs, theme):
    qs = st.session_state.get("query_history", [])
    chunks = 0
    if vs:
        try: chunks = vs._collection.count()
        except: pass

    # ── Header ────────────────────────────────────────────────────────
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Hospital intelligence overview — Q1 2025</div>', unsafe_allow_html=True)

    # ── Stat cards ────────────────────────────────────────────────────
    n_conflicts = sum(1 for q in qs if q.get("has_conflicts"))
    avg_conf = f"{sum(q.get('confidence',0) for q in qs)/len(qs):.0f}%" if qs else "—"

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl, cls in [
        (c1, chunks,      "Indexed Chunks",  "stat-blue"),
        (c2, len(qs),     "Queries Run",     "stat-green"),
        (c3, n_conflicts, "Conflicts Found",  "stat-red"),
        (c4, avg_conf,    "Avg Confidence",  "stat-amber"),
    ]:
        with col:
            st.markdown(
                f'<div class="stat-card {cls}">'
                f'<div class="stat-value">{val}</div>'
                f'<div class="stat-label">{lbl}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-bottom:1.4rem'></div>", unsafe_allow_html=True)

    # ── Bottom grid ───────────────────────────────────────────────────
    col_l, col_r = st.columns([3, 1], gap="large")

    with col_l:
        st.markdown('<div class="section-title">Recent Queries</div>', unsafe_allow_html=True)
        if not qs:
            st.markdown(
                '<div class="content-panel"><div class="empty-state">'
                'No queries yet. Head to Query &amp; Analysis to get started.'
                '</div></div>',
                unsafe_allow_html=True,
            )
        else:
            items = "".join(
                f'<div class="query-item">'
                f'<span style="flex:1;margin-right:12px">{q["question"][:65]}{"…" if len(q["question"])>65 else ""}</span>'
                f'<span class="conf-badge">{q.get("confidence",0):.0f}% · {q.get("ts","")}</span>'
                f'</div>'
                for q in reversed(qs[-8:])
            )
            st.markdown(
                f'<div class="content-panel"><div class="panel-header">'
                f'<span class="panel-title">History</span>'
                f'<span style="font-size:12px;color:#3A5468">{len(qs)} total</span>'
                f'</div>{items}</div>',
                unsafe_allow_html=True,
            )

    with col_r:
        st.markdown('<div class="section-title">Quick Actions</div>', unsafe_allow_html=True)
        if st.button("New Query", use_container_width=True, key="dash_q", type="primary"):
            st.session_state.page = "query"; st.rerun()
        if st.button("Manage Documents", use_container_width=True, key="dash_d"):
            st.session_state.page = "documents"; st.rerun()

        dept = st.session_state.get("active_dept", {})
        if dept:
            st.markdown(
                f'<div style="margin-top:1rem"><div class="section-title">Active Profile</div>'
                f'<div class="content-panel" style="padding:12px 14px;">'
                f'<div style="display:flex;align-items:center;gap:8px">'
                f'<div style="width:8px;height:8px;border-radius:50%;background:{dept.get("hex","#00D68F")}"></div>'
                f'<span style="font-size:13px;font-weight:600">{dept.get("full","—")}</span></div>'
                f'<div style="font-size:11px;margin-top:4px;opacity:.55">Hospital RAG v2.0 · Q1 2025</div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
