import json
import os
import sys
from typing import Any, Dict, List

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.styles import apply_custom_css, insight_banner, section_divider

st.set_page_config(page_title="Notebook Viewer", page_icon="📓", layout="wide")
apply_custom_css()

st.markdown(
    '<div class="hero-card"><h1>📓 Notebook Viewer</h1><p>Read notebook narrative, code, and outputs directly inside the app.</p></div>',
    unsafe_allow_html=True,
)
section_divider()

path = st.session_state.get("selected_notebook_path")
title = st.session_state.get("selected_notebook_title", "Notebook")

if not path:
    insight_banner("No notebook selected. Please open one from Notebook Showcase.", tone="warning")
    st.page_link("pages/5_Notebook_Showcase.py", label="Go to Notebook Showcase", icon="📚")
    st.stop()

if not os.path.exists(path):
    st.error(f"Notebook file not found: {path}")
    st.stop()


@st.cache_data(show_spinner=False)
def load_notebook(notebook_path: str) -> Dict[str, Any]:
    with open(notebook_path, "r", encoding="utf-8") as f:
        return json.load(f)


nb = load_notebook(path)
cells: List[Dict[str, Any]] = nb.get("cells", [])

insight_banner(f"Viewing: {title} (`{path}`)", tone="info")
show_code = st.toggle("Show code cells", value=True)
show_markdown = st.toggle("Show markdown cells", value=True)

for idx, cell in enumerate(cells, start=1):
    cell_type = cell.get("cell_type", "")
    source = "".join(cell.get("source", []))
    if not source.strip():
        continue
    if cell_type == "markdown" and not show_markdown:
        continue
    if cell_type == "code" and not show_code:
        continue

    with st.expander(f"Cell {idx}: {cell_type}", expanded=(idx <= 3)):
        if cell_type == "markdown":
            st.markdown(source)
        elif cell_type == "code":
            st.code(source, language="python")
        else:
            st.text(source)

st.page_link("pages/5_Notebook_Showcase.py", label="Back to Notebook Showcase", icon="⬅️")
