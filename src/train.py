"""
src/train.py
Trains Logistic Regression & Decision Tree classifiers,
evaluates performance metrics, computes feature importances,
and exports models and metrics.json.
"""

import json
import sys
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)
import joblib

# Force UTF-8 stdout encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

def sample_roc_curve(fpr, tpr, max_points=100):
    """Subsamples ROC curve coordinates for lightweight JSON storage."""
    if len(fpr) <= max_points:
        return [float(x) for x in fpr], [float(y) for y in tpr]
    indices = np.linspace(0, len(fpr) - 1, max_points, dtype=int)
    return [float(fpr[i]) for i in indices], [float(tpr[i]) for i in indices]

def train_and_evaluate():
    print("=" * 70)
    print("🚀 MODEL TRAINING & BENCHMARKING PIPELINE")
    print("=" * 70)

    # Load preprocessed data and metadata
    data_file = MODELS_DIR / "processed_data.pkl"
    meta_file = MODELS_DIR / "feature_metadata.json"

    if not data_file.exists() or not meta_file.exists():
        print("⚠️ Preprocessed data not found. Running preprocessing first...")
        from src.preprocess import run_preprocessing
        run_preprocessing()

    processed_data = joblib.load(data_file)
    with open(meta_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    X_train = processed_data["X_train"]
    X_test = processed_data["X_test"]
    y_train = processed_data["y_train"]
    y_test = processed_data["y_test"]
    feature_names = metadata["encoded_feature_names"]

    print(f"Dataset shapes: X_train={X_train.shape}, X_test={X_test.shape}")
    print(f"Encoded features count: {len(feature_names)}")

    # 1. Model 1: Logistic Regression
    print("\n[1/2] 📈 Training Logistic Regression (class_weight='balanced', max_iter=1000)...")
    lr = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
        solver="lbfgs"
    )
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    y_prob_lr = lr.predict_proba(X_test)[:, 1]

    # Metrics for Logistic Regression
    cm_lr = confusion_matrix(y_test, y_pred_lr)
    fpr_lr, tpr_lr, _ = roc_curve(y_test, y_prob_lr)
    fpr_lr_s, tpr_lr_s = sample_roc_curve(fpr_lr, tpr_lr)

    lr_coefs = lr.coef_[0]
    lr_importance = [
        {
            "feature": feat,
            "importance": float(coef),
            "abs_importance": float(abs(coef)),
            "impact": "Increases Churn" if coef > 0 else "Decreases Churn"
        }
        for feat, coef in zip(feature_names, lr_coefs)
    ]
    lr_importance = sorted(lr_importance, key=lambda x: x["abs_importance"], reverse=True)

    metrics_lr = {
        "accuracy": float(accuracy_score(y_test, y_pred_lr)),
        "precision": float(precision_score(y_test, y_pred_lr, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred_lr, zero_division=0)),
        "f1": float(f1_score(y_test, y_pred_lr, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_prob_lr)),
        "confusion_matrix": {
            "tn": int(cm_lr[0, 0]),
            "fp": int(cm_lr[0, 1]),
            "fn": int(cm_lr[1, 0]),
            "tp": int(cm_lr[1, 1]),
            "matrix": cm_lr.tolist()
        },
        "roc_curve": {"fpr": fpr_lr_s, "tpr": tpr_lr_s},
        "feature_importance": lr_importance
    }

    # 2. Model 2: Decision Tree Classifier
    print("\n[2/2] 🌲 Training Decision Tree Classifier (max_depth=6, min_samples_split=20, balanced)...")
    dt = DecisionTreeClassifier(
        max_depth=6,
        min_samples_split=20,
        class_weight="balanced",
        random_state=42
    )
    dt.fit(X_train, y_train)
    y_pred_dt = dt.predict(X_test)
    y_prob_dt = dt.predict_proba(X_test)[:, 1]

    # Metrics for Decision Tree
    cm_dt = confusion_matrix(y_test, y_pred_dt)
    fpr_dt, tpr_dt, _ = roc_curve(y_test, y_prob_dt)
    fpr_dt_s, tpr_dt_s = sample_roc_curve(fpr_dt, tpr_dt)

    dt_importances = dt.feature_importances_
    dt_importance = [
        {
            "feature": feat,
            "importance": float(imp),
            "abs_importance": float(imp),
            "impact": "Key Decision Split Driver"
        }
        for feat, imp in zip(feature_names, dt_importances)
    ]
    dt_importance = sorted(dt_importance, key=lambda x: x["abs_importance"], reverse=True)

    tree_rules_text = export_text(dt, feature_names=feature_names, max_depth=3)

    metrics_dt = {
        "accuracy": float(accuracy_score(y_test, y_pred_dt)),
        "precision": float(precision_score(y_test, y_pred_dt, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred_dt, zero_division=0)),
        "f1": float(f1_score(y_test, y_pred_dt, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_prob_dt)),
        "confusion_matrix": {
            "tn": int(cm_dt[0, 0]),
            "fp": int(cm_dt[0, 1]),
            "fn": int(cm_dt[1, 0]),
            "tp": int(cm_dt[1, 1]),
            "matrix": cm_dt.tolist()
        },
        "roc_curve": {"fpr": fpr_dt_s, "tpr": tpr_dt_s},
        "feature_importance": dt_importance,
        "tree_rules_summary": tree_rules_text
    }

    # Consolidated metrics export
    all_metrics = {
        "Logistic Regression": metrics_lr,
        "Decision Tree": metrics_dt
    }

    # Save models and metrics
    joblib.dump(lr, MODELS_DIR / "logistic_regression.pkl")
    joblib.dump(dt, MODELS_DIR / "decision_tree.pkl")
    with open(MODELS_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(all_metrics, f, indent=4)

    print("\n" + "=" * 70)
    print("📊 MODEL PERFORMANCE BENCHMARK")
    print("=" * 70)
    print(f"{'Metric':<15} | {'Logistic Regression':<22} | {'Decision Tree':<15}")
    print("-" * 60)
    for m in ["accuracy", "precision", "recall", "f1", "roc_auc"]:
        val_lr = metrics_lr[m]
        val_dt = metrics_dt[m]
        print(f"{m.capitalize():<15} | {val_lr:<22.4f} | {val_dt:<15.4f}")

    print("\n🏆 Top Churn Predictors (Logistic Regression):")
    for item in lr_importance[:5]:
        print(f"   - {item['feature']:<25}: coef={item['importance']:+.4f} ({item['impact']})")

    print("\n🏆 Top Churn Predictors (Decision Tree Gini Importance):")
    for item in dt_importance[:5]:
        print(f"   - {item['feature']:<25}: importance={item['importance']:.4f}")

    print(f"\n✅ Trained models and metrics exported successfully to {MODELS_DIR}")
    return lr, dt, all_metrics

if __name__ == "__main__":
    train_and_evaluate()
