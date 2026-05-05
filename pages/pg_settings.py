"""pages/pg_settings.py — Settings page exact UI"""
import streamlit as st
import os

def render():
    st.markdown("""
    <div class="main-inner">
      <div class="main-header">
        <div class="main-title">Settings</div>
        <div class="main-sub">Configure your Hospital RAG environment</div>
      </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="content-panel">
      <div class="settings-section">
        <div class="settings-label">API Configuration</div>
        <div class="settings-row"><span>Gemini 2.5 Flash API Key</span></div>
      </div>
    """, unsafe_allow_html=True)
    
    # We put the input directly here
    current = st.session_state.get("api_key", "")
    new_key = st.text_input("Key", value=current, type="password", label_visibility="collapsed")
    if new_key != current:
        st.session_state.api_key = new_key
        os.environ["GOOGLE_API_KEY"] = new_key
        st.cache_resource.clear()

    st.markdown("""
      <div class="settings-section">
        <div class="settings-label">Query Preferences</div>
        <div class="settings-row"><span>Enable conflict detection</span><div class="toggle-pill"></div></div>
        <div class="settings-row"><span>Auto-index on upload</span><div class="toggle-pill off"></div></div>
        <div class="settings-row"><span>Show confidence scores</span><div class="toggle-pill"></div></div>
      </div>
      <div class="settings-section" style="border-bottom:none;">
        <div class="settings-label">Chunk Size</div>
        <div class="settings-row"><span id="chunk-label">512 tokens</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    chunk_size = st.slider("Chunk size", 128, 1024, 512, step=128, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
