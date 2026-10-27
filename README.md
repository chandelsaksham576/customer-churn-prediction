# 🛡️ Customer Churn Intelligence & Retention Dashboard

An enterprise-grade, end-to-end Machine Learning and Business Intelligence platform built in Python to predict customer churn, benchmark algorithmic performance, and deliver prescriptive, actionable customer retention interventions.

---

## 📌 Executive Summary
Customer churn presents a critical threat to enterprise top-line recurring revenue and Customer Lifetime Value (LTV). This application bridges the gap between predictive data science and executive decision-making by:
1. **Predicting Customer Churn:** Identifying which subscribers are at risk before cancellation happens.
2. **Benchmarking Interpretable Algorithms:** Comparing **Logistic Regression** (linear log-odds coefficients) against a **Decision Tree Classifier** (hierarchical rule-based partitioning).
3. **Prescriptive Action Engine:** Automatically generating prioritized, dollar-impact customer retention recommendations (e.g., annual contract upgrade incentives, VIP loyalty concierge, support ticket escalations).

---

## 🗂️ Project Directory Structure

```text
customer-churn-prediction/
├── data/
│   ├── raw/                 # Extracted CSV dataset(s) from Kaggle .zip
│   └── extract_data.py      # Auto-detects and extracts any .zip archive & prints schema
├── models/                  # Serialized models, preprocessors, feature metadata, and metrics.json
│   ├── preprocessor.pkl
│   ├── logistic_regression.pkl
│   ├── decision_tree.pkl
│   ├── feature_metadata.json
│   └── metrics.json
├── notebooks/
│   └── eda_report.py        # Executive exploratory data analysis & statistical summaries
├── src/
│   ├── preprocess.py        # Data cleaning, dynamic schema handling, encoding, scaling, stratified split
│   ├── train.py             # Trains Logistic Regression & Decision Tree; exports benchmark metrics
│   └── predict.py           # Inference engine, risk scoring, and tailored retention action generator
├── app.py                   # Full interactive Streamlit Dashboard with 3 tabs
├── requirements.txt         # Production dependencies
└── README.md                # System documentation
```

---

## ⚙️ Dataset Schema & Dynamic Adaptability

The pipeline automatically detects and processes Kaggle churn datasets (Telco, Banking, E-Commerce, or Subscription Services):
- **Target Column:** Automatically identified (`Churn`, `Exited`, `target`, etc.) and mapped to binary `0` (Retained) and `1` (Churned).
- **Identifier Columns:** Non-predictive columns (`CustomerID`, `RowNumber`, `Surname`, etc.) are dropped.
- **Categorical Features:** Processed via `OneHotEncoder(handle_unknown='ignore')`.
- **Numerical Features:** Imputed with median and scaled via `StandardScaler()`.
- **Train/Test Split:** Stratified 80/20 train/test split to preserve natural class balance.

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- Python 3.10+
- Dedicated virtual environment recommended

### 2. Environment Setup
```bash
# Clone or navigate into the project directory
cd customer-churn-prediction

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Step-by-Step Execution

#### Step 1: Extract & Inspect Dataset
```bash
python data/extract_data.py
```
*Auto-locates the `.zip` archive, unpacks the CSV files into `data/raw/`, and displays shapes, data types, null counts, and head rows.*

#### Step 2: Run Exploratory Data Analysis (EDA)
```bash
python notebooks/eda_report.py
```
*Outputs cohort churn rates, numerical distributions, correlations, and executive business takeaways.*

#### Step 3: Run Preprocessing Pipeline
```bash
python src/preprocess.py
```
*Cleans data, builds the `ColumnTransformer` preprocessor pipeline, and saves serialized preprocessors and metadata in `models/`.*

#### Step 4: Train & Benchmark ML Models
```bash
python src/train.py
```
*Trains both `LogisticRegression(class_weight='balanced')` and `DecisionTreeClassifier(max_depth=6)`, evaluating Accuracy, Precision, Recall, F1-Score, ROC-AUC, Confusion Matrices, and Feature Importances into `models/metrics.json`.*

#### Step 5: Launch the Streamlit Web Application
```bash
streamlit run app.py
```

---

## 🖥️ Interactive Web Dashboard Features

### Tab 1: Executive Churn Dashboard
- **Top KPI Cards:** Total customers analyzed, churned customer count, portfolio retention rate, and total revenue/balance at risk.
- **Interactive Plotly Visualizations:**
  - Status breakdown across contract segments.
  - Churn rate across subscription tiers.
  - Multi-dimensional customer value vs. tenure scatter plot with churn overlay.
  - Churn probability surge vs. support ticket escalation volume.

### Tab 2: Model Comparison (LogReg vs. Decision Tree)
- **Scorecard:** Direct side-by-side comparison of Accuracy, Precision, Recall, F1, and ROC-AUC.
- **Confusion Matrices:** Interactive heatmaps for both models showing True Positives, False Positives, False Negatives, and True Negatives.
- **ROC Curve Overlay:** Multi-model ROC curves with AUC score badges.
- **Feature Importance:** Top predictors driving churn (Log-Odds coefficients vs. Decision Tree Gini importance).
- **Tree Split Rules:** Expandable view of hierarchical decision rules.

### Tab 3: Live Customer Predictor & Retention Engine
- **Dynamic Controls:** Responsive sliders for numeric features and dropdown menus for categorical features based on the actual dataset schema.
- **1-Click Profile Simulator:** "Simulate Random Customer Profile" button to instantly test against real historical customer profiles.
- **Interactive Gauge Chart:** Real-time Churn Probability percentage gauge with dynamic color thresholds (Green: Low, Amber: Moderate, Red: High Risk).
- **Tailored Retention Action Plan:** Automated, prioritized retention playbooks (e.g. VIP Concierge Outreach, 20% Annual Contract Upgrade, Auto-pay Billing Restructuring).

---

## 📈 Tech Stack
- **Data Engineering:** `pandas`, `numpy`
- **Machine Learning:** `scikit-learn`, `joblib`
- **Interactive Visualizations:** `plotly`
- **Web Application:** `streamlit`
