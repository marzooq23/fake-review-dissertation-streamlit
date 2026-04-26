import json
import os
import sys
from typing import Any, Dict, List

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.styles import apply_custom_css, insight_banner, section_divider

st.set_page_config(page_title="5. Code Viewer", page_icon="📓", layout="wide")
apply_custom_css()

st.markdown(
    '<div class="hero-card"><h1>📓 5. Code Viewer</h1><p>Peek inside the developer files without needing to open programming software.</p></div>',
    unsafe_allow_html=True,
)
section_divider()

path = st.session_state.get("selected_notebook_path")
title = st.session_state.get("selected_notebook_title", "Notebook")

if not path:
    insight_banner("Oh no! You haven't selected a code file yet. Go back to the Behind the Scenes page and pick one.", tone="warning")
    st.page_link("pages/4_Notebook_Showcase.py", label="Take me back to Behind the Scenes", icon="⚙️")
    st.stop()

if not os.path.exists(path):
    st.error(f"Developer file missing: {path}")
    st.stop()


@st.cache_data(show_spinner=False)
def load_notebook(notebook_path: str) -> Dict[str, Any]:
    with open(notebook_path, "r", encoding="utf-8") as f:
        return json.load(f)


nb = load_notebook(path)
cells: List[Dict[str, Any]] = nb.get("cells", [])

insight_banner(f"Currently Reading: {title}", tone="info")
show_code = st.toggle("Show Python Code", value=True)
show_markdown = st.toggle("Show Explanatory Text", value=True)

for idx, cell in enumerate(cells, start=1):
    cell_type = cell.get("cell_type", "")
    source = "".join(cell.get("source", []))
    if not source.strip():
        continue
    if cell_type == "markdown" and not show_markdown:
        continue
    if cell_type == "code" and not show_code:
        continue

    with st.expander(f"Code Block {idx} ({'Text' if cell_type == 'markdown' else 'Code'})", expanded=(idx <= 3)):
        if cell_type == "markdown":
            st.markdown(source)
        elif cell_type == "code":
            st.code(source, language="python")
        else:
            st.text(source)

st.page_link("pages/4_Notebook_Showcase.py", label="Take me back to Behind the Scenes", icon="⬅️")
