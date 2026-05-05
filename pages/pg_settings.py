"""pages/pg_settings.py — Settings: API key, profiles, appearance, RAG tuning."""
import streamlit as st
import os
import json
from datetime import datetime
from config import SAMPLE_DOCS_DIR

DEFAULT_PROFILES = [
    {"id": "p1", "name": "Emergency Dept", "icon": "ED", "color": "#e53935",
     "description": "ED operational and staffing queries", "docs_dir": SAMPLE_DOCS_DIR},
    {"id": "p2", "name": "Finance", "icon": "FN", "color": "#1e88e5",
     "description": "Budget, expenditure and financial queries", "docs_dir": SAMPLE_DOCS_DIR},
    {"id": "p3", "name": "Administration", "icon": "AD", "color": "#8e24aa",
     "description": "Board-level and cross-department queries", "docs_dir": SAMPLE_DOCS_DIR},
    {"id": "p4", "name": "Quality & Patient Experience", "icon": "QX", "color": "#43a047",
     "description": "Satisfaction, complaints and quality metrics", "docs_dir": SAMPLE_DOCS_DIR},
]


def render(theme):
    st.markdown('<div class="page-title">Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Configure API keys, hospital profiles, appearance and RAG parameters</div>', unsafe_allow_html=True)

    tab_api, tab_prof, tab_appear, tab_rag = st.tabs(["API Key", "Profiles", "Appearance", "RAG Parameters"])

    # ── API Key ───────────────────────────────────────────────────────
    with tab_api:
        st.markdown('<div class="card card-accent">', unsafe_allow_html=True)
        st.markdown("**Gemini 2.5 Flash API Key**")
        st.markdown("Your key is stored only in session memory and is never persisted to disk.")
        current = st.session_state.get("api_key", "")
        new_key = st.text_input("API Key", value=current, type="password",
                                placeholder="AIza…", label_visibility="collapsed")
        c1, c2 = st.columns([2, 5])
        with c1:
            st.markdown('<div class="main-btn">', unsafe_allow_html=True)
            if st.button("Apply Key", use_container_width=True):
                st.session_state.api_key = new_key.strip()
                os.environ["GOOGLE_API_KEY"] = new_key.strip()
                st.cache_resource.clear()  # force chain rebuild with new key
                st.success("API key saved. Reconnecting to Gemini…")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            if st.button("Clear Key", use_container_width=True):
                st.session_state.api_key = ""
                os.environ.pop("GOOGLE_API_KEY", None)
                st.cache_resource.clear()
                st.warning("API key cleared.")
                st.rerun()
        if st.session_state.get("api_key"):
            st.success(f"Key active: {st.session_state.api_key[:8]}{'*' * 20}")
        else:
            st.info("No API key set. Get one free at [aistudio.google.com](https://aistudio.google.com)")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Profiles ──────────────────────────────────────────────────────
    with tab_prof:
        profiles = st.session_state.setdefault("profiles", list(DEFAULT_PROFILES))
        active_id = st.session_state.get("active_profile", {}).get("id", "p1")

        st.markdown("**Switch Profile**")
        cols = st.columns(len(profiles))
        for col, p in zip(cols, profiles):
            with col:
                is_active = p["id"] == active_id
                label = f"{p['icon']} {p['name']}"
                border = "2px solid" if is_active else "1px solid"
                box_style = f"border:{border} {'#00ff88' if theme=='dark' else '#028090'};border-radius:10px;padding:.8rem;text-align:center;cursor:pointer;margin-bottom:.4rem;"
                st.markdown(f'<div style="{box_style}"><div style="font-weight:700;font-size:.9rem">{p["icon"]}</div><div style="font-weight:600;font-size:.85rem;margin-top:.3rem">{p["name"]}</div><div style="font-size:.72rem;opacity:.55">{p["description"]}</div></div>', unsafe_allow_html=True)
                if st.button("Select" if not is_active else "✓ Active", key=f"sel_{p['id']}", use_container_width=True):
                    st.session_state.active_profile = p
                    st.session_state.active_docs_dir = p.get("docs_dir", SAMPLE_DOCS_DIR)
                    st.success(f"Switched to {p['name']}")
                    st.rerun()

        st.markdown("---")
        st.markdown("**Create New Profile**")
        with st.form("new_profile"):
            fc1, fc2 = st.columns([1, 4])
            with fc1:
                icon = st.text_input("Icon", "", max_chars=2)
            with fc2:
                pname = st.text_input("Profile Name", placeholder="e.g. Surgical Department")
            pdesc = st.text_input("Description", placeholder="Short description of this profile's focus")
            if st.form_submit_button("Create Profile"):
                if pname.strip():
                    new_p = {
                        "id": f"p_{len(profiles)+1}_{datetime.now().strftime('%H%M%S')}",
                        "name": pname.strip(), "icon": icon.strip() or "",
                        "color": "#028090", "description": pdesc.strip(),
                        "docs_dir": SAMPLE_DOCS_DIR,
                    }
                    profiles.append(new_p)
                    st.success(f"Profile '{pname}' created.")
                    st.rerun()

        st.markdown("---")
        st.markdown("**Delete a Profile**")
        del_options = {p["name"]: p["id"] for p in profiles if p["id"] not in ("p1","p2","p3","p4")}
        if del_options:
            to_del = st.selectbox("Select profile to delete", list(del_options.keys()))
            if st.button("Delete Selected Profile"):
                st.session_state.profiles = [p for p in profiles if p["id"] != del_options[to_del]]
                st.rerun()
        else:
            st.caption("Default profiles cannot be deleted.")

    # ── Appearance ────────────────────────────────────────────────────
    with tab_appear:
        st.markdown('<div class="card card-accent">', unsafe_allow_html=True)
        st.markdown("**Theme**")
        current_theme = st.session_state.get("theme", "dark")
        col_d, col_l, _ = st.columns([2, 2, 4])
        with col_d:
            if st.button("Dark Mode", use_container_width=True):
                st.session_state.theme = "dark"
                st.rerun()
        with col_l:
            if st.button("Light Mode", use_container_width=True):
                st.session_state.theme = "light"
                st.rerun()
        active_label = "Dark" if current_theme == "dark" else "Light"
        st.info(f"Current theme: **{active_label}**")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RAG Parameters ────────────────────────────────────────────────
    with tab_rag:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Retrieval Parameters**")
        top_k = st.slider("Top-K chunks to retrieve", 4, 16,
                           st.session_state.get("top_k", 8), key="top_k_slider")
        thresh = st.slider("Relevance threshold (min similarity)", 0.1, 0.7,
                            st.session_state.get("rel_thresh", 0.25), step=0.05, key="rel_slider")
        nli_thresh = st.slider("NLI contradiction threshold", 0.4, 0.9,
                                st.session_state.get("nli_thresh", 0.65), step=0.05, key="nli_slider")
        st.markdown("---")
        st.markdown("**LLM Parameters**")
        temp = st.slider("LLM temperature (0 = precise, 1 = creative)", 0.0, 1.0,
                          st.session_state.get("llm_temp", 0.2), step=0.05, key="temp_slider")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        if st.button("Apply Parameters", use_container_width=False):
            st.session_state.top_k = top_k
            st.session_state.rel_thresh = thresh
            st.session_state.nli_thresh = nli_thresh
            st.session_state.llm_temp = temp
            st.cache_resource.clear()  # force chain + store reload with new params
            st.success("Parameters saved. Reloading resources…")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
