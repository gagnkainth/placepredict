import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from imblearn.over_sampling import SMOTE
from sklearn.inspection import permutation_importance
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score, f1_score,
                             precision_score, recall_score, roc_auc_score,
                             roc_curve)
from sklearn.model_selection import train_test_split

# --- Page config ---
st.set_page_config(
    page_title="Placement Prediction Analysis",
    page_icon="📈",
    layout="wide",
)

# --- Helper functions ---

@st.cache_data(show_spinner=False)
def load_data():
    """Load raw student responses data and normalize column names."""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Prefer the cleaned CSV from the EDA folder if available, otherwise fall back.
    candidates = [
        os.path.join(base_dir, "student_responses.csv"),
        os.path.join(base_dir, "../preprocessing_eda_kaggledata/students_cleaned_for_eda.csv"),
        os.path.join(base_dir, "../preprocessing_eda_kaggledata/students.csv"),
    ]

    for path in candidates:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    else:
        raise FileNotFoundError("Could not find the student responses CSV data file.")

    # Normalize columns for consistent processing
    df.columns = df.columns.str.strip()
    # Drop non-predictive identifiers if present
    for c in ["Name", "Email", "Roll No", "Timestamp"]:
        if c in df.columns:
            df = df.drop(columns=c)

    return df


@st.cache_data(show_spinner=False)
def load_artifacts():
    """Load saved models and preprocessing artifacts."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts = {}

    try:
        with open(os.path.join(base_dir, "saved_models", "feature_names.pkl"), "rb") as f:
            artifacts["feature_names"] = pd.read_pickle(f)
    except Exception as e:
        raise RuntimeError(f"Unable to load feature names: {e}")

    try:
        with open(os.path.join(base_dir, "saved_models", "scaler.pkl"), "rb") as f:
            artifacts["scaler"] = pd.read_pickle(f)
    except Exception as e:
        raise RuntimeError(f"Unable to load scaler: {e}")

    try:
        with open(os.path.join(base_dir, "saved_models", "all_models.pkl"), "rb") as f:
            artifacts["models"] = pd.read_pickle(f)
    except Exception as e:
        raise RuntimeError(f"Unable to load models: {e}")

    return artifacts


def preprocess_features(df: pd.DataFrame, feature_names):
    """Create model-ready feature matrix aligned to saved feature names."""
    df = df.copy()

    # Target encoding will be handled outside
    X = df.drop(columns=["Placement Status"])

    # Categorical encoding matches training (get_dummies + drop_first)
    X_enc = pd.get_dummies(X, drop_first=True)

    # Ensure we have exactly the same columns the model expects
    for feat in feature_names:
        if feat not in X_enc.columns:
            X_enc[feat] = 0

    X_enc = X_enc[feature_names]
    return X_enc


def _prepare_input_for_model(X, model, feature_names=None):
    """Return an input representation that matches how the model was trained.

    Avoids sklearn feature-name warnings by aligning X to the model's expectations.
    """
    # If model stores feature names, give it a DataFrame with those names
    if hasattr(model, "feature_names_in_") and model.feature_names_in_ is not None:
        if isinstance(X, np.ndarray):
            return pd.DataFrame(X, columns=feature_names or model.feature_names_in_)
        return X

    # Otherwise, give it a numpy array
    if isinstance(X, pd.DataFrame):
        return X.to_numpy()
    return X


def compute_metrics(models, X_test, y_test, feature_names=None):
    results = []
    y_test_encoded = y_test.map({"Not Placed": 0, "Placed": 1})

    for name, model in models.items():
        X_in = _prepare_input_for_model(X_test, model, feature_names=feature_names)

        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_in)[:, 1]
        else:
            y_proba = model.decision_function(X_in)

        y_pred = model.predict(X_in)
        results.append(
            {
                "Model": name,
                "Accuracy": accuracy_score(y_test_encoded, y_pred),
                "Precision": precision_score(
                    y_test_encoded, y_pred, zero_division=0
                ),
                "Recall": recall_score(y_test_encoded, y_pred, zero_division=0),
                "F1 Score": f1_score(
                    y_test_encoded, y_pred, zero_division=0
                ),
                "ROC AUC": roc_auc_score(y_test_encoded, y_proba),
            }
        )

    return pd.DataFrame(results)


def plot_comparison_metrics(result_df: pd.DataFrame):
    """Figure 2: comparison of all models across multiple evaluation metrics."""
    result_df = result_df.melt(
        id_vars=["Model"],
        value_vars=["Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"],
        var_name="Metric",
        value_name="Score",
    )

    fig = px.bar(
        result_df,
        x="Metric",
        y="Score",
        color="Model",
        barmode="group",
        title="Figure 2: Comparison of Model Performance Metrics",
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig.update_layout(template="plotly_dark", height=600)
    return fig


def plot_smote_distribution(y_train, y_train_smote):
    """Figure 1: class distribution before/after SMOTE."""
    before = y_train.value_counts().rename("Before SMOTE")
    after = pd.Series(y_train_smote).value_counts().rename("After SMOTE")

    df_plot = pd.concat([before, after], axis=1).reset_index()
    df_plot.columns = ["Placement Status", "Before SMOTE", "After SMOTE"]

    fig = go.Figure(
        data=[
            go.Bar(
                name="Before SMOTE",
                x=df_plot["Placement Status"],
                y=df_plot["Before SMOTE"],
                marker_color="#EF553B",
            ),
            go.Bar(
                name="After SMOTE",
                x=df_plot["Placement Status"],
                y=df_plot["After SMOTE"],
                marker_color="#00CC96",
            ),
        ]
    )
    fig.update_layout(
        barmode="group",
        title="Figure 1: Class Distribution Before and After SMOTE",
        template="plotly_dark",
        height=500,
    )
    return fig


def plot_confusion_matrix(model, X_test, y_test, feature_names=None):
    """Figure 3: Confusion matrix for best model (SVM)."""
    y_true = y_test.map({"Not Placed": 0, "Placed": 1})
    X_in = _prepare_input_for_model(X_test, model, feature_names=feature_names)
    y_pred = model.predict(X_in)

    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    labels = ["Not Placed", "Placed"]

    fig = go.Figure(
        data=
        go.Heatmap(
            z=cm,
            x=labels,
            y=labels,
            colorscale="Turbo",
            showscale=True,
            hoverongaps=False,
        )
    )
    fig.update_layout(
        title="Figure 3: SVM Confusion Matrix",
        xaxis_title="Predicted",
        yaxis_title="Actual",
        template="plotly_dark",
        height=500,
    )
    return fig


def plot_roc_curve(model, X_test, y_test, feature_names=None):
    """Figure 4: ROC curve for best model (SVM)."""
    y_true = y_test.map({"Not Placed": 0, "Placed": 1})
    X_in = _prepare_input_for_model(X_test, model, feature_names=feature_names)
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_in)[:, 1]
    else:
        y_proba = model.decision_function(X_in)

    fpr, tpr, _ = roc_curve(y_true, y_proba)
    auc = roc_auc_score(y_true, y_proba)

    fig = go.Figure(
        data=[
            go.Scatter(x=fpr, y=tpr, mode="lines", name="ROC Curve", line_color="#636EFA"),
            go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random", line=dict(dash="dash", color="#EF553B")),
        ]
    )
    fig.update_layout(
        title=f"Figure 4: ROC Curve (AUC = {auc:.3f})",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        template="plotly_dark",
        height=500,
    )
    return fig


def plot_feature_importance(model, X_train, y_train, feature_names):
    """Figure 5: Feature importance for SVM via permutation importance."""
    result = permutation_importance(
        model,
        X_train,
        y_train.map({"Not Placed": 0, "Placed": 1}),
        n_repeats=20,
        random_state=42,
        n_jobs=-1,
    )

    imp = pd.DataFrame(
        {"feature": feature_names, "importance": result.importances_mean}
    ).sort_values("importance", ascending=False).head(15)

    fig = px.bar(
        imp,
        x="importance",
        y="feature",
        orientation="h",
        title="Figure 5: Feature Importance (Permutation) for SVM",
        labels={"importance": "Mean decrease in score", "feature": "Feature"},
        color="importance",
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    fig.update_layout(template="plotly_dark", height=700)
    fig.update_yaxes(categoryorder="total ascending")
    return fig


# --- Page layout ---

st.title("📊 Placement Prediction Model Analysis")
st.markdown(
    "This app recreates the key analysis figures used in the placement prediction study: class distribution, model comparison, confusion matrix, ROC curve, and feature importance."
)

try:
    df_raw = load_data()
    artifacts = load_artifacts()

    feature_names = artifacts["feature_names"]
    scaler = artifacts["scaler"]
    models = artifacts["models"]

    st.markdown("---")

    # Prepare the training/test split and SMOTE
    df = df_raw.copy()

    # Ensure placement status is numeric 0/1 (some cleaned datasets already use numeric labels)
    if df["Placement Status"].dtype == object:
        df["Placement Status"] = df["Placement Status"].map({"Not Placed": 0, "Placed": 1})

    df["Placement Status"] = pd.to_numeric(df["Placement Status"], errors="coerce")
    df = df.dropna(subset=["Placement Status"]).reset_index(drop=True)

    X = preprocess_features(df, feature_names)
    y = df["Placement Status"].map({0: "Not Placed", 1: "Placed"})

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
        shuffle=True,
    )

    smote = SMOTE(random_state=42, k_neighbors=1)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

    X_train_scaled = scaler.transform(X_train_smote)
    X_test_scaled = scaler.transform(X_test)

    # Wrap scaled arrays with DataFrame columns to avoid sklearn feature-name warnings
    X_train_df = pd.DataFrame(X_train_scaled, columns=feature_names)
    X_test_df = pd.DataFrame(X_test_scaled, columns=feature_names)

    st.subheader("Figure 1: Class Distribution Before and After SMOTE")
    st.plotly_chart(plot_smote_distribution(y_train, y_train_smote), width="stretch")

    st.markdown("---")
    st.subheader("Figure 2: Model Comparison Across Evaluation Metrics")
    metrics_df = compute_metrics(models, X_test_df, y_test, feature_names)
    st.plotly_chart(plot_comparison_metrics(metrics_df), width="stretch")

    if "SVM" in models:
        best_model = models["SVM"]
        st.markdown("---")
        st.subheader("Figure 3: SVM Confusion Matrix")
        st.plotly_chart(plot_confusion_matrix(best_model, X_test_df, y_test, feature_names=feature_names), width="stretch")

        st.markdown("---")
        st.subheader("Figure 4: SVM ROC Curve")
        st.plotly_chart(plot_roc_curve(best_model, X_test_df, y_test, feature_names=feature_names), width="stretch")

        st.markdown("---")
        st.subheader("Figure 5: Feature Importance (SVM)")
        st.plotly_chart(
            plot_feature_importance(best_model, X_train_df, y_train_smote, feature_names),
            width="stretch",
        )

except Exception as e:
    st.error(f"Failed to generate analysis: {e}")
    raise
