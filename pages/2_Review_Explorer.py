import os
import sys
import streamlit as st
import pandas as pd

st.set_page_config(page_title="2. Interactive Review Explorer", page_icon="🔍", layout="wide")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_loader import (
    load_filtered_dataset,
    load_experiment_assets,
    load_optional_analysis_artifacts,
    predict_df,
    readable_behavioral_signals,
    load_unfiltered_dataset,
)
from src.styles import apply_custom_css, insight_banner, section_divider

apply_custom_css()
st.markdown('<div class="hero-card"><h1>🔍 2. Interactive Review Explorer</h1><p>See how reading the text isn\'t enough, but looking at user habits catches the spam.</p></div>', unsafe_allow_html=True)
st.caption("Valid per-review comparison: Model 2 (Text-Only) vs Model 3 (Behavior-Smart) only (same clean dataset).")
section_divider()

b_df = load_filtered_dataset()
b1_assets = load_experiment_assets("B1")
b2_assets = load_experiment_assets("B2")
b2_assets["vectorizer"] = b1_assets["vectorizer"]
analysis = load_optional_analysis_artifacts()
interesting = analysis["interesting_reviews"]

if interesting is None:
    if "prediction_b1" not in b_df.columns or "prediction_b2" not in b_df.columns:
        st.error("Missing precomputed interesting review artefact and model predictions in filtered dataset.")
        st.stop()
tricky = b_df[(b_df["label"] == 1) & (b_df["prediction_b1"] == 0) & (b_df["prediction_b2"] == 1)].head(150).copy()
normal_genuine = b_df[(b_df["label"] == 0) & (b_df["prediction_b2"] == 0)].head(100).copy()
interesting = pd.concat([tricky, normal_genuine]).sample(frac=1, random_state=42).copy()

interesting["select_label"] = interesting.apply(
    lambda r: f"{'🚨 TRICKY FAKE' if r['label'] == 1 else '✅ GENUINE'} | Review {r['review_id']} | User {r['reviewer_id']} -> {str(r['text'])[:60]}...",
    axis=1,
)
selected_label = st.selectbox("Select a review to analyze", options=interesting["select_label"].tolist())
row = interesting[interesting["select_label"] == selected_label].iloc[0]

st.header("Review Details")
st.markdown(f"<div class='glass-card'><p>{row['text']}</p></div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("Review ID", str(row["review_id"]))
c2.metric("Star Rating", int(row["rating"]))
c3.metric("True Reality", "Fake" if int(row["label"]) == 1 else "Genuine")

st.header("How the Models Voted")
l, r = st.columns(2)

row_df = b_df[b_df["review_id"] == row["review_id"]].copy().head(1)
pred_b1, prob_b1 = predict_df(row_df, b1_assets, include_behavioral=False, model_key="lgbm")
pred_b2, prob_b2 = predict_df(row_df, b2_assets, include_behavioral=True, model_key="lgbm")

with l:
    st.subheader("Model 2: Text-Only AI")
    pred_text_b1 = "🔴 Fake" if int(pred_b1[0]) == 1 else "🟢 Genuine"
    st.metric("Prediction", pred_text_b1, f"{float(prob_b1[0])*100:.1f}% confident it's fake")
with r:
    st.subheader("Model 3: Behavior-Smart AI")
    pred_text_b2 = "🔴 Fake" if int(pred_b2[0]) == 1 else "🟢 Genuine"
    st.metric("Prediction", pred_text_b2, f"{float(prob_b2[0])*100:.1f}% confident it's fake")

if int(pred_b1[0]) != int(pred_b2[0]):
    insight_banner("⚠️ Model disagreement: The Text-Only AI was fooled, but looking at user behavior changed the final decision.", tone="warning")
else:
    insight_banner("✅ Both models agree on this review.", tone="success")

st.header("Top Behavioral Habits that tipped off the Smart AI")
idx_to_use = row_df["b2_index"].iloc[0] if "b2_index" in row_df.columns else row_df.index[0]
signals = readable_behavioral_signals(b2_assets["behavioral"].loc[idx_to_use], top_n=8)
for idx, (title, value, text) in enumerate(signals, start=1):
    st.markdown(
        f"<div class='signal-panel'><b>{idx}. {title}</b>: {value:.3f}<br/>{text}</div>",
        unsafe_allow_html=True,
    )

st.header("Other Reviews by this User (For Context)")
full_df = load_unfiltered_dataset()
ctx = full_df[(full_df["reviewer_id"] == row["reviewer_id"]) & (full_df["review_id"] != row["review_id"])].head(5)

if ctx.empty:
    st.info("No other reviews found for this user in the dataset.")
else:
    for _, rr in ctx.iterrows():
        with st.expander(f"Another Review | Rating {int(rr['rating'])}"):
            st.markdown(f"<div class='glass-card'><p>{rr['text']}</p></div>", unsafe_allow_html=True)
