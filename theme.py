"""theme.py — Clinical design system matching the Hospital RAG mockup."""

_FONTS = "@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');"

DARK = f"""<style>
{_FONTS}

/* ── Reset & base ── */
*,*::before,*::after{{box-sizing:border-box;}}
html,body,[data-testid="stAppViewContainer"],.stApp{{
  font-family:'DM Sans',system-ui,sans-serif!important;
  background:#0A0F14!important;color:#E8F0F7!important;
}}
[data-testid="stMain"]{{background:transparent!important;}}
[data-testid="stMainBlockContainer"]{{padding-top:0!important;}}
.block-container{{padding-top:1.2rem!important;padding-bottom:1rem!important;}}

/* ── Sidebar ── */
[data-testid="stSidebar"]{{
  background:#0A0F14!important;
  border-right:1px solid #1E2D3D!important;
}}
[data-testid="stSidebar"]>div:first-child{{padding:16px 0 12px!important;}}
[data-testid="stSidebar"] *{{color:#7A9BB5!important;}}
[data-testid="stSidebar"] strong{{color:#E8F0F7!important;}}

/* ── Sidebar nav buttons ── */
section[data-testid="stSidebar"] .stButton>button{{
  width:100%!important;text-align:left!important;
  background:transparent!important;
  border:none!important;border-left:2px solid transparent!important;
  border-radius:0!important;
  color:#7A9BB5!important;
  font-size:13px!important;font-weight:400!important;
  padding:7px 16px!important;
  display:flex!important;align-items:center!important;gap:8px!important;
  transition:background .15s,color .15s!important;
  box-shadow:none!important;
}}
section[data-testid="stSidebar"] .stButton>button:hover{{
  background:#111820!important;color:#4DB8FF!important;
}}
section[data-testid="stSidebar"] .stButton>button[kind="primary"]{{
  background:#111820!important;
  border-left-color:#4DB8FF!important;
  color:#4DB8FF!important;font-weight:500!important;
}}

/* ── Profile section buttons (dept chips + apply/clear) ── */
.dept-row .stButton>button{{
  border-radius:6px!important;border:1.5px solid #1E2D3D!important;
  background:#111820!important;padding:5px 4px!important;
  font-size:11px!important;font-weight:600!important;
  font-family:'DM Mono',monospace!important;
}}

/* ── Main content buttons ── */
[data-testid="stMain"] .stButton>button{{
  background:#111820!important;border:1px solid #1E2D3D!important;
  border-radius:8px!important;color:#E8F0F7!important;
  font-size:13px!important;font-weight:500!important;
  padding:9px 14px!important;transition:background .15s!important;
  box-shadow:none!important;
}}
[data-testid="stMain"] .stButton>button:hover{{background:#162030!important;}}
[data-testid="stMain"] .stButton>button[kind="primary"]{{
  background:#4DB8FF!important;color:#0A0F14!important;border-color:#4DB8FF!important;
}}
[data-testid="stMain"] .stButton>button[kind="primary"]:hover{{background:#3aa8ef!important;}}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"]{{
  border-bottom:1px solid #1E2D3D!important;gap:0!important;
}}
[data-testid="stTabs"] button[role="tab"]{{
  font-family:'DM Sans',sans-serif!important;font-size:10px!important;
  font-weight:600!important;letter-spacing:.1em!important;
  text-transform:uppercase!important;color:#7A9BB5!important;
  border-radius:0!important;border:none!important;
  background:transparent!important;padding:.65rem 1.1rem!important;
  transition:color .15s!important;box-shadow:none!important;
}}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{{
  color:#4DB8FF!important;border-bottom:2px solid #4DB8FF!important;
}}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea{{
  background:#111820!important;border:1px solid #1E2D3D!important;
  border-radius:8px!important;color:#E8F0F7!important;
  font-family:'DM Mono',monospace!important;font-size:12px!important;
}}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus{{
  border-color:#4DB8FF!important;box-shadow:0 0 0 2px rgba(77,184,255,.1)!important;
}}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label{{
  color:#3A5468!important;font-size:10px!important;
  text-transform:uppercase!important;letter-spacing:.08em!important;
}}

/* ── Selects / File uploader / Expanders ── */
[data-testid="stSelectbox"]>div>div{{background:#111820!important;border:1px solid #1E2D3D!important;border-radius:6px!important;color:#E8F0F7!important;}}
[data-testid="stFileUploader"]{{background:#111820!important;border:1px dashed #1E2D3D!important;border-radius:8px!important;}}
[data-testid="stExpander"]{{background:#111820!important;border:1px solid #1E2D3D!important;border-radius:8px!important;}}
[data-testid="stExpander"] summary{{color:#7A9BB5!important;font-size:13px!important;}}

/* ── Typography ── */
h1,h2,h3,h4,h5{{color:#E8F0F7!important;}}
p,li,div,span{{color:#E8F0F7!important;}}
.stMarkdown code{{background:#111820!important;color:#4DB8FF!important;border-radius:3px!important;}}
hr{{border-color:#1E2D3D!important;margin:.8rem 0!important;}}

/* ── Custom semantic components ── */
.page-title{{font-size:26px;font-weight:600;letter-spacing:-.02em;color:#E8F0F7;margin:0 0 .2rem;}}
.page-sub{{font-size:13px;color:#7A9BB5;margin-bottom:1.4rem;}}
.section-title{{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#7A9BB5;margin-bottom:.6rem;}}
.sb-logo{{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#4DB8FF;padding:4px 16px 14px;}}
.sb-label{{font-size:10px;letter-spacing:.1em;text-transform:uppercase;padding:10px 16px 4px;font-weight:500;color:#3A5468;display:block;}}
.profile-badge{{display:flex;align-items:center;gap:8px;margin:4px 12px 8px;padding:8px 10px;border-radius:8px;background:#111820;border:1px solid #1E2D3D;}}
.badge-circle{{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#0A0F14;flex-shrink:0;font-family:'DM Mono',monospace;}}
.badge-name{{font-size:12px;font-weight:500;color:#E8F0F7;}}
.badge-sub{{font-size:10px;color:#3A5468;}}

.stat-card{{border-radius:10px;padding:16px 18px;border:1px solid #1E2D3D;border-left-width:3px!important;background:#111820;margin-bottom:0;}}
.stat-value{{font-size:30px;font-weight:500;font-family:'DM Mono',monospace;line-height:1;margin-bottom:6px;}}
.stat-label{{font-size:10px;letter-spacing:.1em;text-transform:uppercase;font-weight:500;color:#7A9BB5;}}
.stat-blue{{border-left-color:#4DB8FF!important;}} .stat-blue .stat-value{{color:#4DB8FF;}}
.stat-green{{border-left-color:#00D68F!important;}} .stat-green .stat-value{{color:#00D68F;}}
.stat-red{{border-left-color:#FF5C5C!important;}} .stat-red .stat-value{{color:#FF5C5C;}}
.stat-amber{{border-left-color:#FFB547!important;}} .stat-amber .stat-value{{color:#FFB547;}}

.content-panel{{border-radius:10px;overflow:hidden;background:#111820;border:1px solid #1E2D3D;margin-bottom:.8rem;}}
.panel-header{{display:flex;align-items:center;justify-content:space-between;padding:10px 16px;border-bottom:1px solid #1E2D3D;}}
.panel-title{{font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#7A9BB5;}}
.empty-state{{padding:24px;font-size:13px;font-style:italic;text-align:center;color:#3A5468;}}
.query-item{{display:flex;align-items:center;justify-content:space-between;padding:10px 16px;font-size:13px;border-bottom:1px solid #162030;color:#E8F0F7;}}
.doc-item{{display:flex;align-items:center;justify-content:space-between;padding:10px 16px;font-size:13px;border-bottom:1px solid #162030;color:#E8F0F7;}}
.doc-badge{{font-size:11px;font-family:'DM Mono',monospace;color:#7A9BB5;}}
.conf-badge{{font-size:10px;padding:2px 8px;border-radius:20px;font-weight:500;background:#162030;color:#7A9BB5;}}

.answer-box{{border-left:3px solid #4DB8FF;background:#111820;border-radius:4px;padding:1.2rem 1.4rem;font-size:.88rem;line-height:1.75;color:#E8F0F7;border:1px solid #1E2D3D;border-left:3px solid #4DB8FF;}}
.conflict-banner{{border-left:3px solid #FF5C5C;background:rgba(255,92,92,.05);border:1px solid rgba(255,92,92,.2);border-left:3px solid #FF5C5C;border-radius:4px;padding:.75rem 1rem;font-size:.85rem;color:#E8F0F7;margin:.5rem 0;}}
.resolution-box{{border-left:3px solid #00D68F;background:rgba(0,214,143,.05);border:1px solid rgba(0,214,143,.2);border-left:3px solid #00D68F;border-radius:4px;padding:.75rem 1rem;font-size:.85rem;color:#E8F0F7;margin:.5rem 0;}}
.tag-high{{font-size:.7rem;font-weight:600;letter-spacing:.05em;padding:2px 8px;border-radius:2px;background:rgba(0,214,143,.12);color:#00D68F;font-family:'DM Mono',monospace;}}
.tag-medium{{font-size:.7rem;font-weight:600;letter-spacing:.05em;padding:2px 8px;border-radius:2px;background:rgba(255,181,71,.12);color:#FFB547;font-family:'DM Mono',monospace;}}
.tag-low{{font-size:.7rem;font-weight:600;letter-spacing:.05em;padding:2px 8px;border-radius:2px;background:rgba(255,92,92,.12);color:#FF5C5C;font-family:'DM Mono',monospace;}}
.card{{background:#111820;border:1px solid #1E2D3D;border-radius:8px;padding:1rem 1.1rem;margin-bottom:.6rem;}}
.card-accent{{border-left:3px solid #4DB8FF!important;}}
.main-btn>button{{background:rgba(77,184,255,.08)!important;border-color:#4DB8FF!important;color:#4DB8FF!important;}}
.sec-btn>button{{background:transparent!important;border-color:#1E2D3D!important;color:#7A9BB5!important;}}

/* ── Metrics ── */
[data-testid="stMetric"] label{{color:#7A9BB5!important;font-size:.68rem!important;text-transform:uppercase!important;letter-spacing:.08em!important;}}
[data-testid="stMetric"] [data-testid="stMetricValue"]{{font-family:'DM Mono',monospace!important;color:#E8F0F7!important;}}

/* ── Hide Streamlit chrome ── */
#MainMenu,footer,header{{visibility:hidden!important;}}
</style>"""

LIGHT = f"""<style>
{_FONTS}

*,*::before,*::after{{box-sizing:border-box;}}
html,body,[data-testid="stAppViewContainer"],.stApp{{
  font-family:'DM Sans',system-ui,sans-serif!important;
  background:#F4F7F9!important;color:#1C2B36!important;
}}
[data-testid="stMain"]{{background:transparent!important;}}
[data-testid="stMainBlockContainer"]{{padding-top:0!important;}}
.block-container{{padding-top:1.2rem!important;padding-bottom:1rem!important;}}

[data-testid="stSidebar"]{{background:#FFFFFF!important;border-right:1px solid #DDE4EA!important;}}
[data-testid="stSidebar"]>div:first-child{{padding:16px 0 12px!important;}}
[data-testid="stSidebar"] *{{color:#607080!important;}}
[data-testid="stSidebar"] strong{{color:#1C2B36!important;}}

section[data-testid="stSidebar"] .stButton>button{{
  width:100%!important;text-align:left!important;background:transparent!important;
  border:none!important;border-left:2px solid transparent!important;border-radius:0!important;
  color:#607080!important;font-size:13px!important;font-weight:400!important;
  padding:7px 16px!important;transition:background .15s,color .15s!important;box-shadow:none!important;
}}
section[data-testid="stSidebar"] .stButton>button:hover{{background:#F4F7F9!important;color:#1A6FA8!important;}}
section[data-testid="stSidebar"] .stButton>button[kind="primary"]{{
  background:#F0F7FF!important;border-left-color:#1A6FA8!important;color:#1A6FA8!important;font-weight:500!important;
}}

[data-testid="stMain"] .stButton>button{{
  background:#FFFFFF!important;border:1px solid #DDE4EA!important;border-radius:8px!important;
  color:#1C2B36!important;font-size:13px!important;font-weight:500!important;
  padding:9px 14px!important;transition:background .15s!important;box-shadow:none!important;
}}
[data-testid="stMain"] .stButton>button:hover{{background:#F4F7F9!important;}}
[data-testid="stMain"] .stButton>button[kind="primary"]{{background:#1A6FA8!important;color:#fff!important;border-color:#1A6FA8!important;}}
[data-testid="stMain"] .stButton>button[kind="primary"]:hover{{background:#155d90!important;}}

[data-testid="stTabs"] [role="tablist"]{{border-bottom:1px solid #DDE4EA!important;gap:0!important;}}
[data-testid="stTabs"] button[role="tab"]{{
  font-family:'DM Sans',sans-serif!important;font-size:10px!important;font-weight:600!important;
  letter-spacing:.1em!important;text-transform:uppercase!important;color:#607080!important;
  border-radius:0!important;border:none!important;background:transparent!important;
  padding:.65rem 1.1rem!important;box-shadow:none!important;
}}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{{color:#1A6FA8!important;border-bottom:2px solid #1A6FA8!important;}}

[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{{
  background:#FFFFFF!important;border:1px solid #DDE4EA!important;border-radius:8px!important;
  color:#1C2B36!important;font-family:'DM Mono',monospace!important;font-size:12px!important;
}}
[data-testid="stTextInput"] input:focus,[data-testid="stTextArea"] textarea:focus{{border-color:#1A6FA8!important;box-shadow:0 0 0 2px rgba(26,111,168,.08)!important;}}
[data-testid="stTextInput"] label,[data-testid="stTextArea"] label{{color:#607080!important;font-size:10px!important;text-transform:uppercase!important;letter-spacing:.08em!important;}}

[data-testid="stSelectbox"]>div>div{{background:#FFFFFF!important;border:1px solid #DDE4EA!important;border-radius:6px!important;color:#1C2B36!important;}}
[data-testid="stFileUploader"]{{background:#FFFFFF!important;border:1px dashed #DDE4EA!important;border-radius:8px!important;}}
[data-testid="stExpander"]{{background:#FFFFFF!important;border:1px solid #DDE4EA!important;border-radius:8px!important;}}
[data-testid="stExpander"] summary{{color:#607080!important;font-size:13px!important;}}

h1,h2,h3,h4,h5{{color:#1C2B36!important;}}
p,li,div,span{{color:#1C2B36!important;}}
.stMarkdown code{{background:rgba(26,111,168,.06)!important;color:#1A6FA8!important;border-radius:3px!important;}}
hr{{border-color:#DDE4EA!important;margin:.8rem 0!important;}}

.page-title{{font-size:26px;font-weight:600;letter-spacing:-.02em;color:#1C2B36;margin:0 0 .2rem;}}
.page-sub{{font-size:13px;color:#607080;margin-bottom:1.4rem;}}
.section-title{{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#607080;margin-bottom:.6rem;}}
.sb-logo{{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#1A6FA8;padding:4px 16px 14px;}}
.sb-label{{font-size:10px;letter-spacing:.1em;text-transform:uppercase;padding:10px 16px 4px;font-weight:500;color:#A0B4C0;display:block;}}
.profile-badge{{display:flex;align-items:center;gap:8px;margin:4px 12px 8px;padding:8px 10px;border-radius:8px;background:#F4F7F9;border:1px solid #DDE4EA;}}
.badge-circle{{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#fff;flex-shrink:0;font-family:'DM Mono',monospace;}}
.badge-name{{font-size:12px;font-weight:500;color:#1C2B36;}}
.badge-sub{{font-size:10px;color:#A0B4C0;}}

.stat-card{{border-radius:10px;padding:16px 18px;border:1px solid #DDE4EA;border-left-width:3px!important;background:#FFFFFF;margin-bottom:0;}}
.stat-value{{font-size:30px;font-weight:500;font-family:'DM Mono',monospace;line-height:1;margin-bottom:6px;}}
.stat-label{{font-size:10px;letter-spacing:.1em;text-transform:uppercase;font-weight:500;color:#607080;}}
.stat-blue{{border-left-color:#1A6FA8!important;}} .stat-blue .stat-value{{color:#1A6FA8;}}
.stat-green{{border-left-color:#2E9E6B!important;}} .stat-green .stat-value{{color:#2E9E6B;}}
.stat-red{{border-left-color:#D94F3D!important;}} .stat-red .stat-value{{color:#D94F3D;}}
.stat-amber{{border-left-color:#E09B2D!important;}} .stat-amber .stat-value{{color:#E09B2D;}}

.content-panel{{border-radius:10px;overflow:hidden;background:#FFFFFF;border:1px solid #DDE4EA;margin-bottom:.8rem;}}
.panel-header{{display:flex;align-items:center;justify-content:space-between;padding:10px 16px;border-bottom:1px solid #DDE4EA;}}
.panel-title{{font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#607080;}}
.empty-state{{padding:24px;font-size:13px;font-style:italic;text-align:center;color:#A0B4C0;}}
.query-item{{display:flex;align-items:center;justify-content:space-between;padding:10px 16px;font-size:13px;border-bottom:1px solid #F4F7F9;color:#1C2B36;}}
.doc-item{{display:flex;align-items:center;justify-content:space-between;padding:10px 16px;font-size:13px;border-bottom:1px solid #F4F7F9;color:#1C2B36;}}
.doc-badge{{font-size:11px;font-family:'DM Mono',monospace;color:#607080;}}
.conf-badge{{font-size:10px;padding:2px 8px;border-radius:20px;font-weight:500;background:#F4F7F9;color:#607080;}}

.answer-box{{border:1px solid #DDE4EA;border-left:3px solid #1A6FA8;border-radius:4px;padding:1.2rem 1.4rem;font-size:.88rem;line-height:1.75;color:#1C2B36;background:#FFFFFF;}}
.conflict-banner{{border:1px solid rgba(217,79,61,.2);border-left:3px solid #D94F3D;border-radius:4px;background:rgba(217,79,61,.04);padding:.75rem 1rem;font-size:.85rem;color:#1C2B36;margin:.5rem 0;}}
.resolution-box{{border:1px solid rgba(46,158,107,.2);border-left:3px solid #2E9E6B;border-radius:4px;background:rgba(46,158,107,.04);padding:.75rem 1rem;font-size:.85rem;color:#1C2B36;margin:.5rem 0;}}
.tag-high{{font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:2px;background:rgba(46,158,107,.1);color:#2E9E6B;font-family:'DM Mono',monospace;}}
.tag-medium{{font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:2px;background:rgba(224,155,45,.1);color:#E09B2D;font-family:'DM Mono',monospace;}}
.tag-low{{font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:2px;background:rgba(217,79,61,.1);color:#D94F3D;font-family:'DM Mono',monospace;}}
.card{{background:#FFFFFF;border:1px solid #DDE4EA;border-radius:8px;padding:1rem 1.1rem;margin-bottom:.6rem;}}
.card-accent{{border-left:3px solid #1A6FA8!important;}}
.main-btn>button{{background:rgba(26,111,168,.06)!important;border-color:#1A6FA8!important;color:#1A6FA8!important;}}
.sec-btn>button{{background:transparent!important;border-color:#DDE4EA!important;color:#607080!important;}}

[data-testid="stMetric"] label{{color:#607080!important;font-size:.68rem!important;text-transform:uppercase!important;letter-spacing:.08em!important;}}
[data-testid="stMetric"] [data-testid="stMetricValue"]{{font-family:'DM Mono',monospace!important;color:#1C2B36!important;}}
#MainMenu,footer,header{{visibility:hidden!important;}}
</style>"""


def inject(theme: str) -> str:
    return DARK if theme == "dark" else LIGHT
