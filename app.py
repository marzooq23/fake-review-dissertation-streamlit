import streamlit as st

from src.styles import apply_custom_css, insight_banner, section_divider

st.set_page_config(
    page_title="Fake Review Detection Dissertation",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_css()

st.markdown(
    """
    <div class="hero-card">
      <h1>Fake Review Detection Under Imbalance</h1>
      <p>Understanding the trade-off between data quantity and behavioral intelligence</p>
    </div>
    """,
    unsafe_allow_html=True,
)
section_divider()

st.markdown(
    """
    ### Navigate the dissertation demo
    Use the sidebar pages:
    - `Experiment Comparison`
    - `Review Explorer`
    - `Single Review Demo`
    - `SHAP Analysis`
    - `Notebook Showcase`
    """
)

insight_banner(
    "🔵 Core finding: filtering reduces fake-review prevalence, but behavioral intelligence recovers detection power on the same filtered split.",
    tone="info",
)
