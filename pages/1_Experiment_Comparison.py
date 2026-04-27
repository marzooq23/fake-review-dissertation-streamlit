import os
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="1. Comparing the AI Models", page_icon="📊", layout="wide")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_loader import load_filtered_dataset, load_results_table, load_unfiltered_dataset
from src.styles import apply_custom_css, insight_banner, section_divider

apply_custom_css()
st.markdown('<div class="hero-card"><h1>📊 1. Comparing the AI Models</h1><p>Simply throwing more data at the problem does not always mean better fake-review detection.</p></div>', unsafe_allow_html=True)
section_divider()

a1_df = load_unfiltered_dataset()
b_df = load_filtered_dataset()

metrics = pd.concat(
    [load_results_table("A1"), load_results_table("B1"), load_results_table("B2")], ignore_index=True
)
metrics["Experiment"] = metrics["Experiment"].map(
    {"A1": "Model 1 (Raw Data)", "B1": "Model 2 (Clean Data, Text-Only)", "B2": "Model 3 (Clean Data + User Behavior)"}
)

# Rename the columns for display to plain english
metrics = metrics.rename(columns={
    "F1 (Fake Class)": "Overall Success Rate",
    "ROC-AUC": "AI Confidence Score",
    "Precision": "Accuracy of Fake Alerts",
    "Recall": "Percentage of Fakes Caught"
})

fake_a1 = int(a1_df["label"].sum())
# The b_df artefact is a 5,000-row sample for demo purposes. 
# We use the true values of the full B dataset here (172,389 total, 4,901 fake).
b_total_reviews = 172389
fake_b = 4901
removed_fake = fake_a1 - fake_b

st.header("Dataset Composition")
c1, c2, c3 = st.columns(3)
c1.metric("Model 1 Total Reviews", f"{len(a1_df):,}", f"{(fake_a1 / len(a1_df))*100:.2f}% fake")
c2.metric("Model 2/3 Total Reviews", f"{b_total_reviews:,}", f"{(fake_b / b_total_reviews)*100:.2f}% fake")
c3.metric("Fake Reviews Removed by Cleaning", f"{removed_fake:,}", f"{(removed_fake / fake_a1)*100:.1f}% removed")
insight_banner("📉 Cleaning the data removes unhelpful reviews, but we actually lose a huge portion of fake reviews in the process.", tone="warning")

st.header("Performance Metrics")
st.dataframe(metrics[["Experiment", "Model", "Overall Success Rate", "AI Confidence Score", "Accuracy of Fake Alerts", "Percentage of Fakes Caught"]].style.format({k: "{:.4f}" for k in ["Overall Success Rate", "AI Confidence Score", "Accuracy of Fake Alerts", "Percentage of Fakes Caught"]}), use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("Success Rate Comparison")
    fig_f1 = px.bar(
        metrics,
        x="Experiment",
        y="Overall Success Rate",
        color="Model",
        barmode="group",
        color_discrete_sequence=["#60a5fa", "#a78bfa"],
        text_auto=".3f",
    )
    fig_f1.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
    )
    st.plotly_chart(fig_f1, use_container_width=True)
with right:
    st.subheader("AI Confidence Score Comparison")
    fig_auc = px.bar(
        metrics,
        x="Experiment",
        y="AI Confidence Score",
        color="Model",
        barmode="group",
        color_discrete_sequence=["#22d3ee", "#34d399"],
        text_auto=".3f",
    )
    fig_auc.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
    )
    st.plotly_chart(fig_auc, use_container_width=True)

insight_banner("✅ Comparing Model 2 to Model 3 is the fairest test because they use the exact same Clean Data.", tone="success")
insight_banner(
    "🔵 Key takeaway: Model 2 struggles because there are fewer fake reviews to learn from. However, Model 3 bounces back and performs great just by looking at user behavior patterns!",
    tone="info",
)
