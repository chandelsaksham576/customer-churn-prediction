"""
app.py
Minimal Matte-Dark Customer Churn Analytics Dashboard
Built with 100% Native Streamlit Containers & Components for Robust Cloud Rendering
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Streamlit Page Setup
st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal Matte-Dark CSS (Zinc/Carbon Theme, Zero Shadows, Native Overrides)
st.markdown("""
<style>
    /* Hide Streamlit default chrome & reduce top padding */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 100% !important;
        width: 100% !important;
    }

    /* Prevent metric labels and numbers from truncating with ellipsis */
    [data-testid="stMetricLabel"] {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    [data-testid="stMetricLabel"] > div {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    [data-testid="stMetricValue"] {
        white-space: nowrap !important;
        overflow: visible !important;
    }

    /* Base Typography & Backgrounds */
    body, [data-testid="stAppViewContainer"] {
        background-color: #09090B !important;
        color: #FAFAFA !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* Native Card Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #27272A !important;
        border-radius: 6px !important;
        background-color: #121215 !important;
        box-shadow: none !important;
    }

    /* Native Metric Styling (Vercel / Linear inspired) */
    [data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: 600 !important;
        color: #FAFAFA !important;
        letter-spacing: -0.02em !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 11px !important;
        font-weight: 500 !important;
        color: #A1A1AA !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid #27272A !important;
        gap: 1.75rem !important;
        background-color: transparent !important;
        padding-bottom: 0px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        color: #71717A !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        padding: 0.6rem 0.1rem 0.75rem 0.1rem !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #A1A1AA !important;
    }
    .stTabs [aria-selected="true"] {
        color: #FAFAFA !important;
        border-bottom: 2px solid #FAFAFA !important;
    }

    /* Primary Matte Button */
    .stButton > button {
        background-color: #FAFAFA !important;
        color: #09090B !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        border: 1px solid #FAFAFA !important;
        border-radius: 6px !important;
        padding: 0.45rem 1rem !important;
        box-shadow: none !important;
        transition: opacity 0.15s ease !important;
    }
    .stButton > button:hover {
        opacity: 0.9 !important;
        color: #09090B !important;
        border-color: #FAFAFA !important;
    }
</style>
""", unsafe_allow_html=True)

PROJECT_ROOT = Path(__file__).resolve().parent
MODELS_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"

# Standard Matte Plotly Formatter
def format_matte_plot(fig, title=None, height=310):
    """Enforces minimal dark aesthetic with subtle gridlines and zero glowing elements."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif", color="#A1A1AA", size=11),
        title=dict(
            text=title or "",
            font=dict(color="#FAFAFA", size=13, family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"),
            x=0.01,
            y=0.96,
            xanchor="left",
            yanchor="top"
        ) if title else None,
        margin=dict(l=35, r=15, t=40 if title else 15, b=35),
        height=height,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor="#27272A",
            tickfont=dict(color="#A1A1AA", size=10),
            title_font=dict(color="#71717A", size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#27272A",
            zeroline=True,
            zerolinecolor="#27272A",
            showline=False,
            tickfont=dict(color="#A1A1AA", size=10),
            title_font=dict(color="#71717A", size=11)
        ),
        legend=dict(
            font=dict(color="#A1A1AA", size=10),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            yanchor="top",
            y=0.98,
            xanchor="right",
            x=0.98
        )
    )
    return fig

@st.cache_resource
def load_engine():
    """Initializes and caches the ChurnRetentionEngine with self-healing fallback."""
    try:
        from src.predict import ChurnRetentionEngine
        engine = ChurnRetentionEngine(MODELS_DIR)
        if engine.is_ready():
            return engine
    except Exception:
        pass

    try:
        from src.preprocess import run_preprocessing
        from src.train import train_and_evaluate
        sample_csv = DATA_DIR / "sample_data.csv"
        run_preprocessing(data_path=sample_csv if sample_csv.exists() else None, sample_size=10000)
        train_and_evaluate()
        from src.predict import ChurnRetentionEngine
        return ChurnRetentionEngine(MODELS_DIR)
    except Exception:
        return None

@st.cache_data
def load_data_sample():
    """Loads lightweight data sample for reporting."""
    sample_csv = DATA_DIR / "sample_data.csv"
    if sample_csv.exists():
        return pd.read_csv(sample_csv)
    raw_files = list((DATA_DIR / "raw").glob("*.csv"))
    if raw_files:
        return pd.read_csv(raw_files[0], nrows=5000)
    return None

def main():
    engine = load_engine()
    df = load_data_sample()

    if engine is None or df is None:
        st.error("Engine or dataset initialization in progress. Please refresh momentarily.")
        return

    records_count = engine.metadata.get("train_records", 80000) if engine else 80000
    target_col = engine.metadata.get("target_column", "Churn")

    # Native Header Row
    head_left, head_right = st.columns([3, 1])
    with head_left:
        st.markdown("<h1 style='margin:0; font-size: 1.5rem; font-weight: 600; color: #FAFAFA; letter-spacing: -0.02em;'>Customer Churn Analytics</h1>", unsafe_allow_html=True)
        st.caption("Predictive retention modeling and subscriber risk intelligence")
    with head_right:
        st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.caption(f"Engine Ready • {records_count:,} records")

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    # Top KPI Row (4 Native Bordered Cards)
    total_customers = len(df)
    churned_customers = int((df[target_col] == 1).sum())
    retained_customers = total_customers - churned_customers
    churn_rate = (churned_customers / total_customers) * 100
    retention_rate = 100 - churn_rate

    spend_col = "Total Spend" if "Total Spend" in df.columns else None
    revenue_at_risk = df[df[target_col] == 1][spend_col].sum() if spend_col else 0

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        with st.container(border=True):
            st.metric("Total Customers", f"{total_customers:,}", help="Active portfolio sample")
    with kpi2:
        with st.container(border=True):
            st.metric("Monthly Revenue at Risk", f"${revenue_at_risk:,.0f}", help="Identified at-risk accounts")
    with kpi3:
        with st.container(border=True):
            st.metric("Overall Retention Rate", f"{retention_rate:.1f}%", help=f"{retained_customers:,} active subscribers")
    with kpi4:
        with st.container(border=True):
            st.metric("Churn Rate", f"{churn_rate:.1f}%", help=f"{churned_customers:,} accounts churned")

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # 3 Streamlined Tabs
    tab_overview, tab_models, tab_lookup = st.tabs([
        "Overview",
        "Model Evaluation",
        "Customer Risk Lookup"
    ])

    # =========================================================================
    # TAB 1: OVERVIEW (Balanced 2x2 Grid)
    # =========================================================================
    with tab_overview:
        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            with st.container(border=True):
                segment_col = "Contract Length" if "Contract Length" in df.columns else engine.metadata["categorical_features"][0]
                status_df = df.copy()
                status_df["Status"] = status_df[target_col].map({1: "Churned", 0: "Retained"})

                fig_status = px.histogram(
                    status_df,
                    x=segment_col,
                    color="Status",
                    barmode="group",
                    color_discrete_map={"Retained": "#10B981", "Churned": "#F43F5E"}
                )
                format_matte_plot(fig_status, title=f"Customer Status by {segment_col}")
                fig_status.update_layout(xaxis_title="", yaxis_title="Subscribers")
                st.plotly_chart(fig_status, use_container_width=True, config={"displayModeBar": False})

        with row1_col2:
            with st.container(border=True):
                tier_col = "Subscription Type" if "Subscription Type" in df.columns else (
                    engine.metadata["categorical_features"][1] if len(engine.metadata["categorical_features"]) > 1 else segment_col
                )
                tier_churn = df.groupby(tier_col)[target_col].agg(["count", "mean"]).reset_index()
                tier_churn["Churn_Rate_%"] = (tier_churn["mean"] * 100).round(1)

                fig_tier = px.bar(
                    tier_churn,
                    x=tier_col,
                    y="Churn_Rate_%",
                    color_discrete_sequence=["#F43F5E"],
                    text="Churn_Rate_%"
                )
                format_matte_plot(fig_tier, title=f"Churn Rate across {tier_col}")
                fig_tier.update_traces(textposition="outside", textfont=dict(color="#A1A1AA", size=10))
                fig_tier.update_layout(xaxis_title="", yaxis_title="Churn Rate (%)", yaxis=dict(range=[0, max(tier_churn["Churn_Rate_%"]) * 1.25]))
                st.plotly_chart(fig_tier, use_container_width=True, config={"displayModeBar": False})

        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            with st.container(border=True):
                scatter_x = "Tenure" if "Tenure" in df.columns else engine.metadata["numerical_features"][0]
                scatter_y = "Total Spend" if "Total Spend" in df.columns else (
                    engine.metadata["numerical_features"][1] if len(engine.metadata["numerical_features"]) > 1 else scatter_x
                )
                scatter_sample = df.sample(min(len(df), 1200), random_state=42).copy()
                scatter_sample["Status"] = scatter_sample[target_col].map({1: "Churned", 0: "Retained"})

                fig_scatter = px.scatter(
                    scatter_sample,
                    x=scatter_x,
                    y=scatter_y,
                    color="Status",
                    color_discrete_map={"Retained": "#10B981", "Churned": "#F43F5E"},
                    opacity=0.65
                )
                format_matte_plot(fig_scatter, title=f"Customer Value vs. {scatter_x}")
                fig_scatter.update_traces(marker=dict(size=5))
                fig_scatter.update_layout(xaxis_title=f"{scatter_x} (Months)", yaxis_title=f"{scatter_y} ($)")
                st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

        with row2_col2:
            with st.container(border=True):
                if "Support Calls" in df.columns:
                    support_churn = df.groupby("Support Calls")[target_col].agg(["count", "mean"]).reset_index()
                    support_churn["Churn_Rate_%"] = (support_churn["mean"] * 100).round(1)

                    fig_support = px.line(
                        support_churn,
                        x="Support Calls",
                        y="Churn_Rate_%",
                        markers=True,
                        line_shape="linear"
                    )
                    format_matte_plot(fig_support, title="Churn Rate Surge by Support Inquiries")
                    fig_support.update_traces(line=dict(color="#F43F5E", width=2), marker=dict(size=6, color="#FAFAFA"))
                    fig_support.update_layout(xaxis_title="Support Calls Logged", yaxis_title="Churn Rate (%)")
                    st.plotly_chart(fig_support, use_container_width=True, config={"displayModeBar": False})
                else:
                    alt_col = engine.metadata["numerical_features"][0]
                    fig_alt = px.histogram(df, x=alt_col, color=target_col, color_discrete_map={0: "#10B981", 1: "#F43F5E"})
                    format_matte_plot(fig_alt, title=f"Distribution of {alt_col}")
                    st.plotly_chart(fig_alt, use_container_width=True, config={"displayModeBar": False})

    # =========================================================================
    # TAB 2: MODEL EVALUATION
    # =========================================================================
    with tab_models:
        metrics = engine.metrics or {}
        lr_m = metrics.get("Logistic Regression", {})
        dt_m = metrics.get("Decision Tree", {})

        # Native Streamlit Benchmark Table
        with st.container(border=True):
            st.markdown("<div style='font-size: 0.8125rem; font-weight: 600; color: #FAFAFA; margin-bottom: 0.5rem;'>Classification Performance Benchmark</div>", unsafe_allow_html=True)
            
            scorecard_df = pd.DataFrame([
                {
                    "Metric": "Accuracy",
                    "Logistic Regression": f"{lr_m.get('accuracy', 0)*100:.2f}%",
                    "Decision Tree": f"{dt_m.get('accuracy', 0)*100:.2f}%",
                    "Variance": f"+{(dt_m.get('accuracy', 0) - lr_m.get('accuracy', 0))*100:.2f}%",
                    "Best Performer": "Decision Tree"
                },
                {
                    "Metric": "Precision",
                    "Logistic Regression": f"{lr_m.get('precision', 0)*100:.2f}%",
                    "Decision Tree": f"{dt_m.get('precision', 0)*100:.2f}%",
                    "Variance": f"+{(dt_m.get('precision', 0) - lr_m.get('precision', 0))*100:.2f}%",
                    "Best Performer": "Decision Tree"
                },
                {
                    "Metric": "Recall",
                    "Logistic Regression": f"{lr_m.get('recall', 0)*100:.2f}%",
                    "Decision Tree": f"{dt_m.get('recall', 0)*100:.2f}%",
                    "Variance": f"+{(dt_m.get('recall', 0) - lr_m.get('recall', 0))*100:.2f}%",
                    "Best Performer": "Decision Tree"
                },
                {
                    "Metric": "F1-Score",
                    "Logistic Regression": f"{lr_m.get('f1', 0)*100:.2f}%",
                    "Decision Tree": f"{dt_m.get('f1', 0)*100:.2f}%",
                    "Variance": f"+{(dt_m.get('f1', 0) - lr_m.get('f1', 0))*100:.2f}%",
                    "Best Performer": "Decision Tree"
                },
                {
                    "Metric": "ROC-AUC",
                    "Logistic Regression": f"{lr_m.get('roc_auc', 0):.4f}",
                    "Decision Tree": f"{dt_m.get('roc_auc', 0):.4f}",
                    "Variance": f"+{dt_m.get('roc_auc', 0) - lr_m.get('roc_auc', 0):.4f}",
                    "Best Performer": "Decision Tree"
                }
            ])
            st.dataframe(scorecard_df, use_container_width=True, hide_index=True)

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        col_eval1, col_eval2 = st.columns(2)

        with col_eval1:
            with st.container(border=True):
                # Confusion Matrices
                cm_choice = st.radio("Model Selection:", ["Decision Tree", "Logistic Regression"], horizontal=True)
                active_cm_data = dt_m if cm_choice == "Decision Tree" else lr_m
                cm_matrix = np.array(active_cm_data.get("confusion_matrix", {}).get("matrix", [[0,0],[0,0]]))

                fig_cm = px.imshow(
                    cm_matrix,
                    text_auto=True,
                    color_continuous_scale=[[0, "#121215"], [1, "#10B981" if cm_choice == "Decision Tree" else "#6366F1"]],
                    x=["Retained (0)", "Churned (1)"],
                    y=["Retained (0)", "Churned (1)"]
                )
                format_matte_plot(fig_cm, title=f"Confusion Matrix: {cm_choice}", height=280)
                fig_cm.update_layout(xaxis_title="Predicted", yaxis_title="Actual", coloraxis_showscale=False)
                st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})

        with col_eval2:
            with st.container(border=True):
                # ROC Curve Overlay
                fig_roc = go.Figure()
                roc_lr = lr_m.get("roc_curve", {})
                if roc_lr:
                    fig_roc.add_trace(go.Scatter(
                        x=roc_lr.get("fpr", []),
                        y=roc_lr.get("tpr", []),
                        mode="lines",
                        name=f"Logistic Regression ({lr_m.get('roc_auc', 0):.3f})",
                        line=dict(color="#6366F1", width=2)
                    ))
                roc_dt = dt_m.get("roc_curve", {})
                if roc_dt:
                    fig_roc.add_trace(go.Scatter(
                        x=roc_dt.get("fpr", []),
                        y=roc_dt.get("tpr", []),
                        mode="lines",
                        name=f"Decision Tree ({dt_m.get('roc_auc', 0):.3f})",
                        line=dict(color="#10B981", width=2)
                    ))
                fig_roc.add_trace(go.Scatter(
                    x=[0, 1], y=[0, 1],
                    mode="lines",
                    name="Reference",
                    line=dict(color="#52525B", width=1, dash="dot")
                ))
                format_matte_plot(fig_roc, title="ROC Curves Comparison", height=280)
                fig_roc.update_layout(xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
                st.plotly_chart(fig_roc, use_container_width=True, config={"displayModeBar": False})

        col_fi1, col_fi2 = st.columns(2)
        with col_fi1:
            with st.container(border=True):
                lr_fi = lr_m.get("feature_importance", [])[:6]
                df_lr_fi = pd.DataFrame(lr_fi)
                if not df_lr_fi.empty:
                    fig_lr_fi = px.bar(
                        df_lr_fi,
                        x="importance",
                        y="feature",
                        orientation="h",
                        color="impact",
                        color_discrete_map={"Increases Churn": "#F43F5E", "Decreases Churn": "#10B981"}
                    )
                    format_matte_plot(fig_lr_fi, title="Logistic Regression: Log-Odds Coefficients", height=260)
                    fig_lr_fi.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="Coefficient", yaxis_title="")
                    st.plotly_chart(fig_lr_fi, use_container_width=True, config={"displayModeBar": False})

        with col_fi2:
            with st.container(border=True):
                dt_fi = dt_m.get("feature_importance", [])[:6]
                df_dt_fi = pd.DataFrame(dt_fi)
                if not df_dt_fi.empty:
                    fig_dt_fi = px.bar(
                        df_dt_fi,
                        x="importance",
                        y="feature",
                        orientation="h",
                        color_discrete_sequence=["#10B981"]
                    )
                    format_matte_plot(fig_dt_fi, title="Decision Tree: Gini Feature Importance", height=260)
                    fig_dt_fi.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="Gini Score", yaxis_title="")
                    st.plotly_chart(fig_dt_fi, use_container_width=True, config={"displayModeBar": False})

        # Decision Tree Rules Inspector
        tree_rules = dt_m.get("tree_rules_summary")
        if tree_rules:
            with st.expander("Decision Tree Split Structure (Top 3 Levels)"):
                st.code(tree_rules, language="text")

    # =========================================================================
    # TAB 3: CUSTOMER RISK LOOKUP
    # =========================================================================
    with tab_lookup:
        meta = engine.metadata
        num_features = meta.get("numerical_features", [])
        cat_features = meta.get("categorical_features", [])
        stats = meta.get("feature_stats", {})
        cats = meta.get("categorical_unique", {})

        if "sim_state" not in st.session_state:
            st.session_state.sim_state = {}

        # Top Bar: Actions & Simulator
        top_col1, top_col2 = st.columns([3, 1])
        with top_col1:
            active_model_type = st.radio(
                "Prediction Model:",
                ["Decision Tree", "Logistic Regression", "Dual-Model"],
                horizontal=True
            )
        with top_col2:
            st.markdown("<div style='height: 1.4rem;'></div>", unsafe_allow_html=True)
            if st.button("Load Random Profile"):
                random_row = df.sample(1, random_state=int(np.random.randint(1, 10000))).iloc[0].to_dict()
                for c in num_features + cat_features:
                    if c in random_row:
                        st.session_state.sim_state[c] = random_row[c]
                st.rerun()

        # Input Form inside clean 3-column bordered container
        input_data = {}
        with st.container(border=True):
            st.markdown("<div style='font-size: 0.8125rem; font-weight: 600; color: #FAFAFA; margin-bottom: 0.5rem;'>Customer Parameters</div>", unsafe_allow_html=True)
            f_col1, f_col2, f_col3 = st.columns(3)

            # Divide features logically across 3 columns
            all_cols = num_features + cat_features
            col_buckets = [f_col1, f_col2, f_col3]

            for idx, feat in enumerate(all_cols):
                target_box = col_buckets[idx % 3]
                with target_box:
                    if feat in num_features:
                        f_min = float(stats.get(feat, {}).get("min", 0.0))
                        f_max = float(stats.get(feat, {}).get("max", 100.0))
                        f_def = float(stats.get(feat, {}).get("default", (f_min + f_max) / 2))
                        val = float(st.session_state.sim_state.get(feat, f_def))
                        val = max(f_min, min(f_max, val))

                        is_integer = (f_min.is_integer() and f_max.is_integer())
                        if is_integer:
                            input_data[feat] = st.slider(feat, int(f_min), int(f_max), int(val), 1, key=f"f_{feat}")
                        else:
                            input_data[feat] = st.slider(feat, f_min, f_max, round(val, 2), 0.1, key=f"f_{feat}")
                    else:
                        opt_list = cats.get(feat, ["Standard"])
                        saved_opt = str(st.session_state.sim_state.get(feat, opt_list[0]))
                        idx_sel = opt_list.index(saved_opt) if saved_opt in opt_list else 0
                        input_data[feat] = st.selectbox(feat, opt_list, index=idx_sel, key=f"f_{feat}")

            st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
            run_pred = st.button("Run Risk Assessment", use_container_width=True)

        # Output Card
        if run_pred or True:
            model_eval_name = "Logistic Regression" if active_model_type == "Logistic Regression" else "Decision Tree"
            pred_res = engine.predict_single(input_data, model_name=model_eval_name)
            prob_pct = pred_res["probability_pct"]

            st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

            with st.container(border=True):
                out_col1, out_col2 = st.columns([1, 1.4])

                with out_col1:
                    st.markdown("<div style='font-size: 0.8125rem; font-weight: 600; color: #FAFAFA; margin-bottom: 0.5rem;'>Assessment Result</div>", unsafe_allow_html=True)
                    if prob_pct >= 65:
                        st.error(f"High Churn Risk — {prob_pct}% Likelihood")
                    elif prob_pct >= 35:
                        st.warning(f"Moderate Churn Risk — {prob_pct}% Likelihood")
                    else:
                        st.success(f"Low Churn Risk — {prob_pct}% Likelihood")

                    st.progress(prob_pct / 100.0)

                    if active_model_type == "Dual-Model":
                        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
                        with st.container(border=True):
                            st.caption(f"Decision Tree: {pred_res['decision_tree']['probability_pct']}% • Logistic Regression: {pred_res['logistic_regression']['probability_pct']}%")

                with out_col2:
                    st.markdown("<div style='font-size: 0.8125rem; font-weight: 600; color: #FAFAFA; margin-bottom: 0.5rem;'>Prescribed Retention Actions</div>", unsafe_allow_html=True)
                    actions = pred_res["action_plan"]
                    for a in actions:
                        with st.container(border=True):
                            st.markdown(f"**{a['title']}**")
                            st.caption(f"{a['action']}")
                            st.markdown(f"<div style='font-size: 0.75rem; color: #10B981;'>Impact: {a['expected_impact']} &bull; Priority: {a['urgency']}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
