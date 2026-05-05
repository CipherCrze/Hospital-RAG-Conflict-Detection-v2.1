"""theme.py — Exact UI CSS applied to Streamlit"""

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Hide Streamlit Chrome & Set Background ── */
#MainMenu, header, footer { visibility: hidden !important; }
[data-testid="collapsedControl"] { display: none !important; }
.block-container { padding-top: 1rem !important; padding-bottom: 0 !important; max-width: 1200px !important; }
html, body, [data-testid="stAppViewContainer"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background: #0A0F14 !important;
    color: #E8F0F7 !important;
}
[data-testid="stSidebar"] {
    background: #0A0F14 !important;
    border-right: 1px solid #1E2D3D !important;
    width: 260px !important;
}

/* ── Exact CSS from User ── */
.app { font-family: 'DM Sans', sans-serif; display: flex; height: 680px; overflow: hidden; border-radius: 12px; border: 0.5px solid #1E2D3D; background: #0A0F14; color: #E8F0F7; }

/* Sidebar */
.sidebar-logo { padding: 4px 16px 16px; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #4DB8FF; }
.sidebar-nav { display: flex; flex-direction: column; }
.sidebar-nav-item { display: flex; align-items: center; gap: 8px; padding: 7px 16px; font-size: 13px; text-decoration: none; cursor: pointer; border-left: 2px solid transparent; transition: background 0.15s; color: #7A9BB5; }
.sidebar-nav-item.active, .sidebar-nav-item:hover { background: #111820; color: #4DB8FF; }
.sidebar-nav-item.active { border-left-color: #4DB8FF; }
.nav-icon { width: 14px; height: 14px; flex-shrink: 0; }

.section-label { font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; padding: 12px 16px 4px; font-weight: 500; color: #3A5468; }
.profile-badge { display: flex; align-items: center; gap: 8px; margin: 8px 12px; padding: 8px 10px; border-radius: 8px; background: #111820; border: 1px solid #1E2D3D; color: #4DB8FF; }
.badge-initials { width: 28px; height: 28px; border-radius: 50%; background: #4DB8FF; color: #0A0F14; font-size: 11px; font-weight: 600; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.badge-name { font-size: 12px; font-weight: 500; color: #E8F0F7; }
.badge-sub { font-size: 10px; opacity: 0.6; color: #7A9BB5; }

.dept-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px; padding: 4px 12px 8px; }
.dept-btn { border-radius: 6px; padding: 5px 4px; cursor: pointer; text-align: center; transition: background 0.15s; background: #111820; border: 1.5px solid #1E2D3D; color: #7A9BB5; }
.dept-btn:hover { background: #162030; }
.dept-btn.empty { opacity: 0.15; pointer-events: none; border-color: transparent; }
.dept-code { font-size: 11px; font-weight: 600; font-family: 'DM Mono', monospace; }
.dept-name { font-size: 9px; opacity: 0.7; margin-top: 1px; }

.dept-btn.ed { border-color: #D94F3D !important; } .dept-btn.ed .dept-code { color: #D94F3D; }
.dept-btn.fn { border-color: #607080 !important; } .dept-btn.fn .dept-code { color: #7A9BB5; }
.dept-btn.ad { border-color: #7B5EA7 !important; } .dept-btn.ad .dept-code { color: #A67FD4; }
.dept-btn.ad.active { background: rgba(123,94,167,0.15) !important; }
.dept-btn.qx { border-color: #2E9E6B !important; } .dept-btn.qx .dept-code { color: #2E9E6B; }
.dept-btn.ic { border-color: #E09B2D !important; } .dept-btn.ic .dept-code { color: #E09B2D; }
.dept-btn.sg { border-color: #4DB8FF !important; } .dept-btn.sg .dept-code { color: #4DB8FF; }

.api-section { padding: 8px 12px; }
.api-label { font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px; color: #7A9BB5; font-weight: 500; }
.api-input { width: 100%; padding: 6px 8px; border-radius: 6px; font-size: 12px; font-family: 'DM Mono', monospace; outline: none; background: #111820; border: 1px solid #1E2D3D; color: #E8F0F7; }

/* Main Area */
.main-inner { padding: 12px 16px; }
.main-header { margin-bottom: 24px; }
.main-title { font-size: 26px; font-weight: 600; letter-spacing: -0.02em; color: #E8F0F7; }
.main-sub { font-size: 13px; margin-top: 3px; color: #7A9BB5; }

.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 28px; }
.stat-card { border-radius: 10px; padding: 16px 18px; border-left-width: 3px; border-left-style: solid; background: #111820; border-top: 1px solid #1E2D3D; border-right: 1px solid #1E2D3D; border-bottom: 1px solid #1E2D3D; }
.stat-value { font-size: 30px; font-weight: 500; font-family: 'DM Mono', monospace; line-height: 1; margin-bottom: 6px; }
.stat-label { font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 500; color: #7A9BB5; }
.stat-card.chunks { border-left-color: #4DB8FF; } .stat-card.chunks .stat-value { color: #4DB8FF; }
.stat-card.queries { border-left-color: #00D68F; } .stat-card.queries .stat-value { color: #00D68F; }
.stat-card.conflicts { border-left-color: #FF5C5C; } .stat-card.conflicts .stat-value { color: #FF5C5C; }
.stat-card.confidence { border-left-color: #FFB547; } .stat-card.confidence .stat-value { color: #FFB547; }

.bottom-grid { display: grid; grid-template-columns: 1fr 260px; gap: 20px; }
.section-title { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px; color: #7A9BB5; }
.empty-state { padding: 24px; border-radius: 8px; font-size: 13px; font-style: italic; text-align: center; color: #3A5468; border: 1px solid #1E2D3D; background: #111820; }
.action-btn { display: block; width: 100%; padding: 10px 14px; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 500; text-align: left; margin-bottom: 6px; transition: background 0.15s; font-family: 'DM Sans', sans-serif; background: #111820; border: 1px solid #1E2D3D; color: #E8F0F7; }
.action-btn:hover { background: #162030; }

.active-profile-card { border-radius: 8px; padding: 12px 14px; margin-top: 12px; background: #111820; border: 1px solid #1E2D3D; }
.active-profile-name { font-size: 13px; font-weight: 600; color: #E8F0F7; }
.active-profile-sub { font-size: 11px; margin-top: 2px; color: #7A9BB5; }
.active-indicator { display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #00D68F; margin-right: 6px; vertical-align: middle; }

.content-panel { border-radius: 10px; overflow: hidden; background: #111820; border: 1px solid #1E2D3D; }
.panel-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid #1E2D3D; }
.panel-title { font-size: 10px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #7A9BB5; }

.query-form { padding: 16px; display: flex; flex-direction: column; gap: 10px; }
.query-textarea { width: 100%; padding: 10px 12px; border-radius: 8px; font-size: 13px; font-family: 'DM Sans', sans-serif; resize: none; outline: none; height: 80px; background: #0A0F14; border: 1px solid #1E2D3D; color: #E8F0F7; }
.query-submit { padding: 9px 16px; border-radius: 8px; background: #4DB8FF; color: #0A0F14; border: none; font-size: 13px; font-weight: 500; cursor: pointer; font-family: 'DM Sans', sans-serif; align-self: flex-end; }
.query-item { display: flex; align-items: center; justify-content: space-between; padding: 10px 16px; font-size: 13px; cursor: pointer; border-bottom: 1px solid #162030; color: #E8F0F7; }
.query-item:hover { background: #162030; }
.query-badge { font-size: 10px; padding: 2px 8px; border-radius: 20px; font-weight: 500; background: #162030; color: #7A9BB5; }
.doc-item { display: flex; align-items: center; justify-content: space-between; padding: 10px 16px; font-size: 13px; cursor: pointer; border-bottom: 1px solid #162030; color: #E8F0F7; }
.doc-item:hover { background: #162030; }
.doc-badge { font-size: 11px; font-family: 'DM Mono', monospace; color: #7A9BB5; }

.settings-section { padding: 14px 16px; border-bottom: 1px solid #1E2D3D; }
.settings-label { font-size: 11px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; color: #7A9BB5; }
.settings-input { width: 100%; padding: 7px 10px; border-radius: 6px; font-size: 13px; font-family: 'DM Sans', sans-serif; outline: none; margin-top: 4px; background: #0A0F14; border: 1px solid #1E2D3D; color: #E8F0F7; }
.settings-row { display: flex; align-items: center; justify-content: space-between; padding: 8px 0; font-size: 13px; color: #E8F0F7; }
.toggle-pill { width: 36px; height: 20px; border-radius: 10px; background: #00D68F; cursor: pointer; position: relative; flex-shrink: 0; transition: background 0.2s; display: inline-block; }
.toggle-pill::after { content: ''; position: absolute; width: 14px; height: 14px; border-radius: 50%; background: #fff; top: 3px; right: 3px; transition: left 0.2s, right 0.2s; }
.toggle-pill.off { background: #1E2D3D; }
.toggle-pill.off::after { right: auto; left: 3px; }

/* ── Streamlit Overlays (Make native elements invisible over our UI) ── */
.invisible-btn button {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    opacity: 0 !important;
    cursor: pointer !important;
    z-index: 10 !important;
}
.click-wrapper {
    position: relative;
    display: block;
}
.stTextInput input, .stTextArea textarea {
    background: #111820 !important; border: 1px solid #1E2D3D !important;
    border-radius: 8px !important; color: #E8F0F7 !important;
    font-size: 13px !important; font-family: 'DM Sans', sans-serif !important;
}
.stButton>button {
    background: #111820 !important; border: 1px solid #1E2D3D !important;
    border-radius: 8px !important; color: #E8F0F7 !important;
    font-size: 13px !important; font-family: 'DM Sans', sans-serif !important;
}
.stButton>button[kind="primary"] {
    background: #4DB8FF !important; color: #0A0F14 !important; border: none !important;
    font-weight: 500 !important;
}

/* Modern polish and document workspace */
:root {
    --hrag-bg: #071017;
    --hrag-surface: #0f1923;
    --hrag-surface-2: #121f2c;
    --hrag-border: #223244;
    --hrag-text: #E8F0F7;
    --hrag-muted: #86A4BB;
    --hrag-dim: #4E687D;
    --hrag-accent: #4DB8FF;
    --hrag-green: #00D68F;
    --hrag-red: #FF5C5C;
    --hrag-amber: #FFB547;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
    background:
        radial-gradient(circle at top right, rgba(77,184,255,0.09), transparent 34rem),
        linear-gradient(180deg, #071017 0%, #0A0F14 60%, #071017 100%) !important;
}

.block-container {
    padding: 1.4rem 1.8rem 2rem !important;
    max-width: 1280px !important;
}

[data-testid="stSidebar"] {
    background: rgba(7,16,23,0.96) !important;
    box-shadow: 12px 0 30px rgba(0,0,0,0.18) !important;
}

.sidebar-logo {
    font-size: 13px;
    color: var(--hrag-accent);
}

.sidebar-nav-item,
.profile-badge,
.dept-btn,
.content-panel,
.stat-card,
.action-btn,
.active-profile-card {
    box-shadow: 0 12px 28px rgba(0,0,0,0.16);
}

.sidebar-nav-item {
    margin: 1px 10px;
    border-radius: 8px;
    border-left: 0;
    padding: 9px 12px;
}

.sidebar-nav-item.active {
    border-left-color: transparent;
    background: rgba(77,184,255,0.12);
}

.dept-btn.active {
    background: rgba(77,184,255,0.10) !important;
}

.main-inner {
    padding: 20px 24px 32px;
}

.main-title {
    font-size: 30px;
}

.main-sub,
.panel-meta,
.doc-meta,
.inline-hint,
.upload-copy {
    color: var(--hrag-muted);
}

.content-panel,
.stat-card,
.active-profile-card,
.profile-badge,
.dept-btn,
.action-btn {
    background: linear-gradient(180deg, rgba(18,31,44,0.96), rgba(12,22,31,0.98));
    border-color: var(--hrag-border);
}

.stat-card {
    min-height: 104px;
}

.panel-header {
    background: rgba(7,16,23,0.32);
}

.panel-meta {
    font-size: 12px;
    font-family: 'DM Mono', monospace;
}

.doc-workspace,
.tips-list,
.suggestion-list {
    display: flex;
    flex-direction: column;
}

.upload-panel {
    margin-bottom: 10px;
}

.upload-copy {
    padding: 14px 16px 16px;
    font-size: 13px;
    line-height: 1.55;
}

[data-testid="stFileUploader"] {
    background: rgba(18,31,44,0.72);
    border: 1px dashed var(--hrag-border);
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 10px;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--hrag-accent);
}

[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: 0 !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] div {
    color: var(--hrag-muted) !important;
}

.upload-summary {
    border: 1px solid rgba(77,184,255,0.22);
    background: rgba(77,184,255,0.08);
    border-radius: 8px;
    color: var(--hrag-accent);
    font-size: 12px;
    line-height: 1.45;
    padding: 9px 11px;
    margin: 2px 0 10px;
}

.inline-hint {
    font-size: 12px;
    line-height: 1.45;
    padding-top: 9px;
}

.doc-table {
    margin-top: 16px;
}

.modern-doc-item {
    gap: 16px;
    min-height: 58px;
}

.doc-name {
    color: var(--hrag-text);
    font-size: 13px;
    font-weight: 600;
    line-height: 1.35;
}

.doc-meta {
    font-size: 11px;
    line-height: 1.5;
    margin-top: 2px;
}

.tips-panel,
.suggestion-panel {
    margin-bottom: 16px;
}

.tips-list {
    gap: 8px;
    padding: 12px;
}

.tip-card {
    display: grid;
    grid-template-columns: 26px 1fr;
    gap: 10px;
    align-items: start;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid rgba(77,184,255,0.14);
    background: rgba(7,16,23,0.36);
    color: var(--hrag-text);
    font-size: 12px;
    line-height: 1.5;
}

.tip-index {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(77,184,255,0.14);
    color: var(--hrag-accent);
    font-family: 'DM Mono', monospace;
    font-size: 11px;
}

.suggestion-list {
    padding: 10px 12px 12px;
    gap: 8px;
}

.suggestion-item {
    border-radius: 8px;
    background: rgba(0,214,143,0.06);
    border: 1px solid rgba(0,214,143,0.13);
    color: var(--hrag-text);
    font-size: 12px;
    line-height: 1.45;
    padding: 10px 11px;
}

@media (max-width: 900px) {
    .stats-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .bottom-grid {
        grid-template-columns: 1fr;
    }
    .main-inner {
        padding: 16px 12px 24px;
    }
}
</style>"""

def inject(theme=None):
    return CSS
