"""pages/pg_query.py — Query page with exact UI"""
import streamlit as st
from datetime import datetime

def _tag(level):
    if level == "High": cls = "tag-high"
    elif level == "Medium": cls = "tag-medium"
    else: cls = "tag-low"
    return f'<span class="{cls}">{level}</span>'

def render(vs, chain, api_key):
    st.markdown("""
    <div class="main-inner">
      <div class="main-header">
        <div class="main-title">Query & Analysis</div>
        <div class="main-sub">Run queries across indexed hospital documents</div>
      </div>
    """, unsafe_allow_html=True)

    if not api_key: st.warning("Please set your Gemini API key in Settings."); return
    if vs is None: st.warning("No documents indexed. Go to Documents to upload."); return
    if chain is None: st.info("Building LLM chain…"); return

    st.markdown("""
    <div class="content-panel" style="margin-bottom:20px;">
      <div class="panel-header"><span class="panel-title">New Query</span></div>
      <div class="query-form">
    """, unsafe_allow_html=True)
    
    # Render text area natively so user can type
    query = st.text_area("Query", key="query_input", placeholder="Ask a question about your indexed documents...", height=80, label_visibility="collapsed")
    
    st.markdown(f'<div class="click-wrapper"><button class="query-submit">Run Query</button></div>', unsafe_allow_html=True)
    st.markdown('<div class="invisible-btn" style="text-align: right;">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([4,1,1])
    with c3:
        analyze = st.button(" ", use_container_width=True)
    st.markdown('</div></div></div>', unsafe_allow_html=True)

    if analyze and query.strip():
        with st.spinner("Analyzing…"):
            try:
                from rag_pipeline import query_with_conflict_detection
                result = query_with_conflict_detection(chain=chain, vector_store=vs, question=query.strip())
                result["question"] = query.strip()
                result["ts"] = datetime.now().strftime("%H:%M")
                st.session_state.last_result = result
                hist = st.session_state.setdefault("query_history", [])
                hist.append({
                    "question": query.strip(), "confidence": result["confidence"]["score"],
                    "confidence_level": result["confidence"]["level"], "has_conflicts": result["conflicts"]["has_conflicts"], "ts": result["ts"]
                })
            except Exception as e:
                st.error(f"Analysis failed: {e}")

    result = st.session_state.get("last_result")
    if result:
        st.markdown(f"""
        <div class="content-panel" style="margin-bottom:20px;">
            <div class="panel-header"><span class="panel-title">Result: {result['question']}</span></div>
            <div style="padding: 16px; color: #E8F0F7; font-size: 13px; line-height: 1.6;">
                <div style="margin-bottom: 12px; font-weight: 500; color: #4DB8FF;">Confidence: {result['confidence']['score']:.0f}% {_tag(result['confidence']['level'])}</div>
                <div>{result['answer']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Conflict rendering
        cr = result["conflicts"]
        if cr["has_conflicts"]:
            st.markdown(f"""
            <div class="content-panel" style="border-color: #FF5C5C;">
              <div class="panel-header" style="background: rgba(255,92,92,0.1); border-color: rgba(255,92,92,0.2);"><span class="panel-title" style="color: #FF5C5C;">{cr["conflict_count"]} Conflict(s) Detected</span></div>
              <div style="padding: 16px;">
            """, unsafe_allow_html=True)
            for i, c in enumerate(cr["conflicts"], 1):
                st.markdown(f"**Conflict #{i}** (Contradiction Score: {c['contradiction_score']:.2f})")
                ca, cb = st.columns(2)
                ca.info(f"**{c['doc_a']['source']}**\n\n{c['doc_a']['snippet'][:200]}...")
                cb.error(f"**{c['doc_b']['source']}**\n\n{c['doc_b']['snippet'][:200]}...")
            st.markdown("</div></div>", unsafe_allow_html=True)

    # Query history
    st.markdown('<div class="section-title">Query History</div>', unsafe_allow_html=True)
    qs = st.session_state.get("query_history", [])
    if not qs:
        st.markdown('<div class="content-panel"><div class="empty-state">No queries yet.</div></div>', unsafe_allow_html=True)
    else:
        items = "".join(
            f'<div class="query-item">'
            f'<span style="flex:1">{q["question"][:80]}{"…" if len(q["question"])>80 else ""}</span>'
            f'<span class="query-badge">{q.get("confidence",0):.0f}% conf</span>'
            f'</div>'
            for q in reversed(qs)
        )
        st.markdown(f'<div class="content-panel">{items}</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
