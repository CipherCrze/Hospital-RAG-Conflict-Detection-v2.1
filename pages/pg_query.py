"""pages/pg_query.py — Query & Analysis page with conflict detection and resolutions."""
import streamlit as st
from datetime import datetime


DEMO_QUERIES = [
    "How has patient satisfaction changed in Q1?",
    "What is the ED budget status?",
    "Were there emergency procurement requests?",
    "What are the top complaint categories?",
    "How did nursing availability trend?",
    "Give a complete Q1 performance overview.",
]


def _tag(level):
    return f'<span class="tag-{level.lower()}">{level}</span>'


def render(vs, chain, api_key, theme):
    st.markdown('<div class="page-title">Query & Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Ask questions across all hospital documents — conflicts detected automatically</div>', unsafe_allow_html=True)

    if not api_key:
        st.warning("⚙ Please set your Gemini API key in Settings first.")
        return
    if vs is None:
        st.warning("📄 No documents indexed yet. Go to Documents to ingest files.")
        return
    if chain is None:
        st.info("Building LLM chain…")
        return

    # Demo query buttons
    with st.expander("Demo Queries", expanded=False):
        cols = st.columns(3)
        for i, q in enumerate(DEMO_QUERIES):
            if cols[i % 3].button(q, key=f"demo_{i}", use_container_width=True):
                st.session_state.query_input = q
                st.rerun()

    query = st.text_area(
        "Your Question",
        key="query_input",
        placeholder="e.g. How has patient satisfaction changed in Q1?",
        height=90,
        label_visibility="collapsed",
    )

    c1, c2, c3 = st.columns([2, 1, 5])
    with c1:
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        analyze = st.button("Analyze", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if st.button("Clear", use_container_width=True):
            st.session_state.pop("last_result", None)
            st.session_state.query_input = ""
            st.rerun()

    if analyze and query.strip():
        with st.spinner("Retrieving documents and detecting conflicts…"):
            try:
                from rag_pipeline import query_with_conflict_detection
                result = query_with_conflict_detection(chain=chain, vector_store=vs, question=query.strip())
                result["question"] = query.strip()
                result["ts"] = datetime.now().strftime("%H:%M")
                st.session_state.last_result = result
                # Save to history
                hist = st.session_state.setdefault("query_history", [])
                hist.append({
                    "question": query.strip(),
                    "confidence": result["confidence"]["score"],
                    "confidence_level": result["confidence"]["level"],
                    "has_conflicts": result["conflicts"]["has_conflicts"],
                    "ts": result["ts"],
                })
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                return

    result = st.session_state.get("last_result")
    if not result:
        return

    st.markdown("---")

    # ── Answer ────────────────────────────────────────────────────────
    conf = result["confidence"]
    col_a, col_b = st.columns([5, 2])
    with col_a:
        st.markdown("**Answer**")
        st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown("**Confidence**")
        lvl = conf["level"]
        st.markdown(
            f'<div class="card card-accent" style="text-align:center">'
            f'<div class="metric-val">{conf["score"]:.0f}%</div>'
            f'<div style="margin-top:.3rem">{_tag(lvl)}</div></div>',
            unsafe_allow_html=True,
        )
        with st.expander("Factors"):
            for f in conf.get("factors", []):
                st.markdown(f"- {f}")

    # ── Executive Summary ─────────────────────────────────────────────
    if st.button("Generate Executive Summary", key="exec_sum"):
        with st.spinner("Summarising…"):
            from resolution import executive_summary
            summ = executive_summary(
                question=result["question"],
                answer=result["answer"],
                conflict_result=result["conflicts"],
                n_chunks=len(result.get("retrieved_chunks", [])),
                api_key=api_key,
            )
            st.session_state.exec_summary = summ
    if "exec_summary" in st.session_state:
        st.markdown(f'<div class="resolution-box">{st.session_state.exec_summary}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Conflict Panel ────────────────────────────────────────────────
    st.markdown("**Conflict Analysis**")
    cr = result["conflicts"]
    if not cr["has_conflicts"]:
        st.success("✓ No conflicting evidence detected among retrieved documents.")
    else:
        st.markdown(
            f'<div class="conflict-banner"><strong>{cr["conflict_count"]} conflict(s) detected</strong>'
            f' across {cr.get("total_pairs", "?")} chunk pairs '
            f'(conflict ratio {cr.get("conflict_ratio", 0):.0%})</div>',
            unsafe_allow_html=True,
        )
        for i, c in enumerate(cr["conflicts"], 1):
            with st.expander(
                f"Conflict #{i} — {c['doc_a']['source']} vs {c['doc_b']['source']} "
                f"| Score {c['contradiction_score']:.2f}",
                expanded=(i == 1),
            ):
                ca, cb = st.columns(2)
                for col, side, label in [(ca, "doc_a", "Document A"), (cb, "doc_b", "Document B")]:
                    with col:
                        st.markdown(f"**{label}:** `{c[side]['source']}`")
                        st.info(c[side]["snippet"][:280])
                        st.caption(f"Dept: {c[side].get('department','—')} · Similarity: {c[side]['similarity_score']:.2f}")
                s1, s2, s3 = st.columns(3)
                s1.metric("Contradiction", f"{c['contradiction_score']:.2f}")
                s2.metric("Entailment", f"{c.get('entailment_score',0):.2f}")
                s3.metric("Neutral", f"{c.get('neutral_score',0):.2f}")

                st.markdown("---")
                st.markdown('<div class="resolution-box" style="padding:.6rem 1rem;"><strong>Resolution Suggestion</strong></div>', unsafe_allow_html=True)
                res_key = f"res_{i}"
                if st.button(f"Suggest Resolution — Conflict {i}", key=f"btn_res_{i}"):
                    with st.spinner("Asking Gemini for resolution steps…"):
                        from resolution import suggest_resolution
                        st.session_state[res_key] = suggest_resolution(c, api_key)
                if res_key in st.session_state:
                    st.markdown(f'<div class="resolution-box">{st.session_state[res_key]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Sources ───────────────────────────────────────────────────────
    with st.expander(f"Source Provenance ({len(result['sources'])} documents)", expanded=False):
        for src in result["sources"]:
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"**{src['source']}**")
            c2.markdown(f"Dept: `{src['department']}`")
            c3.markdown(f"Chunks: `{src['chunks_retrieved']}`")
            c4.markdown(f"Max sim: `{src['max_similarity']:.3f}`")
            st.markdown("---")

    with st.expander("Raw Retrieved Chunks", expanded=False):
        for i, ch in enumerate(result.get("retrieved_chunks", []), 1):
            st.markdown(f"**#{i}** `{ch['source']}` — Score: `{ch['similarity_score']:.4f}`")
            st.text(ch["content"][:400])
            st.markdown("---")
