import os
os.environ['MPLCONFIGDIR'] = r"C:\Users\chand\.gemini\antigravity\scratch\customer-churn-prediction\.mplconfig"
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

fig_dir = r"C:\Users\chand\.gemini\antigravity\scratch\customer-churn-prediction\reports\figures"
os.makedirs(fig_dir, exist_ok=True)

# Set global matplotlib styles for clean academic plots
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

# 1. Figure 3.1: Block Diagram Architecture
fig, ax = plt.subplots(figsize=(8, 5))
ax.axis('off')
boxes = [
    ("Kaggle Customer Churn Dataset\n(440,833 records, 11 features)", 0.5, 0.9, 0.7, 0.12, "#E0E7FF"),
    ("Automated Preprocessing & Pipeline\n(Drop ID, Median Imputer, OneHotEncoder, StandardScaler)", 0.5, 0.72, 0.75, 0.12, "#EDE9FE"),
    ("Model Training & Benchmark\n(Logistic Regression vs. Decision Tree)", 0.5, 0.54, 0.7, 0.12, "#FEF3C7"),
    ("Evaluation & Model Serialization\n(Metrics JSON, models/*.pkl)", 0.5, 0.36, 0.7, 0.12, "#DCFCE7"),
    ("Interactive Streamlit Cloud Dashboard\n(Overview, Benchmark, Risk Inference & Retention Playbooks)", 0.5, 0.18, 0.8, 0.12, "#FCE7F3")
]
for text, x, y, w, h, col in boxes:
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.01", facecolor=col, edgecolor='#374151', linewidth=1.5, zorder=2)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#111827', zorder=3)

for i in range(len(boxes) - 1):
    y_start = boxes[i][2] - boxes[i][4]/2
    y_end = boxes[i+1][2] + boxes[i+1][4]/2
    ax.annotate('', xy=(0.5, y_end), xytext=(0.5, y_start),
                arrowprops=dict(facecolor='#4B5563', edgecolor='#4B5563', width=1.5, headwidth=7), zorder=1)

plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "fig_3_1_system_architecture.png"), bbox_inches='tight')
plt.close()
print("Generated Fig 3.1")

# 2. Figure 5.1: Class Distribution
fig, ax = plt.subplots(figsize=(6, 4))
classes = ['Retained (0)', 'Churned (1)']
counts = [190833, 249999]
pcts = [43.29, 56.71]
colors = ['#10B981', '#F43F5E']
bars = ax.bar(classes, counts, color=colors, width=0.45, edgecolor='#1F2937', linewidth=1)
for bar, pct, cnt in zip(bars, pcts, counts):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 5000, f"{cnt:,}\n({pct}%)", ha='center', va='bottom', fontsize=9.5, fontweight='bold')
ax.set_ylim(0, 300000)
ax.set_ylabel("Customer Count", fontsize=10, fontweight='bold')
ax.set_title("Customer Churn Class Distribution (440,833 Records)", fontsize=11, fontweight='bold', pad=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "fig_5_1_class_distribution.png"), bbox_inches='tight')
plt.close()
print("Generated Fig 5.1")

# 3. Figure 5.2: Churn by Contract Length
fig, ax = plt.subplots(figsize=(6, 4))
contracts = ['Annual', 'Quarterly', 'Monthly']
churn_rates = [46.08, 46.03, 100.00]
colors = ['#6366F1', '#8B5CF6', '#EF4444']
bars = ax.bar(contracts, churn_rates, color=colors, width=0.45, edgecolor='#1F2937', linewidth=1)
for bar, rate in zip(bars, churn_rates):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{rate:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_ylim(0, 115)
ax.set_ylabel("Churn Rate (%)", fontsize=10, fontweight='bold')
ax.set_title("Historical Churn Rate by Contract Length", fontsize=11, fontweight='bold', pad=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "fig_5_2_contract_churn.png"), bbox_inches='tight')
plt.close()
print("Generated Fig 5.2")

# 4. Figure 5.3: Feature Correlation
fig, ax = plt.subplots(figsize=(7, 4))
features = ['Support Calls', 'Payment Delay', 'Age', 'Usage Frequency', 'Tenure', 'Last Interaction', 'Total Spend']
corrs = [0.5743, 0.3121, 0.2184, -0.0461, -0.0682, -0.0984, -0.4294]
bar_colors = ['#EF4444' if c > 0 else '#10B981' for c in corrs]
bars = ax.barh(features[::-1], corrs[::-1], color=bar_colors[::-1], edgecolor='#1F2937', linewidth=1, height=0.55)
for bar, val in zip(bars, corrs[::-1]):
    xpos = val + 0.02 if val >= 0 else val - 0.08
    ax.text(xpos, bar.get_y() + bar.get_height()/2, f"{val:+.3f}", va='center', fontsize=9, fontweight='bold')
ax.axvline(0, color='#374151', linewidth=1)
ax.set_xlim(-0.6, 0.75)
ax.set_xlabel("Pearson Correlation Coefficient with Churn Target", fontsize=9.5, fontweight='bold')
ax.set_title("Correlation of Numerical Attributes with Customer Churn", fontsize=11, fontweight='bold', pad=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "fig_5_3_correlation.png"), bbox_inches='tight')
plt.close()
print("Generated Fig 5.3")

# 5. Figure 5.4: Model Comparison
fig, ax = plt.subplots(figsize=(7, 4))
metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
lr_scores = [89.85, 94.10, 87.59, 90.73, 96.05]
dt_scores = [97.95, 100.00, 96.39, 98.16, 98.66]
x = np.arange(len(metrics))
width = 0.35
rects1 = ax.bar(x - width/2, lr_scores, width, label='Logistic Regression', color='#64748B', edgecolor='#1E293B')
rects2 = ax.bar(x + width/2, dt_scores, width, label='Decision Tree Classifier', color='#10B981', edgecolor='#064E3B')
ax.set_ylabel('Score (%)', fontsize=10, fontweight='bold')
ax.set_title('Hold-out Test Set Performance Benchmark (20,000 Samples)', fontsize=11, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=9.5, fontweight='bold')
ax.set_ylim(75, 105)
ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for rect in rects1:
    h = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, h + 0.6, f"{h:.1f}", ha='center', va='bottom', fontsize=8)
for rect in rects2:
    h = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, h + 0.6, f"{h:.1f}", ha='center', va='bottom', fontsize=8, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "fig_5_4_model_comparison.png"), bbox_inches='tight')
plt.close()
print("Generated Fig 5.4")

# 6. Figure 5.5: Confusion Matrix
fig, ax = plt.subplots(figsize=(5, 4.2))
cm = np.array([[8659, 0], [410, 10931]])
im = ax.imshow(cm, cmap='Blues', interpolation='nearest')
for i in range(2):
    for j in range(2):
        c = "white" if cm[i, j] > 5000 else "black"
        lbl = f"{cm[i, j]:,}\n({cm[i, j]/20000*100:.1f}%)"
        ax.text(j, i, lbl, ha="center", va="center", color=c, fontsize=11, fontweight='bold')
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Predicted Retained', 'Predicted Churned'], fontsize=9.5, fontweight='bold')
ax.set_yticklabels(['Actual Retained', 'Actual Churned'], fontsize=9.5, fontweight='bold')
ax.set_title("Decision Tree Confusion Matrix (20,000 Test Records)", fontsize=10.5, fontweight='bold', pad=12)
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "fig_5_5_confusion_matrix.png"), bbox_inches='tight')
plt.close()
print("Generated Fig 5.5")

# 7. Figure 5.6: Feature Importance
fig, ax = plt.subplots(figsize=(7, 4))
feat_imp = [
    ('Support Calls', 0.4160),
    ('Total Spend', 0.2638),
    ('Contract: Monthly', 0.1384),
    ('Payment Delay', 0.0989),
    ('Age', 0.0828),
    ('Usage Frequency', 0.0001)
]
feats, imps = zip(*feat_imp)
bars = ax.barh(feats[::-1], imps[::-1], color='#3B82F6', edgecolor='#1E3A8A', height=0.55)
for bar, val in zip(bars, imps[::-1]):
    ax.text(val + 0.008, bar.get_y() + bar.get_height()/2, f"{val:.4f} ({val*100:.1f}%)", va='center', fontsize=9, fontweight='bold')
ax.set_xlim(0, 0.48)
ax.set_xlabel("Gini Feature Importance", fontsize=9.5, fontweight='bold')
ax.set_title("Top Predictive Drivers in Decision Tree Classifier", fontsize=11, fontweight='bold', pad=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "fig_5_6_feature_importance.png"), bbox_inches='tight')
plt.close()
print("Generated Fig 5.6")
print("All charts successfully generated!")
