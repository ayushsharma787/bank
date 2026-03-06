CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── ROOT & BODY ── */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0C1120 !important;
    border-right: 1px solid rgba(212,168,83,0.15) !important;
}
[data-testid="stSidebar"] .stMarkdown h1 {
    font-family: 'Syne', sans-serif !important;
    color: #D4A853 !important;
    font-size: 22px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

/* ── METRIC CARDS ── */
[data-testid="stMetric"] {
    background: #0C1120;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 18px 20px;
    border-top: 2px solid #D4A853;
}
[data-testid="stMetricLabel"] {
    font-size: 10px !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #64748B !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    color: #F0F4FF !important;
}
[data-testid="stMetricDelta"] {
    font-size: 11px !important;
}

/* ── PAGE TITLE ── */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #F0F4FF;
    margin-bottom: 4px;
}
.page-title span { color: #D4A853; font-style: italic; }
.page-subtitle {
    font-size: 12px;
    color: #64748B;
    margin-bottom: 28px;
    letter-spacing: 0.5px;
}
.section-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    background: rgba(212,168,83,0.12);
    color: #D4A853;
    border: 1px solid rgba(212,168,83,0.3);
    margin-bottom: 8px;
}

/* ── DIVIDER ── */
hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    margin: 20px 0;
}

/* ── TABS ── */
[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #64748B;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #D4A853 !important;
    border-bottom-color: #D4A853 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #D4A853, #C4943A) !important;
    color: #050810 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    transition: all 0.2s;
}
.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(212,168,83,0.25) !important;
}

/* ── SLIDERS ── */
.stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
    background: #D4A853 !important;
    color: #050810 !important;
}
.stSlider [role="slider"] { background: #D4A853 !important; }

/* ── SELECT BOXES ── */
.stSelectbox [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border-color: rgba(255,255,255,0.12) !important;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
}

/* ── PREDICTION RESULT BOX ── */
.result-box-approved {
    background: rgba(34,197,94,0.07);
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
}
.result-box-declined {
    background: rgba(100,116,139,0.07);
    border: 1px solid rgba(100,116,139,0.25);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
}
.result-verdict-approved {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #22C55E;
    margin: 0;
}
.result-verdict-declined {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #94A3B8;
    margin: 0;
}
.result-prob {
    font-family: 'Syne', sans-serif;
    font-size: 48px;
    font-weight: 800;
    color: #F0F4FF;
    line-height: 1;
}
.result-label {
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #64748B;
}

/* ── INFO CARDS ── */
.info-card {
    background: #0C1120;
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid #D4A853;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 10px;
    font-size: 12px;
    color: #94A3B8;
    line-height: 1.6;
}
.info-card strong { color: #F0F4FF; }
</style>
"""

def inject_css():
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def metric_row(cols_data: list):
    """cols_data = list of (label, value, delta, delta_color) tuples"""
    import streamlit as st
    cols = st.columns(len(cols_data))
    for col, (label, value, delta, color) in zip(cols, cols_data):
        with col:
            st.metric(label=label, value=value, delta=delta, delta_color=color)
