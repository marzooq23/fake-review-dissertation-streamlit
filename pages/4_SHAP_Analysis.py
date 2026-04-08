import os
import sys
from glob import glob
from typing import Optional, Tuple

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="SHAP Analysis", page_icon="🧠", layout="wide")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_loader import load_filtered_dataset, load_optional_analysis_artifacts, load_unfiltered_dataset
from src.styles import apply_custom_css, insight_banner, section_divider

apply_custom_css()

st.markdown('<div class="hero-card"><h1>🧠 SHAP Analysis</h1><p>Interpreting why B2 improves fake-review detection.</p></div>', unsafe_allow_html=True)
section_divider()

analysis = load_optional_analysis_artifacts()
shap_payload = analysis["shap_values"]

@st.cache_data(show_spinner=False)
def load_b2_shap_array() -> Optional[np.ndarray]:
    candidates = sorted(glob("artefacts/shap_values_b2*.pkl"))
    if not candidates:
        return None
    data = joblib.load(candidates[0])
    if isinstance(data, np.ndarray):
        return data
    return None


@st.cache_data(show_spinner=False)
def build_from_array(shap_array: np.ndarray) -> Tuple[pd.DataFrame, pd.DataFrame]:
    feature_name_paths = {
        "A1": "experiment_a1/models/feature_names.pkl",
        "B1": "experiment_b1/models/feature_names.pkl",
        "B2": "experiment_b2/models/feature_names.pkl",
    }
    feature_names = None
    experiment_name = "Unknown"
    for exp, path in feature_name_paths.items():
        if os.path.exists(path):
            names = joblib.load(path)
            if len(names) == shap_array.shape[1]:
                feature_names = names
                experiment_name = exp
                break

    if feature_names is None:
        # Safe fallback: force aligned lengths to avoid crashes on schema mismatch.
        feature_names = [f"feature_{i}" for i in range(shap_array.shape[1])]
        experiment_name = "Array"

    global_importance = np.abs(shap_array).mean(axis=0)
    global_df_arr = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": global_importance,
            "experiment": experiment_name,
        }
    )

    filtered = load_filtered_dataset()
    if experiment_name == "A1":
        base_df = load_unfiltered_dataset()
    else:
        base_df = filtered
    n_rows = min(len(base_df), shap_array.shape[0], 250)
    review_ids = base_df["review_id"].astype(str).iloc[:n_rows].tolist()

    local_records = []
    for i in range(n_rows):
        contrib = pd.DataFrame({"feature": feature_names, "impact": shap_array[i]})
        contrib["abs_impact"] = contrib["impact"].abs()
        top = contrib.sort_values("abs_impact", ascending=False).head(8)
        top["direction"] = top["impact"].apply(lambda x: "increase fake probability" if x > 0 else "decrease fake probability")
        local_records.append(
            {
                "review_id": review_ids[i],
                "top_contributors": top[["feature", "impact", "direction"]].to_dict("records"),
            }
        )
    local_df_arr = pd.DataFrame(local_records)
    return global_df_arr, local_df_arr

if isinstance(shap_payload, dict):
    global_df = pd.DataFrame(shap_payload.get("global_importance", []))
    local_df = pd.DataFrame(shap_payload.get("local_explanations", []))
elif isinstance(shap_payload, np.ndarray):
    global_df, local_df = build_from_array(shap_payload)
else:
    b2_array = load_b2_shap_array()
    if b2_array is None:
        st.error("Unsupported SHAP artefact format and no compatible `shap_values_b2*.pkl` array was found.")
        st.stop()
    global_df, local_df = build_from_array(b2_array)

if global_df.empty:
    fi_path = "experiment_b2/models/feature_importance.pkl"
    if os.path.exists(fi_path):
        fallback = joblib.load(fi_path)
        global_df = pd.DataFrame({"feature": list(fallback.keys()), "importance": list(fallback.values()), "experiment": "B2"})

st.subheader("Global Feature Importance")
if not global_df.empty:
    show = global_df.sort_values("importance", ascending=False).head(20)
    fig = px.bar(show, x="importance", y="feature", color="experiment", orientation="h", text_auto=".3f")
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis={"categoryorder": "total ascending"},
        legend_title_text="",
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Behavioral Feature Impact")
if not global_df.empty:
    behavior_mask = global_df["feature"].astype(str).str.contains("_r|_p|product_|review_count|burst|similar", regex=True)
    behavior_df = global_df[behavior_mask].sort_values("importance", ascending=False).head(12)
    if not behavior_df.empty:
        fig2 = px.bar(
            behavior_df,
            x="importance",
            y="feature",
            orientation="h",
            color_discrete_sequence=["#f59e0b"],
            text_auto=".3f",
        )
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis={"categoryorder": "total ascending"},
        )
        st.plotly_chart(fig2, use_container_width=True)
        insight_banner("🟡 Behavioral features are highlighted here to show their added value in B2.", tone="warning")
    else:
        st.info("No behavioral ranking entries found in SHAP payload.")

st.subheader("Local Explanation (Per Review)")
if local_df.empty:
    st.info("No local SHAP explanations found in payload.")
else:
    review_choice = st.selectbox("Select review_id", options=local_df["review_id"].astype(str).tolist())
    row = local_df[local_df["review_id"].astype(str) == str(review_choice)].iloc[0]
    contrib = pd.DataFrame(row["top_contributors"])
    st.dataframe(contrib, use_container_width=True, hide_index=True)
    insight_banner("🔵 Local explanations show which signals increase or decrease fake probability for this review.", tone="info")
