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
      <h1>Catching Fake Reviews: The Power of User Behavior</h1>
      <p>Why looking at <i>how</i> people write reviews is better than just looking at <i>what</i> they write, even with less data.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
section_divider()

st.markdown(
    """
    ### Navigate the application
    Use the sidebar pages:
    - `Comparing the AI Models` (formerly Experiment Comparison)
    - `Interactive Review Explorer` (formerly Review Explorer)
    - `Inside the AI's Brain` (formerly SHAP Analysis)
    - `Behind the Scenes (Code)` (formerly Notebook Showcase)
    """
)

insight_banner(
    "🔵 Our Main Discovery: While cleaning up data accidentally removed a lot of obvious fake reviews, looking at user behavior allowed our AI to catch the clever ones anyway.",
    tone="info",
)

