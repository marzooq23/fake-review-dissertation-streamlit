import streamlit as st
import os
import sys
import pandas as pd

st.set_page_config(page_title="Single Review Demo", page_icon="🧾", layout="wide")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_loader import load_experiment_assets, predict_df
from src.styles import apply_custom_css, insight_banner, section_divider

apply_custom_css()

st.markdown('<div class="hero-card"><h1>🧾 Single Review Demo</h1><p>A1 works for isolated reviews; behavioral models do not.</p></div>', unsafe_allow_html=True)
st.caption("A1 supports isolated reviews. B2 behavioral features require reviewer history and are not applicable here.")
section_divider()

a1_assets = load_experiment_assets("A1")
text = st.text_area("Review text", height=180, value="Great food and very fast service. Highly recommend.")
rating = st.slider("Star rating", min_value=1, max_value=5, value=5)

if st.button("Predict"):
    tmp = pd.DataFrame(
        [{
            "text": text,
            "text_clean": text,
            "rating": float(rating),
            "review_length": float(len(text.split())),
            "extreme_rating": 1.0 if rating in (1, 5) else 0.0,
            "review_month": 1.0,
            "review_dayofweek": 1.0,
            "is_weekend": 0.0,
        }]
    )
    pred, prob = predict_df(tmp, a1_assets, include_behavioral=False, model_key="lgbm")
    label = "🔴 Fake" if int(pred[0]) == 1 else "🟢 Genuine"
    st.metric("Prediction", label, f"P(fake)={float(prob[0]):.3f}")
    insight_banner(
        "Behavioral features require reviewer history and product interaction context, so B2-style models cannot operate on an isolated review.",
        tone="info",
    )
