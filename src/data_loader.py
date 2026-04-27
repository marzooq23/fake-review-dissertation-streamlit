import os
from glob import glob
import warnings
from typing import Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
import scipy.sparse as sp
import streamlit as st

warnings.filterwarnings("ignore", category=UserWarning)

META_COLS = ["rating", "review_length", "extreme_rating", "review_month", "review_dayofweek", "is_weekend"]
EXPERIMENT_DIRS = {"A1": "experiment_a1/models", "B1": "experiment_b1/models", "B2": "experiment_b2/models"}
BEHAVIOR_DISPLAY = {
    "max_reviews_per_day_r": ("Burstiness", "Many reviews posted in a short time."),
    "review_count_r": ("Review Frequency", "Account posts reviews very often."),
    "EXRR_r": ("Extreme Rating Ratio", "Ratings skew heavily to 1 or 5 stars."),
    "MCS_r": ("Similarity Score", "Reviewer text style is repetitive."),
    "RPR_r": ("Repetition", "Repeated positive-style review pattern."),
    "AFPPR_r": ("Early Review Ratio", "Many reviews appear early in product lifecycle."),
    "product_rating_std": ("Rating Deviation", "Product receives unusually volatile ratings."),
    "product_review_velocity": ("Product Activity Spike", "Review activity surges in short windows."),
}


def _read_pickle_if_exists(path: str) -> Optional[object]:
    return joblib.load(path) if os.path.exists(path) else None


def _read_first_matching_pickle(patterns: List[str]) -> Optional[object]:
    for pattern in patterns:
        matches = sorted(glob(pattern))
        if matches:
            return joblib.load(matches[0])
    return None


@st.cache_resource(show_spinner=False)
def load_experiment_assets(experiment: str) -> Dict[str, object]:
    base = EXPERIMENT_DIRS[experiment]
    assets: Dict[str, object] = {
        "lr": joblib.load(os.path.join(base, "logistic_regression.pkl")),
        "lgbm": joblib.load(os.path.join(base, "lightgbm.pkl")),
        "thresholds": joblib.load(os.path.join(base, "thresholds.pkl")),
        "meta_scaler": joblib.load(os.path.join(base, "meta_scaler.pkl")),
        "feature_names": joblib.load(os.path.join(base, "feature_names.pkl")),
        "vectorizer": _read_pickle_if_exists(os.path.join(base, "tfidf_vectorizer.pkl")),
        "behav_scaler": _read_pickle_if_exists(os.path.join(base, "behav_scaler.pkl")),
        "behavioral": _read_pickle_if_exists(os.path.join(base, "behavioral_features.pkl")),
    }
    return assets


@st.cache_data(show_spinner=False)
def load_unfiltered_dataset() -> pd.DataFrame:
    try:
        df = pd.read_csv("yelp_nyc_processed_v2.csv")
    except FileNotFoundError:
        # Fallback for Streamlit Cloud where the 474MB CSV is not uploaded
        df = joblib.load("artefacts/unfiltered_dataset_stub.pkl")
    if "rating" not in df.columns and "star_rating" in df.columns:
        df = df.rename(columns={"star_rating": "rating"})
    if "review_id" not in df.columns:
        df["review_id"] = df.index.astype(str)
    return df.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_context_reviews() -> pd.DataFrame:
    return joblib.load("artefacts/context_reviews.pkl")

@st.cache_data(show_spinner=False)
def load_filtered_dataset_v2() -> pd.DataFrame:
    df = joblib.load("artefacts/filtered_dataset.pkl")
    if "rating" not in df.columns and "star_rating" in df.columns:
        df = df.rename(columns={"star_rating": "rating"})
    if "review_id" not in df.columns:
        df["review_id"] = df.index.astype(str)
    return df.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_results_table(experiment: str) -> pd.DataFrame:
    path = f"experiment_{experiment.lower()}/models/results_experiment_{experiment.lower()}.csv"
    frame = pd.read_csv(path).copy()
    frame["Experiment"] = experiment
    frame["Model"] = frame["model"].astype(str).apply(lambda x: "LightGBM" if "lightgbm" in x.lower() else "Logistic Regression")
    frame["F1 (Fake Class)"] = frame["f1_fake"]
    frame["ROC-AUC"] = frame["roc_auc"]
    frame["PR-AUC"] = frame["pr_auc"]
    frame["Precision"] = frame["precision_fake"]
    frame["Recall"] = frame["recall_fake"]
    return frame[["Experiment", "Model", "F1 (Fake Class)", "ROC-AUC", "PR-AUC", "Precision", "Recall"]]


def prepare_features(df: pd.DataFrame, assets: Dict[str, object], include_behavioral: bool) -> sp.csr_matrix:
    X_tfidf = assets["vectorizer"].transform(df["text_clean"].fillna(df["text"]).astype(str))
    X_meta = assets["meta_scaler"].transform(df[META_COLS].values.astype(float))
    mats = [X_tfidf, sp.csr_matrix(X_meta)]
    if include_behavioral:
        tfidf_names = list(assets["vectorizer"].get_feature_names_out())
        behav_cols = [c for c in assets["feature_names"] if c not in tfidf_names + META_COLS]
        idx = df["b2_index"].values if "b2_index" in df.columns else df.index
        X_behav = assets["behavioral"].loc[idx, behav_cols].values
        X_behav = assets["behav_scaler"].transform(X_behav)
        mats.append(sp.csr_matrix(X_behav))
    return sp.hstack(mats, format="csr")


def predict_df(df: pd.DataFrame, assets: Dict[str, object], include_behavioral: bool, model_key: str = "lgbm") -> Tuple[np.ndarray, np.ndarray]:
    X = prepare_features(df, assets, include_behavioral=include_behavioral)
    prob = assets[model_key].predict_proba(X)[:, 1]
    pred = (prob >= assets["thresholds"][model_key]).astype(int)
    return pred, prob


def readable_behavioral_signals(row: pd.Series, top_n: int = 8) -> List[Tuple[str, float, str]]:
    picks: List[Tuple[str, float, str]] = []
    for raw_name, (title, expl) in BEHAVIOR_DISPLAY.items():
        if raw_name in row.index:
            picks.append((title, float(row[raw_name]), expl))
    picks.sort(key=lambda x: abs(x[1]), reverse=True)
    return picks[:top_n]


@st.cache_data(show_spinner=False)
def load_optional_analysis_artifacts() -> Dict[str, Optional[object]]:
    return {
        "shap_values": _read_pickle_if_exists("artefacts/shap_values.pkl")
        or _read_first_matching_pickle(["artefacts/*shap*.pkl", "artefacts/*SHAP*.pkl"]),
        "interesting_reviews": _read_pickle_if_exists("artefacts/interesting_reviews.pkl")
        or _read_first_matching_pickle(["artefacts/*interesting*reviews*.pkl"]),
        "reviewer_history": _read_pickle_if_exists("artefacts/reviewer_history.pkl")
        or _read_first_matching_pickle(["artefacts/*reviewer*history*.pkl"]),
    }

