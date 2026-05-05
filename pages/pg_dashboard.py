"""pages/pg_dashboard.py — Dashboard page with exact UI"""
import streamlit as st

def render(vs):
    qs = st.session_state.get("query_history", [])
    chunks = 0
    if vs:
        try: chunks = vs._collection.count()
        except: pass

    n_conflicts = sum(1 for q in qs if q.get("has_conflicts"))
    avg_conf = f"{sum(q.get('confidence',0) for q in qs)/len(qs):.0f}%" if qs else "—"
    
    st.markdown("""
    <div class="main-inner">
      <div class="main-header">
        <div class="main-title">Dashboard</div>
        <div class="main-sub">Hospital intelligence overview — Q1 2025</div>
      </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
      <div class="stats-grid">
        <div class="stat-card chunks"><div class="stat-value">{chunks}</div><div class="stat-label">Indexed Chunks</div></div>
        <div class="stat-card queries"><div class="stat-value">{len(qs)}</div><div class="stat-label">Queries Run</div></div>
        <div class="stat-card conflicts"><div class="stat-value">{n_conflicts}</div><div class="stat-label">Conflicts Found</div></div>
        <div class="stat-card confidence"><div class="stat-value">{avg_conf}</div><div class="stat-label">Avg Confidence</div></div>
      </div>
    """, unsafe_allow_html=True)

    # We need to split into 2 columns for bottom grid because Streamlit doesn't easily let us overlay buttons inside pure HTML without breaking the layout,
    # BUT we can just use Streamlit's columns and apply the exact CSS layout!
    # Or, we can use the same overlay trick we used in the sidebar.
    
    col1, col2 = st.columns([1, 0.4], gap="medium")
    
    with col1:
        st.markdown('<div class="section-title">Recent Queries</div>', unsafe_allow_html=True)
        if not qs:
            st.markdown('<div class="content-panel"><div class="empty-state">No queries yet. Head to Query & Analysis to get started.</div></div>', unsafe_allow_html=True)
        else:
            items = "".join(
                f'<div class="query-item">'
                f'<span style="flex:1">{q["question"][:65]}{"…" if len(q["question"])>65 else ""}</span>'
                f'<span class="query-badge">{q.get("confidence",0):.0f}% · {q.get("ts","")}</span>'
                f'</div>'
                for q in reversed(qs[-8:])
            )
            st.markdown(f'<div class="content-panel">{items}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Quick Actions</div>', unsafe_allow_html=True)
        
        actions = [("query", "+ New Query"), ("documents", "Manage Documents"), ("settings", "Settings")]
        for key, label in actions:
            st.markdown(f'<div class="click-wrapper"><button class="action-btn">{label}</button></div>', unsafe_allow_html=True)
            st.markdown('<div class="invisible-btn">', unsafe_allow_html=True)
            if st.button(" ", key=f"dash_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        dept = st.session_state.get("active_dept", {"name": "Administration"})
        st.markdown(f"""
        <div class="section-title" style="margin-top:18px;">Active Profile</div>
        <div class="active-profile-card">
          <div class="active-profile-name"><span class="active-indicator"></span><span>{dept['name']}</span></div>
          <div class="active-profile-sub">Hospital RAG v2.0 · Q1 2025</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
