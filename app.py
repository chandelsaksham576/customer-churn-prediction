"""
app.py
Minimal Matte-Dark Customer Churn Analytics Dashboard
Design Language: Inspired by Vercel, Linear, and Raycast (Zinc / Matte Carbon)
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

# Minimal Matte-Dark CSS (Zinc/Carbon Theme, Zero Drop-Shadows, Clean Typography)
st.markdown("""
<style>
    /* Hide Streamlit default chrome & tighten top spacing */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1280px !important;
        margin: 0 auto !important;
    }

    /* Base Typography & Backgrounds */
    body, [data-testid="stAppViewContainer"] {
        background-color: #09090B !important;
        color: #FAFAFA !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* App Header Bar */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #27272A;
    }
    .app-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #FAFAFA;
        letter-spacing: -0.02em;
        margin: 0;
    }
    .app-subtitle {
        font-size: 0.8125rem;
        color: #71717A;
        margin: 0.15rem 0 0 0;
    }
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.75rem;
        font-weight: 500;
        color: #A1A1AA;
        background-color: #121215;
        border: 1px solid #27272A;
        border-radius: 9999px;
        padding: 0.25rem 0.65rem;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        background-color: #10B981;
        border-radius: 50%;
    }

    /* KPI Cards */
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #121215;
        border: 1px solid #27272A;
        border-radius: 6px;
        padding: 1rem 1.2rem;
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 500;
        color: #A1A1AA;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 600;
        color: #FAFAFA;
        letter-spacing: -0.02em;
        line-height: 1.15;
    }
    .kpi-meta {
        font-size: 11px;
        color: #71717A;
        margin-top: 0.35rem;
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

    /* Surface Container Styling */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #27272A !important;
        border-radius: 6px !important;
        background-color: #121215 !important;
        box-shadow: none !important;
    }

    /* Primary Matte Button (Linear / Vercel style) */
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

    /* Status Pills */
    .pill-high {
        background-color: #3F131C;
        color: #FB7185;
        border: 1px solid #9F1239;
        border-radius: 9999px;
        padding: 0.2rem 0.65rem;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
    }
    .pill-mod {
        background-color: #382006;
        color: #FBBF24;
        border: 1px solid #78350F;
        border-radius: 9999px;
        padding: 0.2rem 0.65rem;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
    }
    .pill-low {
        background-color: #062E22;
        color: #34D399;
        border: 1px solid #065F46;
        border-radius: 9999px;
        padding: 0.2rem 0.65rem;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
    }

    /* Recommendation Action Row */
    .action-row {
        border-bottom: 1px solid #27272A;
        padding: 0.85rem 0;
    }
    .action-row:last-child {
        border-bottom: none;
    }
    .action-name {
        font-weight: 600;
        font-size: 0.875rem;
        color: #FAFAFA;
        margin-bottom: 0.2rem;
    }
    .action-detail {
        font-size: 0.8125rem;
        color: #A1A1AA;
        line-height: 1.4;
    }
    .action-impact {
        font-size: 0.75rem;
        color: #10B981;
        margin-top: 0.25rem;
    }

    /* Comparison Table Styling */
    .comp-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
    }
    .comp-table th {
        text-align: left;
        color: #71717A;
        font-weight: 500;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.6rem 0.75rem;
        border-bottom: 1px solid #27272A;
    }
    .comp-table td {
        padding: 0.7rem 0.75rem;
        border-bottom: 1px solid #18181B;
        color: #FAFAFA;
    }
    .comp-table tr:hover {
        background-color: #18181B;
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
            titlefont=dict(color="#71717A", size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#27272A",
            zeroline=True,
            zerolinecolor="#27272A",
            showline=False,
            tickfont=dict(color="#A1A1AA", size=10),
            titlefont=dict(color="#71717A", size=11)
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

    # Minimal App Header
    records_count = engine.metadata.get("train_records", 80000) if engine else 80000
    st.markdown(f"""
    <div class="app-header">
        <div>
            <h1 class="app-title">Customer Churn Analytics</h1>
            <p class="app-subtitle">Predictive retention modeling and subscriber risk intelligence</p>
        </div>
        <div class="status-indicator">
            <span class="status-dot"></span>
            <span>Production Engine Ready &bull; {records_count:,} records</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if engine is None or df is None:
        st.error("Engine or dataset initialization in progress. Please refresh momentarily.")
        return

    target_col = engine.metadata.get("target_column", "Churn")

    # Top KPI Row (4 flat cards)
    total_customers = len(df)
    churned_customers = int((df[target_col] == 1).sum())
    retained_customers = total_customers - churned_customers
    churn_rate = (churned_customers / total_customers) * 100
    retention_rate = 100 - churn_rate

    spend_col = "Total Spend" if "Total Spend" in df.columns else None
    revenue_at_risk = df[df[target_col] == 1][spend_col].sum() if spend_col else 0

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">Total Customers</div>
            <div class="kpi-value">{total_customers:,}</div>
            <div class="kpi-meta">Active portfolio sample</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Monthly Revenue at Risk</div>
            <div class="kpi-value">${revenue_at_risk:,.0f}</div>
            <div class="kpi-meta">Identified at-risk accounts</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Overall Retention Rate</div>
            <div class="kpi-value">{retention_rate:.1f}%</div>
            <div class="kpi-meta">{retained_customers:,} active subscribers</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Churn Rate</div>
            <div class="kpi-value">{churn_rate:.1f}%</div>
            <div class="kpi-meta">{churned_customers:,} accounts churned</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
                fig_tier.update_layout(xaxis_title="", yaxis_title="Churn Rate (%)", yaxis=dict(range=[0, max(tier_churn["Churn_Rate_%"]) * 1.2]))
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

        # Scorecard comparison table
        with st.container(border=True):
            st.markdown("""
            <div style="font-size: 0.8125rem; font-weight: 600; color: #FAFAFA; margin-bottom: 0.75rem;">
                Classification Performance Benchmark
            </div>
            """, unsafe_allow_html=True)

            scorecard_rows = [
                ("Accuracy", lr_m.get("accuracy", 0), dt_m.get("accuracy", 0)),
                ("Precision", lr_m.get("precision", 0), dt_m.get("precision", 0)),
                ("Recall", lr_m.get("recall", 0), dt_m.get("recall", 0)),
                ("F1-Score", lr_m.get("f1", 0), dt_m.get("f1", 0)),
                ("ROC-AUC", lr_m.get("roc_auc", 0), dt_m.get("roc_auc", 0))
            ]

            rows_html = ""
            for name, val_lr, val_dt in scorecard_rows:
                delta = val_dt - val_lr
                winner = "Decision Tree" if delta > 0 else "Logistic Regression"
                delta_str = f"+{delta*100:.2f}%" if delta > 0 else f"{delta*100:.2f}%"
                rows_html += f"""
                <tr>
                    <td><strong>{name}</strong></td>
                    <td>{val_lr*100:.2f}%</td>
                    <td>{val_dt*100:.2f}%</td>
                    <td style="color: {'#10B981' if delta >= 0 else '#F43F5E'};">{delta_str}</td>
                    <td style="color: #A1A1AA;">{winner}</td>
                </tr>
                """

            st.markdown(f"""
            <table class="comp-table">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Logistic Regression</th>
                        <th>Decision Tree</th>
                        <th>Variance</th>
                        <th>Best Performer</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
            """, unsafe_allow_html=True)

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

            # Set flat pill style
            if prob_pct >= 65:
                pill_class = "pill-high"
                pill_text = "High Churn Risk"
                bar_color = "#F43F5E"
            elif prob_pct >= 35:
                pill_class = "pill-mod"
                pill_text = "Moderate Churn Risk"
                bar_color = "#F59E0B"
            else:
                pill_class = "pill-low"
                pill_text = "Low Churn Risk"
                bar_color = "#10B981"

            st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

            with st.container(border=True):
                out_col1, out_col2 = st.columns([1, 1.4])

                with out_col1:
                    st.markdown("<div style='font-size: 0.8125rem; font-weight: 600; color: #FAFAFA; margin-bottom: 0.75rem;'>Assessment Result</div>", unsafe_allow_html=True)
                    st.markdown(f'<span class="{pill_class}">{pill_text}</span>', unsafe_allow_html=True)

                    # Minimal horizontal progress bar
                    st.markdown(f"""
                    <div style="margin-top: 1.25rem;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #A1A1AA; margin-bottom: 0.35rem;">
                            <span>Churn Likelihood</span>
                            <span style="font-weight: 600; color: #FAFAFA;">{prob_pct}%</span>
                        </div>
                        <div style="background-color: #27272A; height: 6px; border-radius: 9999px; overflow: hidden;">
                            <div style="background-color: {bar_color}; width: {prob_pct}%; height: 100%; border-radius: 9999px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if active_model_type == "Dual-Model":
                        st.markdown(f"""
                        <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid #27272A; font-size: 0.75rem; color: #71717A;">
                            <div>Decision Tree: <span style="color: #FAFAFA; font-weight: 500;">{pred_res['decision_tree']['probability_pct']}%</span></div>
                            <div style="margin-top: 0.2rem;">Logistic Regression: <span style="color: #FAFAFA; font-weight: 500;">{pred_res['logistic_regression']['probability_pct']}%</span></div>
                        </div>
                        """, unsafe_allow_html=True)

                with out_col2:
                    st.markdown("<div style='font-size: 0.8125rem; font-weight: 600; color: #FAFAFA; margin-bottom: 0.5rem;'>Prescribed Retention Actions</div>", unsafe_allow_html=True)
                    actions = pred_res["action_plan"]
                    action_html = ""
                    for a in actions:
                        action_html += f"""
                        <div class="action-row">
                            <div class="action-name">{a['title']}</div>
                            <div class="action-detail">{a['action']}</div>
                            <div class="action-impact">Impact: {a['expected_impact']} &bull; Priority: {a['urgency']}</div>
                        </div>
                        """
                    st.markdown(action_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
