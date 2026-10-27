"""
src/predict.py
Inference logic, risk scoring, and automated Customer Retention Engine.
Generates actionable, prioritized business retention strategies based on
individual customer risk drivers.
"""

import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

# Force UTF-8 stdout encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

class ChurnRetentionEngine:
    def __init__(self, models_dir: Path = MODELS_DIR):
        self.models_dir = Path(models_dir)
        self.preprocessor = None
        self.lr_model = None
        self.dt_model = None
        self.metadata = None
        self.metrics = None
        self._load_artifacts()

    def _load_artifacts(self):
        """Loads preprocessor, trained models, and metadata."""
        prep_path = self.models_dir / "preprocessor.pkl"
        lr_path = self.models_dir / "logistic_regression.pkl"
        dt_path = self.models_dir / "decision_tree.pkl"
        meta_path = self.models_dir / "feature_metadata.json"
        metrics_path = self.models_dir / "metrics.json"

        if prep_path.exists():
            self.preprocessor = joblib.load(prep_path)
        if lr_path.exists():
            self.lr_model = joblib.load(lr_path)
        if dt_path.exists():
            self.dt_model = joblib.load(dt_path)
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
        if metrics_path.exists():
            with open(metrics_path, "r", encoding="utf-8") as f:
                self.metrics = json.load(f)

    def is_ready(self) -> bool:
        """Returns True if all required artifacts are loaded."""
        return (
            self.preprocessor is not None
            and self.lr_model is not None
            and self.dt_model is not None
            and self.metadata is not None
        )

    def get_model(self, model_name: str):
        if "logistic" in model_name.lower():
            return self.lr_model
        return self.dt_model

    def predict_single(self, customer_input: dict, model_name: str = "Logistic Regression") -> dict:
        """
        Runs inference on a single customer dictionary and yields:
        - Predicted churn label (0 = Retained, 1 = Churned)
        - Probability (%)
        - Risk Tier (Low, Moderate, High)
        - Side-by-side probabilities for both models
        - Tailored Retention Action Plan
        """
        if not self.is_ready():
            raise RuntimeError("ChurnRetentionEngine is not fully initialized. Models or preprocessors missing.")

        input_df = pd.DataFrame([customer_input])
        
        # Ensure numeric columns are cast properly
        for col in self.metadata["numerical_features"]:
            if col in input_df.columns:
                input_df[col] = pd.to_numeric(input_df[col], errors="coerce")
                if input_df[col].isnull().any():
                    input_df[col] = input_df[col].fillna(self.metadata["feature_stats"][col]["median"])

        # Preprocess features
        X_trans = self.preprocessor.transform(input_df)

        # Probabilities
        prob_lr = float(self.lr_model.predict_proba(X_trans)[0, 1])
        prob_dt = float(self.dt_model.predict_proba(X_trans)[0, 1])
        pred_lr = int(self.lr_model.predict(X_trans)[0])
        pred_dt = int(self.dt_model.predict(X_trans)[0])

        active_prob = prob_lr if "logistic" in model_name.lower() else prob_dt
        active_pred = pred_lr if "logistic" in model_name.lower() else pred_dt

        # Risk Classification
        if active_prob >= 0.65:
            risk_level = "High Churn Risk"
            risk_color = "#F43F5E"  # Muted Coral/Crimson
            badge_icon = ""
        elif active_prob >= 0.35:
            risk_level = "Moderate Churn Risk"
            risk_color = "#F59E0B"  # Muted Amber
            badge_icon = ""
        else:
            risk_level = "Low Churn Risk"
            risk_color = "#10B981"  # Muted Emerald
            badge_icon = ""

        # Generate Action Plan
        action_plan = self.generate_retention_recommendations(customer_input, active_prob)

        return {
            "prediction": active_pred,
            "probability": active_prob,
            "probability_pct": round(active_prob * 100, 1),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "badge_icon": badge_icon,
            "selected_model": model_name,
            "logistic_regression": {
                "prediction": pred_lr,
                "probability_pct": round(prob_lr * 100, 1)
            },
            "decision_tree": {
                "prediction": pred_dt,
                "probability_pct": round(prob_dt * 100, 1)
            },
            "action_plan": action_plan
        }

    def generate_retention_recommendations(self, customer_input: dict, churn_prob: float) -> list:
        """
        Dynamically analyzes customer features and produces tailored retention actions.
        """
        recommendations = []
        stats = self.metadata.get("feature_stats", {})

        # 1. Support Calls Analysis
        support_calls = float(customer_input.get("Support Calls", 0))
        if support_calls >= 4:
            recommendations.append({
                "title": "Immediate Customer Success Escalation",
                "trigger": f"High Support Ticket Volume ({int(support_calls)} calls recorded)",
                "urgency": "Immediate (Within 24 Hours)",
                "action": "Assign a Tier-3 Senior Customer Success Manager to schedule an executive resolution call. Expedite pending tickets and provide a personalized platform walkthrough.",
                "expected_impact": "Reduces customer frustration churn by ~35%."
            })

        # 2. Payment Delay Analysis
        delay = float(customer_input.get("Payment Delay", 0))
        if delay >= 10:
            recommendations.append({
                "title": "Billing Friction & Flexible Payment Assistance",
                "trigger": f"Extended Payment Delay ({int(delay)} days overdue)",
                "urgency": "High Priority",
                "action": "Offer automated invoice grace-period restructuring, or a 5% monthly billing discount upon enrolling in automated credit card/ACH auto-pay.",
                "expected_impact": "Resolves payment-induced involuntary churn by ~45%."
            })

        # 3. Contract Type Analysis
        contract = str(customer_input.get("Contract Length", "")).strip().lower()
        if "month" in contract:
            recommendations.append({
                "title": "Annual Contract Lock-in Incentive",
                "trigger": "Customer is on Month-to-Month commitment (Highest attrition segment)",
                "urgency": "High Priority",
                "action": "Extend an exclusive retention promotion: Upgrade to a 12-month annual contract with 2 free months or a 20% discount plus free premium tier features.",
                "expected_impact": "Increases customer lifetime value and reduces month-to-month churn risk."
            })

        # 4. Usage Frequency Analysis
        usage = float(customer_input.get("Usage Frequency", 0))
        usage_median = stats.get("Usage Frequency", {}).get("median", 15)
        if usage < usage_median * 0.7:
            recommendations.append({
                "title": "Automated Re-engagement & Value Realization",
                "trigger": f"Low Platform Usage Frequency ({usage:.0f} sessions/month vs cohort median {usage_median:.0f})",
                "urgency": "Medium Priority",
                "action": "Trigger an automated smart drip email campaign highlighting underutilized high-value features, accompanied by a 15-minute quick-start consultation booking link.",
                "expected_impact": "Boosts product stickiness and daily active usage."
            })

        # 5. High Spend / VIP Protection
        total_spend = float(customer_input.get("Total Spend", 0))
        spend_median = stats.get("Total Spend", {}).get("median", 500)
        if total_spend >= spend_median * 1.3 and churn_prob >= 0.40:
            recommendations.append({
                "title": "VIP High-Value Customer Retention Concierge",
                "trigger": f"High Customer Spend (${total_spend:,.2f}) at imminent risk of departure",
                "urgency": "Immediate (Highest Revenue Impact)",
                "action": "Dispatch an executive loyalty gift, invite to quarterly product advisory council, and provide direct 24/7 priority support hotline access.",
                "expected_impact": "Protects top-line recurring revenue and prevents high-tier account loss."
            })

        # 6. Interaction Recency
        last_inter = float(customer_input.get("Last Interaction", 0))
        if last_inter >= 20:
            recommendations.append({
                "title": "Proactive Health Check-in",
                "trigger": f"Inactivity Gap ({int(last_inter)} days since last communication)",
                "urgency": "Medium Priority",
                "action": "Send a lightweight 'How can we help your team win?' pulse survey with a $25 coffee voucher upon completion to rekindle connection.",
                "expected_impact": "Re-establishes customer dialogue before total attrition."
            })

        # Fallback if no specific trigger fired but overall risk is high
        if not recommendations and churn_prob >= 0.50:
            recommendations.append({
                "title": "Proactive Account Optimization Review",
                "trigger": "Model-identified multi-factor churn risk profile",
                "urgency": "High Priority",
                "action": "Conduct an end-to-end account audit to review usage trends, eliminate unused add-ons, and right-size service tier.",
                "expected_impact": "Realigns product value proposition with customer needs."
            })
        elif not recommendations:
            recommendations.append({
                "title": "Sustain Healthy Customer Engagement",
                "trigger": "Customer demonstrates positive retention indicators",
                "urgency": "Standard Cadence",
                "action": "Continue regular product release newsletters, celebrate milestone renewals, and explore referral incentive program participation.",
                "expected_impact": "Maintains NPS satisfaction above 90%."
            })

        return recommendations

    def predict_batch(self, df: pd.DataFrame, model_name: str = "Logistic Regression") -> pd.DataFrame:
        """Performs batch prediction on a dataframe and adds prediction columns."""
        if not self.is_ready():
            raise RuntimeError("Engine artifacts not loaded.")

        res_df = df.copy()
        model = self.get_model(model_name)
        X_trans = self.preprocessor.transform(res_df)

        probs = model.predict_proba(X_trans)[:, 1]
        preds = model.predict(X_trans)

        res_df["Churn_Predicted"] = preds
        res_df["Churn_Probability_Pct"] = (probs * 100).round(1)
        res_df["Risk_Category"] = np.where(
            probs >= 0.65, "High Risk",
            np.where(probs >= 0.35, "Moderate Risk", "Low Risk")
        )
        return res_df

# Quick testing interface
if __name__ == "__main__":
    engine = ChurnRetentionEngine()
    if engine.is_ready():
        sample_cust = {
            "Age": 45,
            "Gender": "Female",
            "Tenure": 12,
            "Usage Frequency": 6,
            "Support Calls": 5,
            "Payment Delay": 14,
            "Subscription Type": "Basic",
            "Contract Length": "Monthly",
            "Total Spend": 650.0,
            "Last Interaction": 22
        }
        res = engine.predict_single(sample_cust)
        print("Inference Result Preview:")
        print(f"Risk: {res['risk_level']} ({res['probability_pct']}%)")
        print("Action Plan Items:", len(res["action_plan"]))
    else:
        print("Engine models not trained yet.")
