# Designing and Implementing a Mini Project on
# Customer Churn Prediction and Retention System
### Machine Learning based Customer Retention & Churn Analytics using a Large-Scale Subscription Dataset and a Deployed Streamlit Cloud Web Application

Submitted to the  
**Savitribai Phule Pune University**  
In partial fulfillment for the award of the Degree of  
**Bachelor of Engineering**  
in  
**Information Technology**  

by  
**Prince Maurya (Roll No. 8348)**  
**Ritika Gautam (Roll No. 8352)**  
**Saksham Chandel (Roll No. 8356)**  

Under the guidance of  
**Prof. Shweta Wankhede**  

**Department of Information Technology**  
**Army Institute of Technology**  
Dighi Hills, Pune - 411 015  
**2026-2027**  

---

## CERTIFICATE

This is to certify that **Prince Maurya (Roll No. 8348)**, **Ritika Gautam (Roll No. 8352)**, and **Saksham Chandel (Roll No. 8356)** of class T.E. IT have successfully completed their mini project work on **Customer Churn Prediction and Retention System using Machine Learning** at **Army Institute of Technology**, in partial fulfillment of the Bachelor of Engineering degree course in Information Technology for the academic year 2026-2027, Semester I, as prescribed by **Savitribai Phule Pune University**.

| Prof. Shweta Wankhede<br>Project Guide / Evaluator<br>Department of Information Technology | Dr. (Mrs.) Sangeeta Jadhav<br>Head of the Department<br>Department of Information Technology |
| :--- | :--- |

---

## ACKNOWLEDGEMENT

We express our sincere gratitude to **Prof. Shweta Wankhede** for her guidance, patient support, and valuable feedback throughout the development and evaluation of this mini project. Her suggestions helped us formulate the analytical problem, implement rigorous data preprocessing, connect the machine learning workflow to the interactive dashboard, and compile this report.

We are deeply thankful to **Dr. (Mrs.) Sangeeta Jadhav**, Head of the Department of Information Technology, and the teaching and technical staff of the department for providing the academic infrastructure, computing facilities, and constant encouragement required to complete this project.

We also acknowledge the open-source communities behind Python, pandas, NumPy, scikit-learn, Plotly, Streamlit, and joblib, whose libraries formed the core technical foundation of this platform. Finally, we thank our classmates, friends, and families for their encouragement during the development of this project.

**Prince Maurya (8348)**  
**Ritika Gautam (8352)**  
**Saksham Chandel (8356)**  

---

## INDEX

| Sr. No. | Content | Page No. |
| :---: | :--- | :---: |
| **1.** | **Introduction** | **1** |
| | 1.1 Background | 1 |
| | 1.2 About the Project | 1 |
| | 1.3 Objectives | 2 |
| | 1.4 Tools and Technology Used | 2 |
| **2.** | **Feasibility Study** | **3** |
| | 2.1 Feasibility Analysis | 3 |
| | 2.2 Technical Feasibility | 3 |
| | 2.3 Economic Feasibility | 3 |
| | 2.4 Operational Feasibility | 3 |
| | 2.5 Working of the Present System | 4 |
| | 2.6 Drawbacks of the Present System | 4 |
| **3.** | **Proposed System** | **5** |
| | 3.1 Proposed System Overview | 5 |
| | 3.2 Key Innovations and Solutions Provided | 5 |
| | 3.3 Role of the User | 6 |
| | 3.4 Role of the Developer | 6 |
| | 3.5 Justification and Need for the System | 6 |
| **4.** | **Design** | **7** |
| | 4.1 System Architecture and ML Pipeline | 7 |
| | 4.2 Dataset Description and Characteristics | 8 |
| | 4.3 Feature Space Definition (Model Inputs) | 8 |
| | 4.4 Data Preparation and Preprocessing Design | 9 |
| | 4.5 Models and Evaluation Design | 10 |
| | 4.6 Application Data Flow | 11 |
| | 4.7 Saved Model Artifacts | 11 |
| **5.** | **Implementation** | **12** |
| | 5.1 Software Environment and Dependencies | 12 |
| | 5.2 Important Code Modules | 12 |
| | 5.3 Exploratory Data Analysis | 14 |
| | 5.4 Results and Evaluation Metrics | 15 |
| | 5.5 Model Interpretation and Feature Importance | 16 |
| | 5.6 Deployment Architecture | 17 |
| **6.** | **Snapshots** | **18** |
| | 6.1 Executive Overview Dashboard | 18 |
| | 6.2 Model Comparison and Scorecard | 19 |
| | 6.3 Customer Risk Lookup and Inference Tool | 20 |
| | 6.4 Prescribed Retention Action Engine | 21 |
| **7.** | **Conclusion and Future Scope** | **22** |
| | 7.1 Conclusion | 22 |
| | 7.2 Future Scope | 22 |
| **8.** | **References** | **23** |

---

## List of Figures

* **Figure 3.1:** Proposed Customer Churn Prediction and Retention System Architecture
* **Figure 4.1:** End-to-End Machine Learning Pipeline and Data Transformation Flow
* **Figure 5.1:** Class Distribution of the Customer Churn Dataset (Retained vs. Churned)
* **Figure 5.2:** Churn Rate by Contract Length (Annual, Monthly, Quarterly)
* **Figure 5.3:** Correlation of Numerical Features with the Churn Target
* **Figure 5.4:** Algorithmic Performance Comparison (Logistic Regression vs. Decision Tree)
* **Figure 5.5:** Confusion Matrix of the Decision Tree Classifier (20,000 Test Records)
* **Figure 5.6:** Top Gini Feature Importances in the Decision Tree Model
* **Figure 6.1:** Executive Overview Dashboard (4 Top KPI Cards and 2x2 Plotly Grid)
* **Figure 6.2:** Model Evaluation Interface with Performance Benchmark and Overlaid ROC Curve
* **Figure 6.3:** Customer Risk Lookup Form with 3-Column Parameter Inputs
* **Figure 6.4:** Dual-Model Probability Output with Prescriptive Retention Playbook

---

## List of Tables

* **Table 4.1:** Summary Statistics of the Customer Churn Dataset
* **Table 4.2:** Feature Space Definition and Attribute Descriptions
* **Table 4.3:** Machine Learning Model Hyperparameters and Design Rationales
* **Table 4.4:** Serialized Model Artifacts and Operational Roles
* **Table 5.1:** Development Libraries, Platforms, and Runtime Versions
* **Table 5.2:** Performance Evaluation Metrics on the 20% Hold-out Test Set (20,000 Samples)
* **Table 5.3:** Confusion Matrix Contingency Values for Decision Tree Classifier

---

## Acronyms

| Acronym | Expansion |
| :--- | :--- |
| **AI** | Artificial Intelligence |
| **API** | Application Programming Interface |
| **AUC** | Area Under the Curve |
| **BI** | Business Intelligence |
| **CAC** | Customer Acquisition Cost |
| **CSV** | Comma-Separated Values |
| **DT** | Decision Tree |
| **EDA** | Exploratory Data Analysis |
| **FN / FP** | False Negative / False Positive |
| **GCM** | Git Credential Manager |
| **JSON** | JavaScript Object Notation |
| **KPI** | Key Performance Indicator |
| **LR** | Logistic Regression |
| **LTV** | Lifetime Value |
| **ML** | Machine Learning |
| **NPS** | Net Promoter Score |
| **OHE** | One-Hot Encoding |
| **ROC** | Receiver Operating Characteristic |
| **SaaS** | Software as a Service |
| **SPPU** | Savitribai Phule Pune University |
| **TN / TP** | True Negative / True Positive |
| **UI / UX** | User Interface / User Experience |

---

## Abstract

Customer churn represents one of the most critical operational risks in the modern subscription economy, directly threatening recurring revenue streams, compounding Customer Acquisition Costs (CAC), and diminishing Customer Lifetime Value (LTV). While traditional enterprise retention approaches rely on reactive customer exit surveys or lagging satisfaction indicators, machine learning provides the ability to proactively identify attrition patterns across multidimensional behavioral indicators before cancellation occurs.

This mini project presents the **Customer Churn Prediction and Retention System**, an end-to-end predictive machine learning and executive business intelligence platform that analyzes customer engagement, billing patterns, and contract types to predict churn probability and deliver automated, prescriptive retention playbooks. The system is engineered on a comprehensive subscription dataset comprising 440,833 customer records characterized across 11 behavioral and contractual attributes.

The project is structured into two integrated components:
1. **Model Engineering and Training Pipeline:** The raw dataset was ingested, cleaned, checked for missing values, and encoded. Categorical features (`Gender`, `Subscription Type`, `Contract Length`) were encoded using `OneHotEncoder`, and numerical attributes (`Age`, `Tenure`, `Usage Frequency`, `Support Calls`, `Payment Delay`, `Total Spend`, `Last Interaction`) were scaled using `StandardScaler`. The dataset was split into an 80/20 stratified partition (80,000 train samples and 20,000 test samples). Two distinct paradigms—**Logistic Regression** (linear log-odds) and a **Decision Tree Classifier** (hierarchical non-linear partitioning)—were trained and evaluated. The Decision Tree achieved a test accuracy of **97.95%**, precision of **100.00%**, recall of **96.39%**, and a ROC-AUC of **0.9866**, outperforming Logistic Regression (89.85% accuracy and 0.9605 ROC-AUC).
2. **Web Application & Retention Engine:** Built with Streamlit and Plotly and deployed on Streamlit Community Cloud with a minimal matte-dark carbon aesthetic inspired by modern enterprise SaaS platforms (Vercel, Linear). The application features 3 core tabs: an **Executive Churn Dashboard** with real-time KPI metrics and Plotly charts, a **Model Evaluation** benchmarking view with interactive confusion matrices and ROC curves, and a **Customer Risk Lookup** tool with real-time probability gauges, dual-model consensus checking, and an automated rule-based Customer Retention Action Plan.

**Keywords:** Machine Learning, Customer Churn, Customer Retention, Decision Tree, Logistic Regression, Feature Importance, StandardScaler, Streamlit, Business Intelligence.

---

# Chapter 1: Introduction

### 1.1 Background
In software-as-a-service (SaaS), telecommunications, financial services, and digital subscription business models, customer retention is substantially more cost-effective than customer acquisition. Empirical industry studies show that acquiring a new customer costs 5 to 7 times more than retaining an existing subscriber, while an increase of just 5% in customer retention can boost overall corporate profitability by 25% to 95%.

Customer churn occurs when a subscriber cancels their membership, downgrades their contract, or ceases platform engagement. Customers rarely terminate subscriptions abruptly without prior warning signals; their likelihood of leaving manifests in behavioral patterns such as:
* Escalating customer support tickets indicating unresolved technical friction.
* Delays in invoice settlements indicating billing dissatisfaction or cash flow stress.
* Reductions in daily active platform sessions indicating diminishing perceived value.
* Month-to-month contract commitments offering frictionless cancellation pathways.

Manual identification of these multidimensional signals across hundreds of thousands of accounts is impossible for customer success teams. Machine learning algorithms, however, can detect subtle non-linear dependencies across historical subscriber cohorts and flag at-risk accounts weeks before formal cancellation occurs.

### 1.2 About the Project
The **Customer Churn Prediction and Retention System** is an end-to-end Machine Learning and Business Intelligence mini project that bridges the gap between statistical predictive modeling and executive retention decision-making. The project executes four interconnected tasks:
1. **Dynamic Data Ingestion & Schema Adaptation:** Auto-extracts compressed `.zip` archives, inspects schemas, removes non-predictive IDs (`CustomerID`), handles outliers, and maps target columns (`Churn`) to binary representations.
2. **Feature Engineering & Transformation:** Deploys a unified `ColumnTransformer` executing `OneHotEncoder(handle_unknown='ignore')` on categorical variables and `StandardScaler()` on numerical attributes within a clean, leak-free pipeline.
3. **Comparative Algorithmic Benchmarking:** Simultaneously trains and evaluates **Logistic Regression** (for linear log-odds coefficients) and a **Decision Tree Classifier** (for non-linear threshold rules) using stratified 80/20 train-test splits.
4. **Cloud-Deployed Decision Support Platform:** Delivers a production-ready, dark-themed Streamlit web dashboard deployed globally on Streamlit Community Cloud that translates statistical risk probabilities into structured, prioritized customer retention action plans.

### 1.3 Objectives
The main objectives of this mini project are:
* **Dataset Selection and Inspection:** Acquire and analyze a comprehensive, large-scale customer churn dataset containing both behavioral and financial customer features.
* **Leak-Free Data Preprocessing:** Implement a production-grade scikit-learn preprocessing pipeline ensuring zero data leakage between training and testing splits.
* **Comparative Algorithm Evaluation:** Compare linear vs. tree-based classification techniques on identical hold-out test samples using Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
* **Model Serialization:** Serialize fitted preprocessors, trained estimators, and metadata using `joblib` and JSON to enable instantaneous inference without retraining.
* **Minimalist SaaS Web Deployment:** Design and deploy a responsive, matte-dark web application featuring executive KPI cards, Plotly charts, and an interactive customer risk simulator.
* **Prescriptive Retention Playbooks:** Automatically generate personalized business interventions (e.g., annual contract upgrade incentives, VIP concierge outreach, auto-pay restructuring) based on individual customer risk triggers.

### 1.4 Tools and Technology Used
The complete project stack consists of the following modern technologies:
* **Core Language:** Python 3.13 / 3.11.
* **Data Processing & Manipulation:** `pandas` for tabular data structures and `numpy` for high-performance matrix computations.
* **Machine Learning & Preprocessing:** `scikit-learn` for data imputation, standard scaling, one-hot encoding, stratified splitting, Logistic Regression, Decision Tree classification, and metric evaluation.
* **Model Serialization:** `joblib` for persisting binary model pipelines and Python standard `json` for metadata.
* **Interactive Visualizations:** `plotly` (Plotly Express and Plotly Graph Objects) for interactive charts with matte carbon styling.
* **Web Framework:** `streamlit` for the responsive, component-driven web user interface.
* **Version Control & Hosting:** Git, GitHub repository tracking (`chandelsaksham576/customer-churn-prediction`), and Streamlit Community Cloud for global web deployment.

---

# Chapter 2: Feasibility Study

### 2.1 Feasibility Analysis
Before commencing engineering work, a feasibility analysis was conducted to confirm that the proposed machine learning retention system could be implemented, evaluated, and deployed successfully within academic project constraints. The analysis examined technical, economic, and operational dimensions.

### 2.2 Technical Feasibility
The project dataset contains 440,833 customer records. Training a Decision Tree and Logistic Regression model on a representative stratified cohort of 100,000 samples executes within 6 to 8 seconds on standard modern CPU hardware without requiring dedicated GPU acceleration. The serialized model artifacts (`.pkl` and `.json`) occupy less than 200 KB, ensuring instantaneous loading into memory. The web interface is constructed using Streamlit and runs smoothly within Streamlit Community Cloud’s 1 GB memory limit. Therefore, the project is technically feasible.

### 2.3 Economic Feasibility
All libraries (`scikit-learn`, `pandas`, `numpy`, `plotly`, `streamlit`) are open-source and free under permissive licenses. The Kaggle customer churn dataset is publicly accessible for research. Hosting on GitHub and Streamlit Community Cloud utilizes free academic tiers. As a result, the project incurred zero financial expenditure, proving entirely economically feasible.

### 2.4 Operational Feasibility
Traditional churn models produce static CSV reports that require data analysts to interpret. The proposed application solves this by providing a self-service interactive web portal. Non-technical customer success managers and executives can simply drag sliders, select account parameters, or click "Load Random Profile" to immediately view color-coded risk tiers, probability bars, and plain-English retention action plans. Operational feasibility is therefore exceptionally high.

### 2.5 Working of the Present System
In most organizations, customer retention operates reactively:
1. A customer submits an official cancellation request or stops renewing invoices.
2. An exit survey is triggered inquiring why the customer decided to leave.
3. A customer service agent attempts a last-minute salvage call, which rarely succeeds because the decision to leave has already been finalized.
4. Retention performance is tracked retrospectively through monthly lagging churn reports.

### 2.6 Drawbacks of the Present System
* **Reactive Rather than Proactive:** Retention efforts begin only after customer intent to leave is irreversible.
* **Lack of Quantitative Risk Scoring:** Accounts are not continuously scored to identify early deterioration indicators.
* **Siloed Diagnostic Visibility:** Customer support ticket escalations, payment delays, and platform usage metrics are stored in separate operational databases and rarely analyzed together.
* **Generic Interventions:** Customers are offered one-size-fits-all retention discounts rather than targeted interventions addressing their specific root cause of dissatisfaction.

---

# Chapter 3: Proposed System

### 3.1 Proposed System Overview
The proposed **Customer Churn Prediction and Retention System** replaces reactive exit interviews with automated machine learning surveillance and prescriptive retention interventions. The architecture consists of three integrated subsystems:
1. **Automated Preprocessing & Pipeline Subsystem:** Ingests raw data, strips non-predictive keys, converts string currency metrics, standardizes numerical features, and generates one-hot encodings.
2. **Dual-Model Inference & Benchmarking Subsystem:** Compares Logistic Regression against a Decision Tree Classifier, evaluating accuracy, precision, recall, F1, and ROC-AUC on hold-out test sets.
3. **Prescriptive Web Delivery Subsystem:** A deployed, matte-dark web application that enables interactive customer profile simulation, real-time probability scoring, and automated generation of prioritized retention playbooks.

```
+-------------------------------------------------------------------------+
|                       Kaggle Churn Dataset                              |
|         440,833 records | 11 predictive features | Target: Churn        |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                       Data Preprocessing Pipeline                       |
|   Drop CustomerID | Impute Median | OneHotEncoder | StandardScaler      |
|                      80/20 Stratified Partition                         |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                     Comparative Model Training                          |
|         Logistic Regression (Balanced) vs. Decision Tree (Depth=6)      |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                     Model Evaluation & Serialization                    |
|      Accuracy | Precision | Recall | F1 | ROC-AUC | Metrics Export      |
|           Saved: preprocessor.pkl | decision_tree.pkl | metrics.json     |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  Interactive Web Application (app.py)                   |
|        Overview Dashboard | Model Benchmark | Customer Risk Simulator   |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                 Prescriptive Customer Retention Engine                  |
|    Churn Probability Gauge | Risk Pill Badge | Tailored Retention Plan  |
+-------------------------------------------------------------------------+
```
*Figure 3.1: Proposed Customer Churn Prediction and Retention System Architecture*

### 3.2 Key Innovations and Solutions Provided
* **Dual-Model Consensus Architecture:** Provides simultaneous inference across linear log-odds (Logistic Regression) and non-linear hierarchical trees (Decision Tree), allowing operators to verify whether risk is driven by gradual compounding signals or sharp threshold cutoffs.
* **Prescriptive Retention Playbooks:** Rather than merely predicting a probability number, the platform translates detected risk triggers into prioritized corporate actions (e.g., assigning a Tier-3 Customer Success Manager for accounts with over 4 support calls, or offering a 20% annual contract discount for month-to-month accounts).
* **100% Native Streamlit Layout:** Uses native `st.container(border=True)`, `st.columns(4)`, and `st.metric()` components styled with minimal matte-carbon CSS, ensuring full-width responsiveness without UI clipping.
* **Schema-Agnostic Preprocessing:** The ingestion pipeline automatically identifies target columns (`Churn`, `Exited`, `target`) and dynamically separates categorical and numerical features.

### 3.3 Role of the User
* **Executive / Analyst:** Navigates the **Overview** dashboard to review portfolio health, retention rates, and revenue at risk across customer segments.
* **Customer Success Manager:** Opens **Customer Risk Lookup**, inputs customer parameters or loads a historical customer profile, clicks "Run Risk Assessment", and reads the prescribed retention playbook to execute targeted retention outreach.

### 3.4 Role of the Developer
* **Pipeline Maintenance:** Ingest updated customer datasets in `data/raw/` and execute `preprocess.py` and `train.py`.
* **Model Serialization:** Export updated `.pkl` estimators, preprocessors, and `metrics.json` into `models/`.
* **Deployment Updates:** Commit and push changes to GitHub, triggering automatic continuous deployment on Streamlit Community Cloud.

### 3.5 Justification and Need for the System
Manual monitoring of subscriber retention is unscalable and reactive. A deployed, real-time machine learning system provides customer success teams with automated early-warning alerts, protecting top-line recurring revenue and preventing avoidable subscriber attrition.

---

# Chapter 4: Design

### 4.1 System Architecture and ML Pipeline
The platform implements an end-to-end Machine Learning pipeline comprising offline training and serialization, followed by online inference within the deployed web application:

```
[ Raw CSV Data ]
       |
       v
[ Ingestion & Cleaning (Drop IDs, Impute Missing Values) ]
       |
       v
[ ColumnTransformer (OneHotEncoder for Categoricals, StandardScaler for Numerics) ]
       |
       v
[ Stratified 80/20 Train-Test Split (Preserving 56.7% / 43.3% Class Ratio) ]
       |
       +-----------------------+-----------------------+
       |                                               |
       v                                               v
[ Logistic Regression (Balanced) ]          [ Decision Tree (Depth=6) ]
       |                                               |
       +-----------------------+-----------------------+
                               |
                               v
[ Evaluation Scorecard (Accuracy, Precision, Recall, F1, ROC-AUC) ]
                               |
                               v
[ Artifact Export (models/*.pkl, feature_metadata.json, metrics.json) ]
                               |
                               v
[ Streamlit Cloud Web Application (Overview, Benchmark, Risk Lookup) ]
```
*Figure 4.1: End-to-End Machine Learning Pipeline and Data Transformation Flow*

### 4.2 Dataset Description and Characteristics
The system uses a large-scale subscription customer churn dataset containing 440,833 training samples and 64,374 test samples. The dataset includes demographic, behavioral, contractual, and financial attributes.

*Table 4.1: Summary Statistics of the Customer Churn Dataset*
| Attribute | Specification |
| :--- | :--- |
| **Total Records (Training File)** | 440,833 customer records |
| **Total Records (Testing File)** | 64,374 customer records |
| **Representative Training Sample** | 100,000 records (80,000 train / 20,000 test) |
| **Class Distribution (Churned = 1)** | 56.71% (249,999 records) |
| **Class Distribution (Retained = 0)** | 43.29% (190,833 records) |
| **Input Features** | 10 predictive features (7 numerical, 3 categorical) |
| **Target Column** | `Churn` (Binary: `0` = Retained, `1` = Churned) |
| **Identifier Column** | `CustomerID` (automatically dropped) |
| **Missing Values** | 1 empty record detected in raw CSV; handled via cleaning |

### 4.3 Feature Space Definition (Model Inputs)
Ten attributes describe customer engagement, tenure, spending, and support utilization.

*Table 4.2: Feature Space Definition and Attribute Descriptions*
| Feature Name | Inferred Data Type | Value Range / Categories | Description |
| :--- | :--- | :--- | :--- |
| **`Age`** | Numerical (`float64`) | 18 to 65 years | Age of the customer in years |
| **`Gender`** | Categorical (`str`) | `Female`, `Male` | Biological gender of the subscriber |
| **`Tenure`** | Numerical (`float64`) | 1 to 60 months | Number of continuous active subscription months |
| **`Usage Frequency`** | Numerical (`float64`) | 1 to 30 sessions | Average number of platform login sessions per month |
| **`Support Calls`** | Numerical (`float64`) | 0 to 10 inquiries | Total technical and customer support calls logged |
| **`Payment Delay`** | Numerical (`float64`) | 0 to 30 days | Average billing settlement delay beyond due date |
| **`Subscription Type`** | Categorical (`str`) | `Basic`, `Standard`, `Premium` | Tier of platform service package |
| **`Contract Length`** | Categorical (`str`) | `Annual`, `Monthly`, `Quarterly` | Customer contract term commitment |
| **`Total Spend`** | Numerical (`float64`) | $100 to $1,000 | Cumulative monetary spending across subscription lifetime |
| **`Last Interaction`** | Numerical (`float64`) | 1 to 30 days | Number of days elapsed since the last customer touchpoint |
| **`Churn`** | Binary Target | `0` (Retained), `1` (Churned) | Historical customer attrition outcome |

### 4.4 Data Preparation and Preprocessing Design
1. **Identifier Elimination:** Columns such as `CustomerID`, `RowNumber`, and `Surname` carry no predictive signal and are automatically removed to prevent overfitting on database keys.
2. **Missing Value Imputation:** Missing numerical values are imputed with the median of the training distribution, which provides robustness against skewed outliers.
3. **Categorical One-Hot Encoding:** Categorical attributes (`Gender`, `Subscription Type`, `Contract Length`) are transformed into binary indicator columns via `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`. This expands the 3 categorical variables into 8 binary features.
4. **Standard Feature Scaling:** Numerical features have vastly differing magnitudes (e.g., `Total Spend` up to $1,000 vs. `Support Calls` up to 10). A `StandardScaler()` transforms all numeric inputs to zero mean and unit variance ($z = (x - \mu) / \sigma$), fitted exclusively on training data to prevent data leakage.
5. **Stratified Partitioning:** The dataset is partitioned into 80% training and 20% hold-out testing using `stratify=y`, strictly preserving the 56.7% / 43.3% churn-to-retention ratio across both splits.

### 4.5 Models and Evaluation Design
Two diverse classification paradigms were selected to provide complementary strengths:

*Table 4.3: Machine Learning Model Hyperparameters and Design Rationales*
| Algorithm | Hyperparameters | Architectural Rationale |
| :--- | :--- | :--- |
| **Logistic Regression** | `max_iter=1000`, `class_weight='balanced'`, `solver='lbfgs'`, `random_state=42` | Serves as a transparent linear probabilistic baseline, providing log-odds coefficients for direct risk attribution. |
| **Decision Tree Classifier** | `max_depth=6`, `min_samples_split=20`, `class_weight='balanced'`, `random_state=42` | Models complex non-linear feature interactions and threshold cutoffs while remaining interpretable without overfitting. |

The models were evaluated using five standardized classification metrics:
* **Accuracy:** Overall proportion of correct predictions across both classes.
* **Precision:** The proportion of predicted churners who truly churned ($\frac{TP}{TP + FP}$), measuring the avoidance of false alarms.
* **Recall (Sensitivity):** The proportion of actual churners correctly identified ($\frac{TP}{TP + FN}$), measuring the ability to catch departing accounts.
* **F1-Score:** The harmonic mean of Precision and Recall ($\frac{2 \cdot P \cdot R}{P + R}$), balancing detection accuracy against false alarm costs.
* **ROC-AUC Score:** Area under the Receiver Operating Characteristic curve, measuring discrimination capability across all possible decision thresholds.

### 4.6 Application Data Flow
1. The user enters customer attributes via sliders and dropdowns or clicks "Load Random Profile".
2. The web application structures the inputs into a single-row DataFrame matching the exact schema of the training set.
3. The saved `preprocessor.pkl` transforms the input through the fitted imputer, `OneHotEncoder`, and `StandardScaler`.
4. The serialized model (`decision_tree.pkl` or `logistic_regression.pkl`) calculates class probabilities ($P(\text{Churn})$ and $P(\text{Retained})$).
5. The application renders a color-coded status badge (`High Churn Risk`, `Moderate Churn Risk`, `Low Churn Risk`), a horizontal probability bar, and triggers rule-based prescriptive retention recommendations.

### 4.7 Saved Model Artifacts
*Table 4.4: Serialized Model Artifacts and Operational Roles*
| File Name | File Type | Operational Role |
| :--- | :--- | :--- |
| **`preprocessor.pkl`** | Serialized `ColumnTransformer` | Executes identical median imputation, one-hot encoding, and standard scaling on new user inputs. |
| **`decision_tree.pkl`** | Serialized `DecisionTreeClassifier` | Computes non-linear tree-based probability scores and predicted labels. |
| **`logistic_regression.pkl`** | Serialized `LogisticRegression` | Computes linear log-odds probabilities and feature coefficients. |
| **`feature_metadata.json`** | JSON Metadata Document | Stores ordered feature names, min/max slider ranges, unique category dropdown lists, and training stats. |
| **`metrics.json`** | JSON Evaluation Document | Stores precision, recall, F1, ROC-AUC, confusion matrices, and ROC coordinates for the dashboard scorecard. |
| **`sample_data.csv`** | CSV Data Sample (5,000 records) | Provides a lightweight, stratified sample for instant dashboard loading on Streamlit Community Cloud without memory overhead. |

---

# Chapter 5: Implementation

### 5.1 Software Environment and Dependencies
*Table 5.1: Development Libraries, Platforms, and Runtime Versions*
| Component | Version / Specification | Role in System Architecture |
| :--- | :--- | :--- |
| **Python** | 3.11 / 3.13 | Primary development language and runtime |
| **pandas** | >= 2.0.0 | Tabular dataset manipulation, cleaning, and aggregation |
| **numpy** | >= 1.24.0 | Numerical array manipulation and vectorized computations |
| **scikit-learn** | >= 1.3.0 | Preprocessing pipelines, classification models, and evaluation metrics |
| **plotly** | >= 5.15.0 | Interactive chart visualization and styling |
| **streamlit** | >= 1.28.0 | Web application delivery framework |
| **joblib** | >= 1.3.0 | High-performance serialization of models and pipelines |
| **GitHub** | Cloud Git Repository | Version control, codebase hosting, and CI/CD triggers |
| **Streamlit Cloud** | Global Hosting Platform | Cloud server runtime for worldwide web access |

### 5.2 Important Code Modules

#### (a) Ingestion and Dynamic Cleaning (`src/preprocess.py`)
```python
def clean_data(df: pd.DataFrame, target_col: str, id_cols: list) -> pd.DataFrame:
    cleaned_df = df.copy()
    cols_to_drop = [col for col in id_cols if col in cleaned_df.columns]
    if cols_to_drop:
        cleaned_df = cleaned_df.drop(columns=cols_to_drop)

    cleaned_df = cleaned_df.dropna(subset=[target_col])
    cleaned_df[target_col] = cleaned_df[target_col].astype(int)

    for col in cleaned_df.columns:
        if col == target_col:
            continue
        if not pd.api.types.is_numeric_dtype(cleaned_df[col]):
            s = cleaned_df[col].astype(str).str.replace("$", "").str.replace(",", "").str.strip()
            numeric_conv = pd.to_numeric(s, errors="coerce")
            if numeric_conv.notnull().sum() / len(cleaned_df) > 0.6:
                cleaned_df[col] = numeric_conv.fillna(numeric_conv.median())
    return cleaned_df
```

#### (b) Pipeline Construction & Feature Transformation (`src/preprocess.py`)
```python
def build_preprocessor(categorical_features: list, numerical_features: list) -> ColumnTransformer:
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    return ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numerical_features),
            ("cat", cat_pipeline, categorical_features)
        ],
        remainder="drop"
    )
```

#### (c) Model Training & Evaluation (`src/train.py`)
```python
# Model 1: Logistic Regression
lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
y_prob_lr = lr.predict_proba(X_test)[:, 1]

# Model 2: Decision Tree Classifier
dt = DecisionTreeClassifier(max_depth=6, min_samples_split=20, class_weight="balanced", random_state=42)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
y_prob_dt = dt.predict_proba(X_test)[:, 1]
```

#### (d) Prescriptive Retention Action Engine (`src/predict.py`)
```python
def generate_retention_recommendations(customer_input: dict, churn_prob: float) -> list:
    recommendations = []
    support_calls = float(customer_input.get("Support Calls", 0))
    if support_calls >= 4:
        recommendations.append({
            "title": "Immediate Customer Success Escalation",
            "trigger": f"High Support Ticket Volume ({int(support_calls)} calls recorded)",
            "urgency": "Immediate (Within 24 Hours)",
            "action": "Assign a Tier-3 Senior Customer Success Manager to schedule an executive resolution call.",
            "expected_impact": "Reduces customer frustration churn by ~35%."
        })
    contract = str(customer_input.get("Contract Length", "")).strip().lower()
    if "month" in contract:
        recommendations.append({
            "title": "Annual Contract Lock-in Incentive",
            "trigger": "Customer is on Month-to-Month commitment",
            "urgency": "High Priority",
            "action": "Extend an exclusive promotion: Upgrade to a 12-month annual contract with a 20% discount.",
            "expected_impact": "Substantially increases LTV and reduces month-to-month attrition."
        })
    return recommendations
```

### 5.3 Exploratory Data Analysis
Exploratory Data Analysis revealed several critical business and statistical relationships:
1. **Class Distribution:** The full training dataset contains 249,999 churned customers (56.71%) and 190,833 retained customers (43.29%), representing a balanced 1.31:1 ratio.
2. **Contract Type as a Dominant Driver:** Customers on Month-to-Month contracts exhibit an alarming 100% historical churn rate in this cohort, whereas subscribers enrolled in Annual and Quarterly contracts maintain churn rates of only 46.08% and 46.03% respectively.
3. **Support Inquiry Escalation:** Retained customers average only **1.59 support calls**, whereas churned subscribers average **5.14 calls**—a dramatic +224.3% surge indicating that unresolved technical friction directly triggers cancellations.
4. **Correlation Analysis:** `Support Calls` exhibits the strongest positive correlation with churn (+0.5743), followed by `Payment Delay` (+0.3121) and `Age` (+0.2184). Conversely, `Total Spend` correlates negatively (-0.4294), confirming that high-value customers possess greater product stickiness.

### 5.4 Results and Evaluation Metrics
Both models were benchmarked on the identical 20% hold-out test set comprising 20,000 customer records:

*Table 5.2: Model Evaluation Metrics on the 20% Hold-out Test Set (20,000 Samples)*
| Metric | Logistic Regression | Decision Tree Classifier | Variance / Delta | Leading Architecture |
| :--- | :--- | :--- | :--- | :--- |
| **Accuracy** | 89.85% | **97.95%** | +8.10% | **Decision Tree** |
| **Precision** | 94.10% | **100.00%** | +5.90% | **Decision Tree** |
| **Recall** | 87.59% | **96.39%** | +8.80% | **Decision Tree** |
| **F1-Score** | 90.73% | **98.16%** | +7.43% | **Decision Tree** |
| **ROC-AUC** | 0.9605 | **0.9866** | +0.0261 | **Decision Tree** |

The **Decision Tree Classifier** achieved superior performance across all evaluation metrics, reaching an overall accuracy of **97.95%** and an F1-Score of **98.16%**. Its perfect precision (100.00%) indicates that when the Decision Tree predicts an account will churn, it produces zero false alarms, allowing marketing and retention teams to invest retention budgets with complete confidence.

*Table 5.3: Confusion Matrix Contingency Values for Decision Tree Classifier (20,000 Test Records)*
| | Predicted Retained (0) | Predicted Churned (1) |
| :--- | :---: | :---: |
| **Actual Retained (0)** | 8,659 (True Negatives) | 0 (False Positives) |
| **Actual Churned (1)** | 410 (False Negatives) | 10,931 (True Positives) |

### 5.5 Model Interpretation and Feature Importance
The models provide complementary interpretability insights into customer attrition mechanisms:
* **Decision Tree Gini Importance:** The top decision split in the tree is governed by **`Support Calls`** (Gini importance = **0.4160**), followed by **`Total Spend`** (0.2638), **`Contract Length_Monthly`** (0.1384), **`Payment Delay`** (0.0989), and **`Age`** (0.0828). This proves that technical support friction and financial commitment thresholds dominate retention outcomes.
* **Logistic Regression Log-Odds Coefficients:** The feature with the highest positive odds of churn is `Contract Length_Monthly` (coefficient = **+6.7045**), followed by `Support Calls` (**+2.3623**). Conversely, `Contract Length_Annual` (**-2.5392**) and `Total Spend` (**-1.4784**) strongly decrease churn probability.

### 5.6 Deployment Architecture
The web application is deployed on **Streamlit Community Cloud** directly connected to the GitHub repository `chandelsaksham576/customer-churn-prediction`. The deployment utilizes:
* **Matte Carbon Design System:** Custom-configured via `.streamlit/config.toml` (`base="dark"`, `backgroundColor="#09090B"`, `secondaryBackgroundColor="#121215"`, `primaryColor="#FAFAFA"`).
* **Native Component Architecture:** Eliminates custom HTML divs in favor of native `st.container(border=True)`, `st.columns(4)`, `st.metric()`, and `st.dataframe()`, guaranteeing seamless rendering across all display resolutions.
* **Zero-Latency In-Memory Inference:** Serialized estimators load in under 15 milliseconds, enabling instantaneous real-time prediction updates as users adjust parameter sliders.

---

# Chapter 6: Snapshots

This chapter presents the working web application deployed at:  
**https://github.com/chandelsaksham576/customer-churn-prediction**  
*(Live on Streamlit Community Cloud)*

### 6.1 Executive Overview Dashboard
The Overview tab presents four top KPI cards (`Total Customers`, `Monthly Revenue at Risk`, `Overall Retention Rate`, `Churn Rate`) above a balanced 2x2 Plotly visualization grid:
* **Chart 1:** Customer Status across Contract Length (Grouped Bar chart comparing Retained vs. Churned subscribers).
* **Chart 2:** Churn Rate across Subscription Tiers (Basic, Standard, Premium).
* **Chart 3:** Customer Value vs. Tenure Scatter Mapping.
* **Chart 4:** Churn Rate Surge by Support Inquiries logged.

### 6.2 Model Comparison and Scorecard
The Model Evaluation tab displays the side-by-side performance scorecard comparing Logistic Regression against the Decision Tree Classifier, accompanied by:
* An interactive Confusion Matrix toggleable between both models.
* An overlaid dual-model ROC Curve with an AUC score badge and random baseline.
* Horizontal bar charts comparing Logistic Regression Log-Odds Coefficients against Decision Tree Gini Split Importance.
* An expandable Decision Tree rule breakdown.

### 6.3 Customer Risk Lookup and Inference Tool
The Customer Risk Lookup tab provides a clean, 3-column bordered parameter input container:
* **Account Profile:** Age, Gender, Tenure sliders and dropdowns.
* **Service Subscriptions:** Subscription Type, Contract Length, Usage Frequency.
* **Billing & Usage:** Support Calls, Payment Delay, Total Spend, Last Interaction.
* **Model Selector & Simulator:** Radio pill toggling between Decision Tree, Logistic Regression, or Dual-Model, with a "Load Random Profile" button to simulate real historical customer records.

### 6.4 Prescribed Retention Action Engine
Upon clicking "Run Risk Assessment", the application outputs:
* A flat status pill badge (`High Churn Risk` in crimson or `Low Churn Risk` in emerald).
* A horizontal probability progress bar displaying exact churn likelihood (%).
* In Dual-Model mode, a consensus check comparing both models side-by-side.
* A structured table of tailored, prioritized retention playbooks detailing Title, Driver, Urgency, Action, and Expected ROI Impact.

---

# Chapter 7: Conclusion and Future Scope

### 7.1 Conclusion
In this mini project, a complete end-to-end **Customer Churn Prediction and Retention System** was successfully designed, evaluated, and deployed. Key accomplishments include:
1. **End-to-End Scalable Pipeline:** Implemented dynamic data ingestion, cleaning, median imputation, one-hot encoding, standard scaling, and stratified 80/20 partitioning across large-scale subscription data.
2. **Empirical Algorithmic Benchmarking:** Compared linear and tree-based classification architectures. The Decision Tree Classifier achieved an outstanding **97.95% accuracy**, **100% precision**, and a **0.9866 ROC-AUC**, successfully catching 96.39% of churners with zero false alarms.
3. **Prescriptive Action Engine:** Successfully bridged machine learning with executive decision-making by translating statistical probabilities into actionable corporate retention interventions.
4. **Production Web Deployment:** Deployed a responsive, matte-dark web application on Streamlit Community Cloud with 100% native component styling and zero runtime errors.

### 7.2 Future Scope
* **Ensemble Integration (XGBoost & LightGBM):** Incorporate gradient boosted decision trees to further minimize false negatives.
* **Automated CRM Integration:** Connect the prediction engine directly to enterprise CRM platforms (e.g., Salesforce, HubSpot) via REST APIs to automatically trigger automated email campaigns and support tickets.
* **Survival Analysis:** Implement Cox Proportional Hazards modeling to predict not only *if* a customer will churn, but the exact expected *time until churn*.
* **Explainable AI (SHAP & LIME):** Integrate SHAP waterfall plots into the web dashboard to visualize the exact numerical contribution of each feature toward an individual subscriber's risk score.
* **Automated PDF Export:** Enable customer success teams to export single-customer retention dossiers as formatted PDF reports with one click.

---

# Chapter 8: References

1. **Pedregosa, F., et al.** (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
2. **Breiman, L., Friedman, J., Stone, C. J., and Olshen, R. A.** (1984). *Classification and Regression Trees*. CRC Press.
3. **Hosmer Jr, D. W., Lemeshow, S., and Sturdivant, R. X.** (2013). *Applied Logistic Regression*. John Wiley & Sons.
4. **McKinney, W.** (2010). *Data Structures for Statistical Computing in Python*. Proceedings of the 9th Python in Science Conference, 51-56.
5. **Harris, C. R., et al.** (2020). *Array programming with NumPy*. Nature, 585(7825), 357-362.
6. **Plotly Technologies Inc.** (2025). *Collaborative Data Science: Plotly Python Open Source Graphing Library*. https://plotly.com/python/
7. **Streamlit Inc.** (2025). *Streamlit: A faster way to build and share data apps*. https://docs.streamlit.io/
8. **Kaggle Inc.** (2024). *Customer Churn Prediction Dataset*. Kaggle Machine Learning Datasets. https://www.kaggle.com
9. **Fawcett, T.** (2006). *An introduction to ROC analysis*. Pattern Recognition Letters, 27(8), 861-874.
10. **Savitribai Phule Pune University (SPPU).** *Curriculum and Guidelines for Third Year Engineering (T.E. Information Technology) Mini Project (2026-2027)*.
