import os
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Experiment Comparison", page_icon="📊", layout="wide")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_loader import load_filtered_dataset, load_results_table, load_unfiltered_dataset
from src.styles import apply_custom_css, insight_banner, section_divider

apply_custom_css()
st.markdown('<div class="hero-card"><h1>📊 Experiment Comparison</h1><p>More data does not always mean better fake-review detection.</p></div>', unsafe_allow_html=True)
section_divider()

a1_df = load_unfiltered_dataset()
b_df = load_filtered_dataset()

metrics = pd.concat(
    [load_results_table("A1"), load_results_table("B1"), load_results_table("B2")], ignore_index=True
)
metrics["Experiment"] = metrics["Experiment"].map(
    {"A1": "A1 (Unfiltered)", "B1": "B1 (Filtered)", "B2": "B2 (Filtered + Behavioral)"}
)

fake_a1 = int(a1_df["label"].sum())
fake_b = int(b_df["label"].sum())
removed_fake = fake_a1 - fake_b

st.header("Dataset Composition")
c1, c2, c3 = st.columns(3)
c1.metric("A1 Total Reviews", f"{len(a1_df):,}", f"{(fake_a1 / len(a1_df))*100:.2f}% fake")
c2.metric("B1/B2 Total Reviews", f"{len(b_df):,}", f"{(fake_b / len(b_df))*100:.2f}% fake")
c3.metric("Fake Reviews Removed by Filtering", f"{removed_fake:,}", f"{(removed_fake / fake_a1)*100:.1f}% removed")
insight_banner("📉 Data loss after filtering is substantial, especially for fake reviews.", tone="warning")

st.header("Performance Metrics")
st.dataframe(metrics.style.format({k: "{:.4f}" for k in ["F1 (Fake Class)", "ROC-AUC", "PR-AUC", "Precision", "Recall"]}), use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("Fake-Class F1 Across Experiments")
    fig_f1 = px.bar(
        metrics,
        x="Experiment",
        y="F1 (Fake Class)",
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
    st.subheader("ROC-AUC Across Experiments")
    fig_auc = px.bar(
        metrics,
        x="Experiment",
        y="ROC-AUC",
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

insight_banner("✅ B1 vs B2 is the valid like-for-like comparison (same rows, same split).", tone="success")
insight_banner(
    "🔵 Key takeaway: filtering reduces fake prevalence, while behavioral intelligence recovers detection quality.",
    tone="info",
)

