import streamlit as st


def apply_custom_css():
    st.markdown("""
    <style>
    .stApp {
        background:
            radial-gradient(circle at 10% 20%, rgba(29, 78, 216, 0.16), transparent 30%),
            radial-gradient(circle at 80% 0%, rgba(124, 58, 237, 0.12), transparent 35%),
            linear-gradient(140deg, #050816 0%, #0d1328 42%, #0a1022 100%);
        color: #e9eefb;
    }
    .block-container {
        padding-top: 1.2rem;
        max-width: 1350px;
        animation: fadeIn 0.55s ease-out;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(9, 14, 30, 0.95), rgba(6, 10, 24, 0.88)) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.22);
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(160deg, rgba(15, 23, 42, 0.80), rgba(30, 41, 59, 0.56));
        border: 1px solid rgba(125, 211, 252, 0.30);
        border-radius: 14px;
        padding: 12px 10px;
        box-shadow: 0 8px 30px rgba(2, 6, 23, 0.28);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 26px rgba(14, 165, 233, 0.20);
    }
    [data-testid="stExpander"], .stAlert, div[data-testid="stDataFrame"] {
        background: rgba(15, 23, 42, 0.58) !important;
        border: 1px solid rgba(148, 163, 184, 0.24) !important;
        border-radius: 14px;
    }
    h1, h2, h3 {
        background: linear-gradient(90deg, #a5b4fc, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    p, li, span, div {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #e2e8f0;
    }
    .hero-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.84), rgba(15,23,42,0.62));
        border: 1px solid rgba(125, 211, 252, 0.28);
        border-radius: 18px;
        padding: 1.35rem 1.5rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 14px 36px rgba(2, 6, 23, 0.30);
        animation: slideIn 0.45s ease-out;
    }
    .glass-card {
        background: rgba(15, 23, 42, 0.58);
        border: 1px solid rgba(148, 163, 184, 0.24);
        border-radius: 16px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.7rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(14, 165, 233, 0.16);
    }
    .signal-panel {
        background: linear-gradient(145deg, rgba(30,41,59,0.56), rgba(17,24,39,0.48));
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-left: 3px solid rgba(125, 211, 252, 0.65);
        border-radius: 12px;
        padding: 0.6rem 0.85rem;
        margin-bottom: 0.45rem;
    }
    .insight-banner {
        border-radius: 14px;
        padding: 0.75rem 0.95rem;
        margin: 0.35rem 0 0.7rem 0;
        border: 1px solid transparent;
        font-weight: 600;
    }
    .insight-info { background: rgba(59, 130, 246, 0.12); border-color: rgba(147, 197, 253, 0.30); }
    .insight-success { background: rgba(34, 197, 94, 0.12); border-color: rgba(134, 239, 172, 0.30); }
    .insight-warning { background: rgba(245, 158, 11, 0.12); border-color: rgba(252, 211, 77, 0.32); }
    .insight-danger { background: rgba(239, 68, 68, 0.12); border-color: rgba(252, 165, 165, 0.30); }
    .tag-green { color: #86efac; font-weight: 700; }
    .tag-red { color: #fca5a5; font-weight: 700; }
    .tag-amber { color: #fcd34d; font-weight: 700; }
    .tag-blue { color: #93c5fd; font-weight: 700; }
    .section-divider {
        height: 1px;
        border: 0;
        margin: 0.35rem 0 0.9rem 0;
        background: linear-gradient(90deg, rgba(56, 189, 248, 0.0), rgba(56, 189, 248, 0.48), rgba(56, 189, 248, 0.0));
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(4px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    div[data-baseweb="select"] *, div[data-baseweb="popover"] * {
        color: #e2e8f0 !important;
    }
    /* Keep form fields dark in all states */
    div[data-baseweb="select"] > div {
        background: rgba(15, 23, 42, 0.78) !important;
        border: 1px solid rgba(148, 163, 184, 0.30) !important;
        color: #e2e8f0 !important;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="select"] > div:focus-within {
        background: rgba(30, 58, 138, 0.38) !important;
        border-color: rgba(125, 211, 252, 0.55) !important;
    }
    div[data-baseweb="popover"] > div {
        background: rgba(15, 23, 42, 0.95) !important;
        border: 1px solid rgba(148, 163, 184, 0.30) !important;
    }
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li {
        background: transparent !important;
        color: #e2e8f0 !important;
    }
    div[data-baseweb="popover"] li:hover {
        background: rgba(37, 99, 235, 0.25) !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stNumberInput"] input {
        background: rgba(15, 23, 42, 0.78) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(148, 163, 184, 0.30) !important;
    }
    div[data-testid="stTextInput"] input:hover,
    div[data-testid="stTextArea"] textarea:hover,
    div[data-testid="stNumberInput"] input:hover,
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus,
    div[data-testid="stNumberInput"] input:focus {
        background: rgba(30, 58, 138, 0.32) !important;
        border-color: rgba(125, 211, 252, 0.55) !important;
    }
    /* Notebook showcase and other action buttons */
    div[data-testid="stButton"] > button, div[data-testid="stLinkButton"] > a {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.92), rgba(30, 41, 59, 0.82)) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(148, 163, 184, 0.35) !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 20px rgba(2, 6, 23, 0.30);
        transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
    }
    div[data-testid="stButton"] > button:hover, div[data-testid="stLinkButton"] > a:hover {
        background: linear-gradient(145deg, rgba(30, 58, 138, 0.72), rgba(37, 99, 235, 0.62)) !important;
        border-color: rgba(125, 211, 252, 0.60) !important;
        transform: translateY(-1px);
        box-shadow: 0 12px 24px rgba(30, 64, 175, 0.34);
        color: #f8fafc !important;
    }
    /* Expander headers like Notebook Viewer cells */
    [data-testid="stExpander"] details summary {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.90), rgba(30, 41, 59, 0.78)) !important;
        border: 1px solid rgba(148, 163, 184, 0.30) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stExpander"] details summary:hover {
        background: linear-gradient(145deg, rgba(30, 58, 138, 0.72), rgba(37, 99, 235, 0.60)) !important;
        border-color: rgba(125, 211, 252, 0.55) !important;
        color: #f8fafc !important;
    }
    /* Code section inside notebook cells */
    [data-testid="stCodeBlock"] pre, [data-testid="stCode"] pre {
        background: linear-gradient(160deg, rgba(2, 6, 23, 0.94), rgba(15, 23, 42, 0.92)) !important;
        border: 1px solid rgba(96, 165, 250, 0.38) !important;
        border-radius: 12px !important;
        box-shadow: inset 0 0 0 1px rgba(30, 58, 138, 0.18), 0 10px 24px rgba(2, 6, 23, 0.35);
    }
    [data-testid="stCodeBlock"] pre:hover, [data-testid="stCode"] pre:hover {
        border-color: rgba(125, 211, 252, 0.62) !important;
        box-shadow: inset 0 0 0 1px rgba(37, 99, 235, 0.28), 0 12px 26px rgba(30, 64, 175, 0.22);
    }
    </style>
    """, unsafe_allow_html=True)


def section_divider() -> None:
    st.markdown('<hr class="section-divider" />', unsafe_allow_html=True)


def cinematic_card(title: str, body: str) -> None:
    st.markdown(
        f"<div class='glass-card'><h4>{title}</h4><p>{body}</p></div>",
        unsafe_allow_html=True,
    )


def insight_banner(text: str, tone: str = "info") -> None:
    tone_class = {
        "info": "insight-info",
        "success": "insight-success",
        "warning": "insight-warning",
        "danger": "insight-danger",
    }.get(tone, "insight-info")
    st.markdown(f"<div class='insight-banner {tone_class}'>{text}</div>", unsafe_allow_html=True)
