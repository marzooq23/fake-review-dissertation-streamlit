import os
import sys
from typing import Optional, Tuple

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="3. Inside the AI's Brain", page_icon="🧠", layout="wide")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_loader import load_filtered_dataset, load_unfiltered_dataset
from src.styles import apply_custom_css, insight_banner, section_divider

apply_custom_css()

st.markdown('<div class="hero-card"><h1>🧠 3. Inside the AI\'s Brain</h1><p>Understanding exactly <i>why</i> the AI decided a review was fake or real.</p></div>', unsafe_allow_html=True)
section_divider()

# Model Selection
exp_mapping = {
    "Model 3 (Behavior-Smart AI)": "B2",
    "Model 2 (Text-Only AI)": "B1",
    "Model 1 (Raw Data AI)": "A1"
}
selected_option = st.selectbox("Select which AI model you want to inspect", options=list(exp_mapping.keys()))
selected_exp = exp_mapping[selected_option]

@st.cache_data(show_spinner=False)
def load_shap_array(exp: str) -> Optional[np.ndarray]:
    path = f"artefacts/shap_values_{exp.lower()}_lgbm.pkl"
    if os.path.exists(path):
        return joblib.load(path)
    return None

@st.cache_data(show_spinner=False)
def build_from_array(shap_array: np.ndarray, experiment_name: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    feature_name_path = f"experiment_{experiment_name.lower()}/models/feature_names.pkl"
    feature_names = None
    
    if os.path.exists(feature_name_path):
        names = joblib.load(feature_name_path)
        if len(names) == shap_array.shape[1]:
            feature_names = names

    if feature_names is None:
        feature_names = [f"feature_{i}" for i in range(shap_array.shape[1])]

    global_importance = np.abs(shap_array).mean(axis=0)
    global_df_arr = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": global_importance,
            "experiment": experiment_name,
        }
    )

    if experiment_name == "A1":
        base_df = load_unfiltered_dataset()
    else:
        base_df = load_filtered_dataset()
        
    n_rows = min(len(base_df), shap_array.shape[0], 250)
    review_ids = base_df["review_id"].astype(str).iloc[:n_rows].tolist()

    local_records = []
    for i in range(n_rows):
        contrib = pd.DataFrame({"feature": feature_names, "impact": shap_array[i]})
        contrib["abs_impact"] = contrib["impact"].abs()
        top = contrib.sort_values("abs_impact", ascending=False).head(10)
        # Simplify display
        top["direction"] = top["impact"].apply(lambda x: "Strongly suggests Fake" if x > 0 else "Suggests Genuine")
        local_records.append(
            {
                "review_id": review_ids[i],
                "top_contributors": top[["feature", "impact", "direction"]].to_dict("records"),
            }
        )
    local_df_arr = pd.DataFrame(local_records)
    return global_df_arr, local_df_arr

shap_array = load_shap_array(selected_exp)
if shap_array is None:
    st.error(f"Data for {selected_exp} not found.")
    st.stop()
    
global_df, local_df = build_from_array(shap_array, selected_exp)

st.subheader("What the AI looks for overall")
st.caption("These are the most important clues the AI uses constantly across thousands of reviews.")
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

if selected_exp == "B2":
    st.subheader("How much did User Behavior matter?")
    st.caption("Here we filter out everything else to look purely at the user-habit clues we invented (like Burstiness or Rating Deviation).")
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
            insight_banner("🟡 Behavior features are massively important to Model 3. They act as the 'smoking guns' that catch clever spammers.", tone="warning")
        else:
            st.info("No behavior clues found.")

st.subheader("Why the AI flagged this specific review")
if local_df.empty:
    st.info("No specific review explanations found.")
else:
    review_choice = st.selectbox("Pick a specific review ID to peek into the AI's math", options=local_df["review_id"].astype(str).tolist())
    row = local_df[local_df["review_id"].astype(str) == str(review_choice)].iloc[0]
    contrib = pd.DataFrame(row["top_contributors"])
    st.dataframe(contrib.style.format({"impact": "{:.4f}"}), use_container_width=True, hide_index=True)
    insight_banner("🔵 This table breaks down exactly which clues nudged the AI toward classifying this review as Fake or Genuine.", tone="info")
