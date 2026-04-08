import os
import sys
from typing import List, Dict

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.styles import apply_custom_css, section_divider, insight_banner

st.set_page_config(page_title="Notebook Showcase", page_icon="📚", layout="wide")
apply_custom_css()

st.markdown('<div class="hero-card"><h1>📚 Notebook Showcase</h1><p>End-to-end research pipeline behind the dissertation experiments.</p></div>', unsafe_allow_html=True)
section_divider()

notebooks: List[Dict[str, str]] = [
    {
        "title": "Filtering Strategy",
        "description": "Iterative reviewer/product support filtering",
        "path": "artefacts/tradeoff_analysis (1).ipynb",
    },
    {
        "title": "Behavior & SHAP",
        "description": "Behavioral impact and interpretability analysis",
        "path": "artefacts/SHAP__analysis.ipynb",
    },
    {
        "title": "Model Training (A1)",
        "description": "Unfiltered baseline with TF-IDF + metadata",
        "path": "experiment_A1_modelling (1).ipynb",
    },
    {
        "title": "Model Training (B1)",
        "description": "Filtered baseline without behavioral features",
        "path": "experiment_B1_modelling (2).ipynb",
    },
    {
        "title": "Model Training (B2)",
        "description": "Filtered dataset + behavioral enhancement",
        "path": "experiment_b2_modelling.ipynb",
    },
]

insight_banner("Open Notebook now loads inside the app via Notebook Viewer.", tone="info")

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
            if st.button("Open Notebook", key=f"open_{title}", use_container_width=True):
                st.session_state["selected_notebook_path"] = local_path
                st.session_state["selected_notebook_title"] = title
                st.switch_page("pages/6_Notebook_Viewer.py")
        else:
            st.caption(f"Missing: {local_path}")
