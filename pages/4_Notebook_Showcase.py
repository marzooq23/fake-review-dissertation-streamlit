import os
import sys
from typing import List, Dict

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.styles import apply_custom_css, section_divider, insight_banner

st.set_page_config(page_title="4. Behind the Scenes", page_icon="⚙️", layout="wide")
apply_custom_css()

st.markdown('<div class="hero-card"><h1>⚙️ 4. Behind the Scenes (Code)</h1><p>Curious about the math and programming underneath? Explore our original developer notebooks.</p></div>', unsafe_allow_html=True)
section_divider()

insight_banner("This section is meant for developers and data scientists. It contains raw Python code, complex visualizations, and the step-by-step pipeline we used to build this project.", tone="info")

notebooks: List[Dict[str, str]] = [
    {
        "title": "Data Cleaning & Filtering",
        "description": "How we discovered that cleaning data accidentally removes obvious fake reviews.",
        "path": "artefacts/tradeoff_analysis (1).ipynb",
    },
    {
        "title": "Behavior Math & Explanations",
        "description": "How we wrote the formulas to catch suspicious user behavior and prove it works.",
        "path": "artefacts/SHAP__analysis.ipynb",
    },
    {
        "title": "Building Model 1",
        "description": "Training the baseline AI on raw, messy data.",
        "path": "experiment_A1_modelling (1).ipynb",
    },
    {
        "title": "Building Model 2",
        "description": "Training the AI on clean data but restricting it to only look at text.",
        "path": "experiment_B1_modelling (2).ipynb",
    },
    {
        "title": "Building Model 3",
        "description": "Training the final, smartest AI that uses clean data AND user behavior tracking.",
        "path": "experiment_b2_modelling.ipynb",
    },
]

for item in notebooks:
    title = item["title"]
    desc = item["description"]
    local_path = item["path"]
    exists = os.path.exists(local_path)
    col_a, col_b = st.columns([4, 1])
    with col_a:
        st.markdown(f"<div class='glass-card'><h4>{title}</h4><p>{desc}</p></div>", unsafe_allow_html=True)
    with col_b:
        if exists:
            if st.button("Read Code", key=f"open_{title}", use_container_width=True):
                st.session_state["selected_notebook_path"] = local_path
                st.session_state["selected_notebook_title"] = title
                st.switch_page("pages/5_Notebook_Viewer.py")
        else:
            st.caption(f"Missing File: {local_path}")
