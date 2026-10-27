"""
app.py
Interactive Customer Churn Prediction & Retention Dashboard
Built with Streamlit, Plotly, Pandas, and Scikit-Learn.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Customer Churn & Retention Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for executive dark design
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.25);
        text-align: center;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-card p {
        margin: 0.4rem 0 0 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: #38BDF8;
    }
    .action-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-left: 5px solid #3B82F6;
        padding: 1rem 1.2rem;
        margin-bottom: 0.9rem;
        border-radius: 0 8px 8px 0;
    }
    .action-title {
        font-weight: 700;
        font-size: 1.05rem;
        color: #F8FAFC;
    }
    .action-meta {
        font-size: 0.85rem;
        color: #94A3B8;
        margin: 0.2rem 0 0.5rem 0;
    }
    .risk-high {
        background-color: rgba(239, 68, 68, 0.2);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    .risk-mod {
        background-color: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    .risk-low {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

PROJECT_ROOT = Path(__file__).resolve().parent
MODELS_DIR = PROJECT_ROOT / "models"
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

@st.cache_resource
def load_engine():
    """Initializes and caches the ChurnRetentionEngine with automatic self-healing."""
    try:
        from src.predict import ChurnRetentionEngine
        engine = ChurnRetentionEngine(MODELS_DIR)
        if engine.is_ready():
            return engine
    except Exception:
        pass

    # Self-healing: if models are missing or pickle versions differ on cloud runtime, retrain cleanly
    try:
        from src.preprocess import run_preprocessing
        from src.train import train_and_evaluate
        sample_csv = PROJECT_ROOT / "data" / "sample_data.csv"
        run_preprocessing(data_path=sample_csv if sample_csv.exists() else None, sample_size=10000)
        train_and_evaluate()
        from src.predict import ChurnRetentionEngine
        engine = ChurnRetentionEngine(MODELS_DIR)
        return engine
    except Exception as e:
        st.sidebar.error(f"Engine initialization error: {e}")
        return None

@st.cache_data
def load_sample_data():
    """Loads a representative sample of raw cleaned data for EDA dashboard."""
    try:
        # Priority 1: Lightweight sample CSV (ideal for cloud deployments)
        sample_csv = PROJECT_ROOT / "data" / "sample_data.csv"
        if sample_csv.exists():
            return pd.read_csv(sample_csv)

        # Priority 2: Serialized processed sample
        data_path = MODELS_DIR / "processed_data.pkl"
        if data_path.exists():
            import joblib
            data = joblib.load(data_path)
            if "raw_cleaned_sample" in data:
                return data["raw_cleaned_sample"]

        # Priority 3: First rows of any raw CSV
        csv_files = list(RAW_DATA_DIR.glob("*.csv"))
        if csv_files:
            train_file = [f for f in csv_files if "train" in f.name.lower()]
            target_file = train_file[0] if train_file else csv_files[0]
            df = pd.read_csv(target_file, nrows=5000)
            return df
    except Exception:
        pass
    return None

def main():
    engine = load_engine()
    sample_df = load_sample_data()

    # Sidebar Header & Controls
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
        st.title("Retention IQ")
        st.markdown("**Enterprise Churn Analytics**")
        st.markdown("---")

        if engine is None or not engine.is_ready():
            st.error("⚠️ Models or preprocessors not detected.")
            if st.button("🚀 Run Preprocessing & Training Pipeline", type="primary"):
                with st.spinner("Training Logistic Regression & Decision Tree models..."):
                    from src.preprocess import run_preprocessing
                    from src.train import train_and_evaluate
                    run_preprocessing()
                    train_and_evaluate()
                    st.cache_resource.clear()
                    st.cache_data.clear()
                    st.success("Pipeline executed successfully! Reloading...")
                    st.rerun()
            st.info("Ensure `src/preprocess.py` and `src/train.py` have finished running.")
            return

        st.subheader("⚙️ System Status")
        st.success("✅ Models & Preprocessors Online")
        st.markdown(f"**Target Metric:** `{engine.metadata.get('target_column', 'Churn')}`")
        st.markdown(f"**Total Features:** `{len(engine.metadata.get('encoded_feature_names', []))}`")
        st.markdown(f"**Training Cohort:** `{engine.metadata.get('train_records', 0):,} records`")
        st.markdown("---")
        st.caption("AI-Powered Customer Retention Platform • Built with Python & Scikit-Learn")

    # Main Header
    st.markdown('<div class="main-header">🛡️ Customer Churn Intelligence & Retention Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Executive Insights, Comparative ML Benchmarks, and Prescriptive Customer Retention Interventions</div>', unsafe_allow_html=True)

    # 3 Primary Tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Executive Churn Dashboard",
        "⚖️ Model Comparison (LogReg vs Decision Tree)",
        "🎯 Live Customer Predictor & Action Engine"
    ])

    target_col = engine.metadata.get("target_column", "Churn")

    # =========================================================================
    # TAB 1: EXECUTIVE CHURN DASHBOARD
    # =========================================================================
    with tab1:
        if sample_df is None or target_col not in sample_df.columns:
            st.warning("Data sample could not be loaded for the executive dashboard.")
        else:
            # High-level KPIs
            total_customers = len(sample_df)
            churned_count = int((sample_df[target_col] == 1).sum())
            retained_count = total_customers - churned_count
            churn_rate = (churned_count / total_customers) * 100
            retention_rate = 100 - churn_rate

            spend_col = "Total Spend" if "Total Spend" in sample_df.columns else None
            total_revenue_at_risk = sample_df[sample_df[target_col] == 1][spend_col].sum() if spend_col else 0
            total_revenue = sample_df[spend_col].sum() if spend_col else 0

            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            with kpi_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Total Portfolio Analyzed</h3>
                    <p style="color: #38BDF8;">{total_customers:,}</p>
                </div>
                """, unsafe_allow_html=True)
            with kpi_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Churned / At-Risk Cohort</h3>
                    <p style="color: #F87171;">{churned_count:,} <span style="font-size: 1rem; color: #F87171;">({churn_rate:.1f}%)</span></p>
                </div>
                """, unsafe_allow_html=True)
            with kpi_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Overall Retention Rate</h3>
                    <p style="color: #34D399;">{retention_rate:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            with kpi_col4:
                revenue_display = f"${total_revenue_at_risk:,.0f}" if spend_col else f"{churned_count:,} Accounts"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Revenue at Immediate Risk</h3>
                    <p style="color: #FB923C;">{revenue_display}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Row 1 of Charts: Customers by Status & Churn Rate by Segment
            row1_col1, row1_col2 = st.columns([1, 1])

            with row1_col1:
                st.subheader("👥 Customer Status by Contract Segment")
                segment_col = "Contract Length" if "Contract Length" in sample_df.columns else engine.metadata["categorical_features"][0]
                status_df = sample_df.copy()
                status_df["Status"] = status_df[target_col].map({1: "Churned", 0: "Retained"})
                
                fig_status = px.histogram(
                    status_df,
                    x=segment_col,
                    color="Status",
                    barmode="group",
                    color_discrete_map={"Churned": "#EF4444", "Retained": "#10B981"},
                    title=f"Customer Status across {segment_col}",
                    text_auto=True
                )
                fig_status.update_layout(xaxis_title=segment_col, yaxis_title="Customer Count", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_status, use_container_width=True)

            with row1_col2:
                st.subheader("📉 Churn Rate by Subscription Tier")
                tier_col = "Subscription Type" if "Subscription Type" in sample_df.columns else (
                    engine.metadata["categorical_features"][1] if len(engine.metadata["categorical_features"]) > 1 else segment_col
                )
                tier_churn = sample_df.groupby(tier_col)[target_col].agg(["count", "mean"]).reset_index()
                tier_churn["Churn_Rate_%"] = (tier_churn["mean"] * 100).round(1)

                fig_tier = px.bar(
                    tier_churn,
                    x=tier_col,
                    y="Churn_Rate_%",
                    color="Churn_Rate_%",
                    color_continuous_scale="Reds",
                    text="Churn_Rate_%",
                    title=f"Churn Percentage across {tier_col}"
                )
                fig_tier.update_layout(yaxis_title="Churn Rate (%)", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_tier, use_container_width=True)

            # Row 2 of Charts: Segmentation Scatter Plot & Support Escalations
            row2_col1, row2_col2 = st.columns([1.1, 0.9])

            with row2_col1:
                st.subheader("🎯 Customer Value vs. Tenure Risk Mapping")
                scatter_x = "Tenure" if "Tenure" in sample_df.columns else engine.metadata["numerical_features"][0]
                scatter_y = "Total Spend" if "Total Spend" in sample_df.columns else (
                    engine.metadata["numerical_features"][1] if len(engine.metadata["numerical_features"]) > 1 else scatter_x
                )
                sample_scatter = sample_df.sample(min(len(sample_df), 1500), random_state=42).copy()
                sample_scatter["Customer Status"] = sample_scatter[target_col].map({1: "Churned", 0: "Retained"})

                fig_scatter = px.scatter(
                    sample_scatter,
                    x=scatter_x,
                    y=scatter_y,
                    color="Customer Status",
                    color_discrete_map={"Churned": "#EF4444", "Retained": "#10B981"},
                    opacity=0.65,
                    title=f"{scatter_x} vs. {scatter_y} by Churn Status",
                    hover_data=[c for c in ["Age", "Support Calls", "Payment Delay"] if c in sample_scatter.columns]
                )
                fig_scatter.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_scatter, use_container_width=True)

            with row2_col2:
                st.subheader("🚨 Churn Probability by Support Ticket Volume")
                if "Support Calls" in sample_df.columns:
                    support_churn = sample_df.groupby("Support Calls")[target_col].agg(["count", "mean"]).reset_index()
                    support_churn["Churn_Rate_%"] = (support_churn["mean"] * 100).round(1)
                    
                    fig_support = px.line(
                        support_churn,
                        x="Support Calls",
                        y="Churn_Rate_%",
                        markers=True,
                        title="Exponential Churn Risk Surge with Support Calls",
                        line_shape="spline"
                    )
                    fig_support.update_traces(line_color="#DC2626", line_width=3, marker=dict(size=8, color="#991B1B"))
                    fig_support.update_layout(yaxis_title="Churn Rate (%)", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_support, use_container_width=True)
                else:
                    # Alternative numerical feature distribution
                    num_alt = engine.metadata["numerical_features"][0]
                    fig_box = px.box(sample_df, x=target_col, y=num_alt, color=target_col, title=f"{num_alt} Distribution by Churn")
                    fig_box.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_box, use_container_width=True)

    # =========================================================================
    # TAB 2: MODEL COMPARISON (LOGISTIC REGRESSION VS DECISION TREE)
    # =========================================================================
    with tab2:
        st.subheader("⚖️ Side-by-Side Model Benchmarking")
        st.markdown("Rigorous evaluation comparing linear interpretability (**Logistic Regression**) against hierarchical rule-based non-linear partitioning (**Decision Tree Classifier**).")

        metrics_data = engine.metrics
        if not metrics_data:
            st.warning("Performance metrics could not be loaded from `models/metrics.json`.")
        else:
            lr_m = metrics_data.get("Logistic Regression", {})
            dt_m = metrics_data.get("Decision Tree", {})

            # Metric Cards Table
            scorecard_cols = st.columns(5)
            metric_keys = [
                ("accuracy", "Accuracy"),
                ("precision", "Precision"),
                ("recall", "Recall"),
                ("f1", "F1-Score"),
                ("roc_auc", "ROC-AUC")
            ]

            for idx, (m_key, m_label) in enumerate(metric_keys):
                val_lr = lr_m.get(m_key, 0)
                val_dt = dt_m.get(m_key, 0)
                winner = "Logistic Regression" if val_lr > val_dt else ("Decision Tree" if val_dt > val_lr else "Tie")
                diff = abs(val_dt - val_lr)

                with scorecard_cols[idx]:
                    st.metric(
                        label=m_label,
                        value=f"{max(val_lr, val_dt):.3f}",
                        delta=f"LR: {val_lr:.3f} | DT: {val_dt:.3f}"
                    )

            st.markdown("---")

            # Confusion Matrices & Overlaid ROC Curve
            viz_col1, viz_col2 = st.columns([1, 1])

            with viz_col1:
                st.subheader("🔲 Side-by-Side Confusion Matrices")
                cm_tabs = st.tabs(["Logistic Regression CM", "Decision Tree CM"])

                with cm_tabs[0]:
                    cm_lr = np.array(lr_m.get("confusion_matrix", {}).get("matrix", [[0,0],[0,0]]))
                    fig_cm_lr = px.imshow(
                        cm_lr,
                        text_auto=True,
                        color_continuous_scale="Blues",
                        labels=dict(x="Predicted Label", y="True Label", color="Count"),
                        x=["Retained (0)", "Churned (1)"],
                        y=["Retained (0)", "Churned (1)"],
                        title="Logistic Regression Confusion Matrix"
                    )
                    fig_cm_lr.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_cm_lr, use_container_width=True)

                with cm_tabs[1]:
                    cm_dt = np.array(dt_m.get("confusion_matrix", {}).get("matrix", [[0,0],[0,0]]))
                    fig_cm_dt = px.imshow(
                        cm_dt,
                        text_auto=True,
                        color_continuous_scale="Greens",
                        labels=dict(x="Predicted Label", y="True Label", color="Count"),
                        x=["Retained (0)", "Churned (1)"],
                        y=["Retained (0)", "Churned (1)"],
                        title="Decision Tree Confusion Matrix"
                    )
                    fig_cm_dt.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_cm_dt, use_container_width=True)

            with viz_col2:
                st.subheader("📈 Overlaid ROC Curves")
                fig_roc = go.Figure()

                # LR Curve
                roc_lr = lr_m.get("roc_curve", {})
                if roc_lr:
                    fig_roc.add_trace(go.Scatter(
                        x=roc_lr.get("fpr", []),
                        y=roc_lr.get("tpr", []),
                        mode="lines",
                        name=f"Logistic Regression (AUC = {lr_m.get('roc_auc', 0):.3f})",
                        line=dict(color="#2563EB", width=2.5)
                    ))

                # DT Curve
                roc_dt = dt_m.get("roc_curve", {})
                if roc_dt:
                    fig_roc.add_trace(go.Scatter(
                        x=roc_dt.get("fpr", []),
                        y=roc_dt.get("tpr", []),
                        mode="lines",
                        name=f"Decision Tree (AUC = {dt_m.get('roc_auc', 0):.3f})",
                        line=dict(color="#059669", width=2.5, dash="dash")
                    ))

                # Diagonal Reference line
                fig_roc.add_trace(go.Scatter(
                    x=[0, 1], y=[0, 1],
                    mode="lines",
                    name="Random Baseline (AUC = 0.500)",
                    line=dict(color="#94A3B8", dash="dot")
                ))

                fig_roc.update_layout(
                    title="Receiver Operating Characteristic (ROC) Benchmark",
                    xaxis_title="False Positive Rate (1 - Specificity)",
                    yaxis_title="True Positive Rate (Sensitivity / Recall)",
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(yanchor="bottom", y=0.05, xanchor="right", x=0.95)
                )
                st.plotly_chart(fig_roc, use_container_width=True)

            # Feature Importance Section
            st.markdown("---")
            st.subheader("🏆 Key Churn Predictors & Feature Drivers")
            fi_col1, fi_col2 = st.columns([1, 1])

            with fi_col1:
                st.markdown("**Logistic Regression (Log-Odds Coefficients)**")
                lr_fi = lr_m.get("feature_importance", [])[:8]
                df_lr_fi = pd.DataFrame(lr_fi)
                if not df_lr_fi.empty:
                    fig_lr_fi = px.bar(
                        df_lr_fi,
                        x="importance",
                        y="feature",
                        orientation="h",
                        color="impact",
                        color_discrete_map={"Increases Churn": "#EF4444", "Decreases Churn": "#10B981"},
                        title="Top Coefficients Influencing Churn Probability"
                    )
                    fig_lr_fi.update_layout(yaxis=dict(autorange="reversed"), template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_lr_fi, use_container_width=True)

            with fi_col2:
                st.markdown("**Decision Tree (Gini Feature Importance)**")
                dt_fi = dt_m.get("feature_importance", [])[:8]
                df_dt_fi = pd.DataFrame(dt_fi)
                if not df_dt_fi.empty:
                    fig_dt_fi = px.bar(
                        df_dt_fi,
                        x="importance",
                        y="feature",
                        orientation="h",
                        color="importance",
                        color_continuous_scale="Teal",
                        title="Decision Tree Gini Split Relevance"
                    )
                    fig_dt_fi.update_layout(yaxis=dict(autorange="reversed"), template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_dt_fi, use_container_width=True)

            # Decision Tree Rules Summary
            tree_rules = dt_m.get("tree_rules_summary")
            if tree_rules:
                with st.expander("🌲 Inspect Decision Tree Hierarchical Split Rules (Top 3 Levels)"):
                    st.code(tree_rules, language="text")

    # =========================================================================
    # TAB 3: LIVE CUSTOMER PREDICTOR & RETENTION ENGINE
    # =========================================================================
    with tab3:
        st.subheader("🎯 Real-Time Customer Churn Risk Predictor")
        st.markdown("Simulate an existing or prospective customer profile, calculate real-time churn risk, and trigger an automated retention strategy.")

        # Top Bar Controls: Model Picker & Random Customer Simulator
        ctrl_col1, ctrl_col2 = st.columns([2, 1])
        with ctrl_col1:
            selected_model_option = st.radio(
                "Select Active Scoring Model:",
                ["Logistic Regression", "Decision Tree", "Side-by-Side Comparison"],
                horizontal=True
            )
        with ctrl_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            simulate_btn = st.button("🎲 Simulate Random Customer Profile", help="Load sample data from a real customer record")

        # Session state for form defaults
        metadata = engine.metadata
        num_features = metadata.get("numerical_features", [])
        cat_features = metadata.get("categorical_features", [])
        stats = metadata.get("feature_stats", {})
        cats = metadata.get("categorical_unique", {})

        if "customer_input_state" not in st.session_state:
            st.session_state.customer_input_state = {}

        if simulate_btn and sample_df is not None:
            random_row = sample_df.sample(1, random_state=int(np.random.randint(1, 10000))).iloc[0].to_dict()
            for col in num_features + cat_features:
                if col in random_row:
                    st.session_state.customer_input_state[col] = random_row[col]
            st.success("Loaded randomized customer record!")

        # Dynamic Input Form
        st.markdown("#### Customer Attributes")
        input_data = {}

        # Divide numerical and categorical features into responsive columns
        form_cols = st.columns(3)

        # Numerical Sliders / Number Inputs
        for idx, feat in enumerate(num_features):
            col_target = form_cols[idx % 3]
            feat_min = float(stats.get(feat, {}).get("min", 0.0))
            feat_max = float(stats.get(feat, {}).get("max", 100.0))
            feat_default = float(stats.get(feat, {}).get("default", (feat_min + feat_max) / 2))

            # Retrieve from session state if set
            current_val = float(st.session_state.customer_input_state.get(feat, feat_default))
            current_val = max(feat_min, min(feat_max, current_val))

            # Determine if integer or float
            is_int = (feat_min.is_integer() and feat_max.is_integer())

            with col_target:
                if is_int:
                    input_data[feat] = st.slider(
                        label=feat,
                        min_value=int(feat_min),
                        max_value=int(feat_max),
                        value=int(current_val),
                        step=1,
                        key=f"input_{feat}"
                    )
                else:
                    input_data[feat] = st.slider(
                        label=feat,
                        min_value=feat_min,
                        max_value=feat_max,
                        value=round(current_val, 2),
                        step=0.1,
                        key=f"input_{feat}"
                    )

        # Categorical Selectboxes
        for idx, feat in enumerate(cat_features):
            col_target = form_cols[(len(num_features) + idx) % 3]
            unique_options = cats.get(feat, ["Standard"])
            saved_val = str(st.session_state.customer_input_state.get(feat, unique_options[0]))
            default_index = unique_options.index(saved_val) if saved_val in unique_options else 0

            with col_target:
                input_data[feat] = st.selectbox(
                    label=feat,
                    options=unique_options,
                    index=default_index,
                    key=f"input_{feat}"
                )

        st.markdown("<br>", unsafe_allow_html=True)
        predict_trigger = st.button("🔍 Calculate Churn Risk & Retention Plan", type="primary", use_container_width=True)

        if predict_trigger or True:  # Instant reactive evaluation
            res = engine.predict_single(input_data, model_name=selected_model_option)

            st.markdown("---")
            st.subheader("📊 Churn Risk Assessment Result")

            res_col1, res_col2 = st.columns([1, 1.2])

            with res_col1:
                st.markdown(f"### Assessment: <span style='color: {res['risk_color']};'>{res['badge_icon']} {res['risk_level']}</span>", unsafe_allow_html=True)
                
                # Interactive Plotly Gauge Chart
                prob_val = res["probability_pct"]
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob_val,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': f"Churn Probability ({res['selected_model']})", 'font': {'size': 18, 'color': '#F8FAFC'}},
                    number={'suffix': "%", 'font': {'size': 36, 'color': res['risk_color']}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
                        'bar': {'color': res['risk_color'], 'thickness': 0.3},
                        'bgcolor': "#1E293B",
                        'borderwidth': 1,
                        'bordercolor': "#334155",
                        'steps': [
                            {'range': [0, 35], 'color': 'rgba(16, 185, 129, 0.25)'},
                            {'range': [35, 65], 'color': 'rgba(245, 158, 11, 0.25)'},
                            {'range': [65, 100], 'color': 'rgba(239, 68, 68, 0.25)'}
                        ],
                        'threshold': {
                            'line': {'color': "#EF4444", 'width': 4},
                            'thickness': 0.75,
                            'value': prob_val
                        }
                    }
                ))
                fig_gauge.update_layout(
                    height=260,
                    margin=dict(l=20, r=20, t=40, b=10),
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_gauge, use_container_width=True)

                if selected_model_option == "Side-by-Side Comparison":
                    sub_col1, sub_col2 = st.columns(2)
                    with sub_col1:
                        st.markdown(f"**Logistic Regression:** `{res['logistic_regression']['probability_pct']}%`")
                    with sub_col2:
                        st.markdown(f"**Decision Tree:** `{res['decision_tree']['probability_pct']}%`")

            with res_col2:
                st.markdown("### 📋 Prescriptive Customer Retention Action Plan")
                st.markdown("Automated algorithmic recommendations tailored to address the primary churn drivers detected in this profile:")

                action_items = res["action_plan"]
                for item in action_items:
                    st.markdown(f"""
                    <div class="action-card">
                        <div class="action-title">💡 {item['title']}</div>
                        <div class="action-meta"><strong>Driver:</strong> {item['trigger']} &nbsp;|&nbsp; <strong>Urgency:</strong> <span style="color: #F87171; font-weight:600;">{item['urgency']}</span></div>
                        <div style="font-size: 0.92rem; color: #CBD5E1;"><strong>Recommended Action:</strong> {item['action']}</div>
                        <div style="font-size: 0.85rem; color: #34D399; margin-top: 0.3rem;"><strong>Expected ROI Impact:</strong> {item['expected_impact']}</div>
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
