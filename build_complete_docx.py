import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def add_p(doc, text="", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(31, 41, 55)
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(17, 24, 39)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(17, 24, 39)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(55, 65, 81)
    return p

def add_bullet(doc, bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        r1.bold = True
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = RGBColor(17, 24, 39)
    r2 = p.add_run(text)
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11.5)
    r2.font.color.rgb = RGBColor(55, 65, 81)
    return p

def add_image_safe(doc, img_path, width_in=5.5, caption=""):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_in))
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(12)
            rc = p_cap.add_run(caption)
            rc.italic = True
            rc.bold = True
            rc.font.name = 'Times New Roman'
            rc.font.size = Pt(10.5)
            rc.font.color.rgb = RGBColor(75, 85, 99)

def format_cell(cell, text, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, size=10.5):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.font.color.rgb = RGBColor(17, 24, 39)

def create_report():
    doc = docx.Document()
    
    # Page Margins (1 inch top, bottom, left, right)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    logo_path = r"C:\Users\chand\.gemini\antigravity\scratch\customer-churn-prediction\extracted_media\image_0.png"
    fig_dir = r"C:\Users\chand\.gemini\antigravity\scratch\customer-churn-prediction\reports\figures"

    # ==================== COVER PAGE ====================
    p = add_p(doc, "Designing and Implementing a Mini Project on", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=6)
    p.runs[0].font.size = Pt(14)
    
    p = add_p(doc, "Customer Churn Prediction and Retention System", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=10)
    p.runs[0].font.size = Pt(22)
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(15, 23, 42)

    p = add_p(doc, "Machine Learning based Customer Retention & Churn Analytics using a Large-Scale Subscription Dataset and a Deployed Streamlit Cloud Web Application", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=20)
    p.runs[0].font.size = Pt(11)
    p.runs[0].italic = True

    add_p(doc, "Submitted to the", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p = add_p(doc, "Savitribai Phule Pune University", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p.runs[0].bold = True
    add_p(doc, "In partial fulfillment for the award of the Degree of", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p = add_p(doc, "Bachelor of Engineering", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p.runs[0].bold = True
    add_p(doc, "in", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p = add_p(doc, "Information Technology", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    p.runs[0].bold = True

    add_p(doc, "by", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    for name_roll in ["Prince Maurya (Roll No. 8348)", "Ritika Gautam (Roll No. 8352)", "Saksham Chandel (Roll No. 8356)"]:
        p = add_p(doc, name_roll, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
        p.runs[0].bold = True

    add_p(doc, "Under the guidance of", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=14, space_after=2)
    p = add_p(doc, "Prof. Shweta Wankhede", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    p.runs[0].bold = True

    if os.path.exists(logo_path):
        add_image_safe(doc, logo_path, width_in=1.1)

    p = add_p(doc, "Department of Information Technology", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=2)
    p.runs[0].bold = True
    p = add_p(doc, "Army Institute of Technology", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p.runs[0].bold = True
    add_p(doc, "Dighi Hills, Pune - 411 015", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p = add_p(doc, "2026-2027", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    p.runs[0].bold = True

    doc.add_page_break()

    # ==================== CERTIFICATE ====================
    add_heading_1(doc, "CERTIFICATE")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=16, space_after=24, line_spacing=1.3)
    p.add_run("This is to certify that ")
    p.add_run("Prince Maurya (Roll No. 8348)").bold = True
    p.add_run(", ")
    p.add_run("Ritika Gautam (Roll No. 8352)").bold = True
    p.add_run(", and ")
    p.add_run("Saksham Chandel (Roll No. 8356)").bold = True
    p.add_run(" of class T.E. IT have successfully completed their mini project work on ")
    p.add_run("Customer Churn Prediction and Retention System using Machine Learning").bold = True
    p.add_run(" at ")
    p.add_run("Army Institute of Technology").bold = True
    p.add_run(", in partial fulfillment of the Bachelor of Engineering degree course in Information Technology for the academic year 2026-2027, Semester I, as prescribed by ")
    p.add_run("Savitribai Phule Pune University").bold = True
    p.add_run(".")

    # Borderless signature table
    table_cert = doc.add_table(rows=1, cols=2)
    table_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_cert.autofit = False

    cell_0, cell_1 = table_cert.rows[0].cells
    cell_0.width = Inches(3.2)
    cell_1.width = Inches(3.2)
    
    p0 = cell_0.paragraphs[0]
    p0.paragraph_format.space_before = Pt(80)
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p0.add_run("Prof. Shweta Wankhede\nProject Guide / Evaluator\nDepartment of Information Technology")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)

    p1 = cell_1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(80)
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p1.add_run("Dr. (Mrs.) Sangeeta Jadhav\nHead of the Department\nDepartment of Information Technology")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)

    doc.add_page_break()

    # ==================== ACKNOWLEDGEMENT ====================
    add_heading_1(doc, "ACKNOWLEDGEMENT")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=16, space_after=12, line_spacing=1.2)
    p.add_run("We express our sincere gratitude to ")
    p.add_run("Prof. Shweta Wankhede").bold = True
    p.add_run(" for her guidance, patient support, and valuable feedback throughout the development and evaluation of this mini project. Her suggestions helped us formulate the analytical problem, implement rigorous data preprocessing, connect the machine learning workflow to the interactive dashboard, and compile this report.")

    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=12, line_spacing=1.2)
    p.add_run("We are deeply thankful to ")
    p.add_run("Dr. (Mrs.) Sangeeta Jadhav").bold = True
    p.add_run(", Head of the Department of Information Technology, and the teaching and technical staff of the department for providing the academic infrastructure, computing facilities, and constant encouragement required to complete this project.")

    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=24, line_spacing=1.2)
    p.add_run("We also acknowledge the open-source communities behind Python, pandas, NumPy, scikit-learn, Plotly, Streamlit, and joblib, whose libraries formed the core technical foundation of this platform. Finally, we thank our classmates, friends, and families for their encouragement during the development of this project.")

    for s_name in ["Prince Maurya (8348)", "Ritika Gautam (8352)", "Saksham Chandel (8356)"]:
        p = add_p(doc, s_name, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=2)
        p.runs[0].bold = True

    doc.add_page_break()

    # ==================== INDEX ====================
    add_heading_1(doc, "INDEX")
    
    index_data = [
        ("1.", "Introduction", "1", True),
        ("", "1.1 Background", "1", False),
        ("", "1.2 About the Project", "1", False),
        ("", "1.3 Objectives", "2", False),
        ("", "1.4 Tools and Technology Used", "2", False),
        ("2.", "Feasibility Study", "3", True),
        ("", "2.1 Feasibility Analysis", "3", False),
        ("", "2.2 Technical Feasibility", "3", False),
        ("", "2.3 Economic Feasibility", "3", False),
        ("", "2.4 Operational Feasibility", "3", False),
        ("", "2.5 Working of the Present System", "4", False),
        ("", "2.6 Drawbacks of the Present System", "4", False),
        ("3.", "Proposed System", "5", True),
        ("", "3.1 Proposed System Overview", "5", False),
        ("", "3.2 Key Innovations and Solutions Provided", "5", False),
        ("", "3.3 Role of the User", "6", False),
        ("", "3.4 Role of the Developer", "6", False),
        ("", "3.5 Justification and Need for the System", "6", False),
        ("4.", "Design", "7", True),
        ("", "4.1 System Architecture and ML Pipeline", "7", False),
        ("", "4.2 Dataset Description and Characteristics", "8", False),
        ("", "4.3 Feature Space Definition (Model Inputs)", "8", False),
        ("", "4.4 Data Preparation and Preprocessing Design", "9", False),
        ("", "4.5 Models and Evaluation Design", "10", False),
        ("", "4.6 Application Data Flow", "11", False),
        ("", "4.7 Saved Model Artifacts", "11", False),
        ("5.", "Implementation", "12", True),
        ("", "5.1 Software Environment and Dependencies", "12", False),
        ("", "5.2 Important Code Modules", "12", False),
        ("", "5.3 Exploratory Data Analysis", "14", False),
        ("", "5.4 Results and Evaluation Metrics", "15", False),
        ("", "5.5 Model Interpretation and Feature Importance", "16", False),
        ("", "5.6 Deployment Architecture", "17", False),
        ("6.", "Snapshots", "18", True),
        ("", "6.1 Executive Overview Dashboard", "18", False),
        ("", "6.2 Model Comparison and Scorecard", "19", False),
        ("", "6.3 Customer Risk Lookup and Inference Tool", "20", False),
        ("", "6.4 Prescribed Retention Action Engine", "21", False),
        ("7.", "Conclusion and Future Scope", "22", True),
        ("", "7.1 Conclusion", "22", False),
        ("", "7.2 Future Scope", "22", False),
        ("8.", "References", "23", True)
    ]

    t_index = doc.add_table(rows=len(index_data)+1, cols=3)
    t_index.style = 'Table Grid'
    t_index.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header
    for idx, h_text in enumerate(["Sr. No.", "Content", "Page No."]):
        cell = t_index.rows[0].cells[idx]
        format_cell(cell, h_text, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER if idx!=1 else WD_ALIGN_PARAGRAPH.LEFT)

    for r_idx, (sr, content, pg, is_b) in enumerate(index_data):
        row = t_index.rows[r_idx+1]
        for c_idx, val in enumerate([sr, content, pg]):
            cell = row.cells[c_idx]
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx!=1 else WD_ALIGN_PARAGRAPH.LEFT
            format_cell(cell, val, bold=is_b, align=align)

    doc.add_page_break()

    # ==================== LIST OF FIGURES & TABLES ====================
    add_heading_2(doc, "List of Figures")
    fig_list = [
        ("Figure 3.1", "Proposed Customer Churn Prediction and Retention System Architecture", "5"),
        ("Figure 4.1", "End-to-End Machine Learning Pipeline and Data Transformation Flow", "7"),
        ("Figure 5.1", "Class Distribution of the Customer Churn Dataset (Retained vs. Churned)", "14"),
        ("Figure 5.2", "Churn Rate by Contract Length (Annual, Monthly, Quarterly)", "14"),
        ("Figure 5.3", "Correlation of Numerical Features with the Churn Target", "15"),
        ("Figure 5.4", "Algorithmic Performance Comparison (Logistic Regression vs. Decision Tree)", "15"),
        ("Figure 5.5", "Confusion Matrix of the Decision Tree Classifier (20,000 Test Records)", "16"),
        ("Figure 5.6", "Top Gini Feature Importances in the Decision Tree Model", "17"),
        ("Figure 6.1", "Executive Overview Dashboard (4 Top KPI Cards and 2x2 Plotly Grid)", "18"),
        ("Figure 6.2", "Model Evaluation Interface with Performance Benchmark & ROC Curve", "19"),
        ("Figure 6.3", "Customer Risk Lookup Form with 3-Column Parameter Inputs", "20"),
        ("Figure 6.4", "Dual-Model Probability Output with Prescriptive Retention Playbook", "21")
    ]
    for tag, desc, pg in fig_list:
        add_bullet(doc, f"{tag}: ", f"{desc}\t\t{pg}")

    add_heading_2(doc, "List of Tables")
    tbl_list = [
        ("Table 4.1", "Summary Statistics of the Customer Churn Dataset", "8"),
        ("Table 4.2", "Feature Space Definition and Attribute Descriptions", "9"),
        ("Table 4.3", "Machine Learning Model Hyperparameters and Design Rationales", "10"),
        ("Table 4.4", "Serialized Model Artifacts and Operational Roles", "11"),
        ("Table 5.1", "Development Libraries, Platforms, and Runtime Versions", "12"),
        ("Table 5.2", "Performance Evaluation Metrics on the 20% Hold-out Test Set", "15"),
        ("Table 5.3", "Confusion Matrix Contingency Values for Decision Tree Classifier", "16")
    ]
    for tag, desc, pg in tbl_list:
        add_bullet(doc, f"{tag}: ", f"{desc}\t\t{pg}")

    add_heading_2(doc, "Acronyms")
    acronyms = [
        ("AI", "Artificial Intelligence"),
        ("API", "Application Programming Interface"),
        ("AUC", "Area Under the Curve"),
        ("BI", "Business Intelligence"),
        ("CAC", "Customer Acquisition Cost"),
        ("CSV", "Comma-Separated Values"),
        ("DT", "Decision Tree"),
        ("EDA", "Exploratory Data Analysis"),
        ("FN / FP", "False Negative / False Positive"),
        ("KPI", "Key Performance Indicator"),
        ("LR", "Logistic Regression"),
        ("LTV", "Lifetime Value"),
        ("ML", "Machine Learning"),
        ("OHE", "One-Hot Encoding"),
        ("ROC", "Receiver Operating Characteristic"),
        ("SaaS", "Software as a Service"),
        ("SPPU", "Savitribai Phule Pune University"),
        ("TN / TP", "True Negative / True Positive"),
        ("UI / UX", "User Interface / User Experience")
    ]
    t_acro = doc.add_table(rows=len(acronyms)+1, cols=2)
    t_acro.style = 'Table Grid'
    t_acro.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, h_text in enumerate(["Acronym", "Expansion"]):
        cell = t_acro.rows[0].cells[idx]
        format_cell(cell, h_text, bold=True)
    for r_idx, (ac, exp) in enumerate(acronyms):
        row = t_acro.rows[r_idx+1]
        for c_idx, val in enumerate([ac, exp]):
            cell = row.cells[c_idx]
            format_cell(cell, val, bold=(c_idx==0))

    doc.add_page_break()

    # ==================== ABSTRACT ====================
    add_heading_1(doc, "Abstract")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=12, space_after=12, line_spacing=1.2)
    p.add_run("Customer churn represents one of the most critical operational risks in the modern subscription economy, directly threatening recurring revenue streams, compounding Customer Acquisition Costs (CAC), and diminishing Customer Lifetime Value (LTV). While traditional enterprise retention approaches rely on reactive customer exit surveys or lagging satisfaction indicators, machine learning provides the ability to proactively identify attrition patterns across multidimensional behavioral indicators before cancellation occurs.")

    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=12, line_spacing=1.2)
    p.add_run("This mini project presents the ")
    p.add_run("Customer Churn Prediction and Retention System").bold = True
    p.add_run(", an end-to-end predictive machine learning and executive business intelligence platform that analyzes customer engagement, billing patterns, and contract types to predict churn probability and deliver automated, prescriptive retention playbooks. The system is engineered on a comprehensive subscription dataset comprising 440,833 customer records characterized across 11 behavioral and contractual attributes.")

    add_bullet(doc, "Model Engineering and Training Pipeline: ", "The raw dataset was ingested, cleaned, checked for missing values, and encoded. Categorical features (Gender, Subscription Type, Contract Length) were encoded using OneHotEncoder, and numerical attributes (Age, Tenure, Usage Frequency, Support Calls, Payment Delay, Total Spend, Last Interaction) were scaled using StandardScaler. The dataset was split into an 80/20 stratified partition (80,000 train samples and 20,000 test samples). Two distinct paradigms—Logistic Regression (linear log-odds) and a Decision Tree Classifier (hierarchical non-linear partitioning)—were trained and evaluated. The Decision Tree achieved a test accuracy of 97.95%, precision of 100.00%, recall of 96.39%, and a ROC-AUC of 0.9866, outperforming Logistic Regression (89.85% accuracy and 0.9605 ROC-AUC).")

    add_bullet(doc, "Web Application & Retention Engine: ", "Built with Streamlit and Plotly and deployed on Streamlit Community Cloud with a minimal matte-dark carbon aesthetic inspired by modern enterprise SaaS platforms (Vercel, Linear). The application features 3 core tabs: an Executive Churn Dashboard with real-time KPI metrics and Plotly charts, a Model Evaluation benchmarking view with interactive confusion matrices and ROC curves, and a Customer Risk Lookup tool with real-time probability gauges, dual-model consensus checking, and an automated rule-based Customer Retention Action Plan.")

    p_kw = add_p(doc, space_before=16, space_after=12)
    r_kw = p_kw.add_run("Keywords: ")
    r_kw.bold = True
    p_kw.add_run("Machine Learning, Customer Churn, Customer Retention, Decision Tree, Logistic Regression, Feature Importance, StandardScaler, Streamlit, Business Intelligence.")

    doc.add_page_break()

    # ==================== CHAPTER 1 ====================
    add_heading_1(doc, "Chapter 1\nIntroduction")
    
    add_heading_2(doc, "1.1 Background")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("In software-as-a-service (SaaS), telecommunications, financial services, and digital subscription business models, customer retention is substantially more cost-effective than customer acquisition. Empirical industry studies show that acquiring a new customer costs 5 to 7 times more than retaining an existing subscriber, while an increase of just 5% in customer retention can boost overall corporate profitability by 25% to 95%.")

    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("Customer churn occurs when a subscriber cancels their membership, downgrades their contract, or ceases platform engagement. Customers rarely terminate subscriptions abruptly without prior warning signals; their likelihood of leaving manifests in behavioral patterns such as:")
    add_bullet(doc, "Escalating Support Tickets: ", "Repeated support inquiries indicate unresolved technical friction or workflow dissatisfaction.")
    add_bullet(doc, "Billing Delays: ", "Delays in invoice settlements frequently reflect billing dissatisfaction, disengagement, or cash flow stress.")
    add_bullet(doc, "Usage Drops: ", "Reductions in daily active platform sessions reflect diminishing perceived product value.")
    add_bullet(doc, "Frictionless Contracts: ", "Month-to-month contract commitments offer zero barrier to exit compared to annual plans.")

    add_heading_2(doc, "1.2 About the Project")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("The Customer Churn Prediction and Retention System is an end-to-end Machine Learning and Business Intelligence mini project that bridges the gap between statistical predictive modeling and executive retention decision-making. The project executes four interconnected tasks:")
    add_bullet(doc, "Dynamic Data Ingestion & Schema Adaptation: ", "Auto-extracts compressed .zip archives, inspects schemas, removes non-predictive IDs (CustomerID), handles outliers, and maps target columns to binary representations.")
    add_bullet(doc, "Feature Engineering & Transformation: ", "Deploys a unified ColumnTransformer executing OneHotEncoder(handle_unknown='ignore') on categorical variables and StandardScaler() on numerical attributes within a clean, leak-free pipeline.")
    add_bullet(doc, "Comparative Algorithmic Benchmarking: ", "Simultaneously trains and evaluates Logistic Regression (for linear log-odds coefficients) and a Decision Tree Classifier (for non-linear threshold rules) using stratified 80/20 train-test splits.")
    add_bullet(doc, "Cloud-Deployed Decision Support Platform: ", "Delivers a production-ready, dark-themed Streamlit web dashboard deployed globally on Streamlit Community Cloud that translates statistical risk probabilities into structured, prioritized customer retention action plans.")

    add_heading_2(doc, "1.3 Objectives")
    add_bullet(doc, "Dataset Selection and Inspection: ", "Acquire and analyze a comprehensive, large-scale customer churn dataset containing both behavioral and financial customer features.")
    add_bullet(doc, "Leak-Free Data Preprocessing: ", "Implement a production-grade scikit-learn preprocessing pipeline ensuring zero data leakage between training and testing splits.")
    add_bullet(doc, "Comparative Algorithm Evaluation: ", "Compare linear vs. tree-based classification techniques on identical hold-out test samples using Accuracy, Precision, Recall, F1-Score, and ROC-AUC.")
    add_bullet(doc, "Model Serialization: ", "Serialize fitted preprocessors, trained estimators, and metadata using joblib and JSON to enable instantaneous inference without retraining.")
    add_bullet(doc, "Minimalist SaaS Web Deployment: ", "Design and deploy a responsive, matte-dark web application featuring executive KPI cards, Plotly charts, and an interactive customer risk simulator.")
    add_bullet(doc, "Prescriptive Retention Playbooks: ", "Automatically generate personalized business interventions (e.g., annual contract upgrade incentives, VIP concierge outreach, auto-pay restructuring) based on individual customer risk triggers.")

    add_heading_2(doc, "1.4 Tools and Technology Used")
    add_bullet(doc, "Core Language: ", "Python 3.13 / 3.11 runtime.")
    add_bullet(doc, "Data Manipulation: ", "pandas for DataFrame operations and NumPy for matrix calculations.")
    add_bullet(doc, "Machine Learning: ", "scikit-learn for ColumnTransformer, SimpleImputer, OneHotEncoder, StandardScaler, LogisticRegression, and DecisionTreeClassifier.")
    add_bullet(doc, "Data Visualization: ", "Plotly Express and Plotly Graph Objects for interactive charts.")
    add_bullet(doc, "Web Framework: ", "Streamlit for rapid component-based web UI development.")
    add_bullet(doc, "Deployment & Version Control: ", "Git, GitHub (chandelsaksham576/customer-churn-prediction), and Streamlit Community Cloud.")

    doc.add_page_break()

    # ==================== CHAPTER 2 ====================
    add_heading_1(doc, "Chapter 2\nFeasibility Study")
    
    add_heading_2(doc, "2.1 Feasibility Analysis")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("Before commencing engineering work, a feasibility analysis was conducted to confirm that the proposed machine learning retention system could be implemented, evaluated, and deployed successfully within academic project constraints. The analysis examined technical, economic, and operational dimensions.")

    add_heading_2(doc, "2.2 Technical Feasibility")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("The project dataset contains 440,833 customer records. Training a Decision Tree and Logistic Regression model on a representative stratified cohort of 100,000 samples executes within 6 to 8 seconds on standard modern CPU hardware without requiring dedicated GPU acceleration. The serialized model artifacts (.pkl and .json) occupy less than 200 KB, ensuring instantaneous loading into memory. The web interface is constructed using Streamlit and runs smoothly within Streamlit Community Cloud’s 1 GB memory limit. Therefore, the project is technically feasible.")

    add_heading_2(doc, "2.3 Economic Feasibility")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("All libraries (scikit-learn, pandas, numpy, plotly, streamlit) are open-source and free under permissive licenses. The Kaggle customer churn dataset is publicly accessible for research. Hosting on GitHub and Streamlit Community Cloud utilizes free academic tiers. As a result, the project incurred zero financial expenditure, proving entirely economically feasible.")

    add_heading_2(doc, "2.4 Operational Feasibility")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("Traditional churn models produce static CSV reports that require data analysts to interpret. The proposed application solves this by providing a self-service interactive web portal. Non-technical customer success managers and executives can simply drag sliders, select account parameters, or click 'Load Random Profile' to immediately view color-coded risk tiers, probability bars, and plain-English retention action plans. Operational feasibility is therefore exceptionally high.")

    add_heading_2(doc, "2.5 Working of the Present System")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("In most organizations, customer retention operates reactively: (1) A customer submits an official cancellation request or stops renewing invoices; (2) An exit survey is triggered inquiring why the customer decided to leave; (3) A customer service agent attempts a last-minute salvage call, which rarely succeeds because the decision to leave has already been finalized; (4) Retention performance is tracked retrospectively through monthly lagging churn reports.")

    add_heading_2(doc, "2.6 Drawbacks of the Present System")
    add_bullet(doc, "Reactive Rather than Proactive: ", "Retention efforts begin only after customer intent to leave is irreversible.")
    add_bullet(doc, "Lack of Quantitative Risk Scoring: ", "Accounts are not continuously scored to identify early deterioration indicators.")
    add_bullet(doc, "Siloed Diagnostic Visibility: ", "Customer support ticket escalations, payment delays, and platform usage metrics are stored in separate operational databases and rarely analyzed together.")
    add_bullet(doc, "Generic Interventions: ", "Customers are offered one-size-fits-all retention discounts rather than targeted interventions addressing their specific root cause of dissatisfaction.")

    doc.add_page_break()

    # ==================== CHAPTER 3 ====================
    add_heading_1(doc, "Chapter 3\nProposed System")
    
    add_heading_2(doc, "3.1 Proposed System Overview")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("The proposed Customer Churn Prediction and Retention System replaces reactive exit interviews with automated machine learning surveillance and prescriptive retention interventions. The architecture consists of three integrated subsystems: (1) Automated Preprocessing & Pipeline Subsystem, (2) Dual-Model Inference & Benchmarking Subsystem, and (3) Prescriptive Web Delivery Subsystem.")

    add_image_safe(doc, os.path.join(fig_dir, "fig_3_1_system_architecture.png"), width_in=5.8, caption="Figure 3.1: Proposed Customer Churn Prediction and Retention System Architecture")

    add_heading_2(doc, "3.2 Key Innovations and Solutions Provided")
    add_bullet(doc, "Dual-Model Consensus Architecture: ", "Provides simultaneous inference across linear log-odds (Logistic Regression) and non-linear hierarchical trees (Decision Tree), allowing operators to verify whether risk is driven by gradual compounding signals or sharp threshold cutoffs.")
    add_bullet(doc, "Prescriptive Retention Playbooks: ", "Rather than merely predicting a probability number, the platform translates detected risk triggers into prioritized corporate actions (e.g., assigning a Tier-3 Customer Success Manager for accounts with over 4 support calls, or offering a 20% annual contract discount for month-to-month accounts).")
    add_bullet(doc, "100% Native Streamlit Layout: ", "Uses native st.container(border=True), st.columns(4), and st.metric() components styled with minimal matte-carbon CSS, ensuring full-width responsiveness without UI clipping.")
    add_bullet(doc, "Schema-Agnostic Preprocessing: ", "The ingestion pipeline automatically identifies target columns (Churn, Exited, target) and dynamically separates categorical and numerical features.")

    add_heading_2(doc, "3.3 Role of the User")
    add_bullet(doc, "Executive / Analyst: ", "Navigates the Overview dashboard to review portfolio health, retention rates, and revenue at risk across customer segments.")
    add_bullet(doc, "Customer Success Manager: ", "Opens Customer Risk Lookup, inputs customer parameters or loads a historical customer profile, clicks 'Run Risk Assessment', and reads the prescribed retention playbook to execute targeted retention outreach.")

    add_heading_2(doc, "3.4 Role of the Developer")
    add_bullet(doc, "Pipeline Maintenance: ", "Ingest updated customer datasets in data/raw/ and execute preprocess.py and train.py.")
    add_bullet(doc, "Model Serialization: ", "Export updated .pkl estimators, preprocessors, and metrics.json into models/.")
    add_bullet(doc, "Deployment Updates: ", "Commit and push changes to GitHub, triggering automatic continuous deployment on Streamlit Community Cloud.")

    add_heading_2(doc, "3.5 Justification and Need for the System")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("Manual monitoring of subscriber retention is unscalable and reactive. A deployed, real-time machine learning system provides customer success teams with automated early-warning alerts, protecting top-line recurring revenue and preventing avoidable subscriber attrition.")

    doc.add_page_break()

    # ==================== CHAPTER 4 ====================
    add_heading_1(doc, "Chapter 4\nDesign")
    
    add_heading_2(doc, "4.1 System Architecture and ML Pipeline")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("The platform implements an end-to-end Machine Learning pipeline comprising offline training and serialization, followed by online inference within the deployed web application:")

    add_image_safe(doc, os.path.join(fig_dir, "fig_4_1_ml_pipeline.png"), width_in=5.8, caption="Figure 4.1: End-to-End Machine Learning Pipeline and Data Transformation Flow")

    add_heading_2(doc, "4.2 Dataset Description and Characteristics")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("The system uses a large-scale subscription customer churn dataset containing 440,833 training samples and 64,374 test samples. The dataset includes demographic, behavioral, contractual, and financial attributes.")

    # Table 4.1
    t41_data = [
        ("Total Records (Training File)", "440,833 customer records"),
        ("Total Records (Testing File)", "64,374 customer records"),
        ("Representative Training Sample", "100,000 records (80,000 train / 20,000 test)"),
        ("Class Distribution (Churned = 1)", "56.71% (249,999 records)"),
        ("Class Distribution (Retained = 0)", "43.29% (190,833 records)"),
        ("Input Features", "10 predictive features (7 numerical, 3 categorical)"),
        ("Target Column", "Churn (Binary: 0 = Retained, 1 = Churned)"),
        ("Identifier Column", "CustomerID (automatically dropped)"),
        ("Missing Values", "1 empty record detected in raw CSV; handled via cleaning")
    ]
    t41 = doc.add_table(rows=len(t41_data)+1, cols=2)
    t41.style = 'Table Grid'
    t41.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, h_text in enumerate(["Attribute", "Specification"]):
        cell = t41.rows[0].cells[idx]
        format_cell(cell, h_text, bold=True)
    for r_idx, (k, v) in enumerate(t41_data):
        row = t41.rows[r_idx+1]
        for c_idx, val in enumerate([k, v]):
            cell = row.cells[c_idx]
            format_cell(cell, val, bold=(c_idx==0))
    add_p(doc, "Table 4.1: Summary Statistics of the Customer Churn Dataset", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12).runs[0].italic = True

    add_heading_2(doc, "4.3 Feature Space Definition (Model Inputs)")
    # Table 4.2
    t42_data = [
        ("Age", "Numerical (float64)", "18 to 65 years", "Age of the customer in years"),
        ("Gender", "Categorical (str)", "Female, Male", "Biological gender of the subscriber"),
        ("Tenure", "Numerical (float64)", "1 to 60 months", "Number of continuous active subscription months"),
        ("Usage Frequency", "Numerical (float64)", "1 to 30 sessions", "Average number of platform login sessions per month"),
        ("Support Calls", "Numerical (float64)", "0 to 10 inquiries", "Total technical and customer support calls logged"),
        ("Payment Delay", "Numerical (float64)", "0 to 30 days", "Average billing settlement delay beyond due date"),
        ("Subscription Type", "Categorical (str)", "Basic, Standard, Premium", "Tier of platform service package"),
        ("Contract Length", "Categorical (str)", "Annual, Monthly, Quarterly", "Customer contract term commitment"),
        ("Total Spend", "Numerical (float64)", "$100 to $1,000", "Cumulative monetary spending across subscription lifetime"),
        ("Last Interaction", "Numerical (float64)", "1 to 30 days", "Number of days elapsed since the last customer touchpoint"),
        ("Churn", "Binary Target", "0 (Retained), 1 (Churned)", "Historical customer attrition outcome")
    ]
    t42 = doc.add_table(rows=len(t42_data)+1, cols=4)
    t42.style = 'Table Grid'
    t42.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, h_text in enumerate(["Feature Name", "Data Type", "Value Range", "Description"]):
        cell = t42.rows[0].cells[idx]
        format_cell(cell, h_text, bold=True)
    for r_idx, row_vals in enumerate(t42_data):
        row = t42.rows[r_idx+1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            format_cell(cell, val, bold=(c_idx==0))
    add_p(doc, "Table 4.2: Feature Space Definition and Attribute Descriptions", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12).runs[0].italic = True

    add_heading_2(doc, "4.4 Data Preparation and Preprocessing Design")
    add_bullet(doc, "Identifier Elimination: ", "Columns such as CustomerID, RowNumber, and Surname carry no predictive signal and are automatically removed to prevent overfitting on database keys.")
    add_bullet(doc, "Missing Value Imputation: ", "Missing numerical values are imputed with the median of the training distribution, which provides robustness against skewed outliers.")
    add_bullet(doc, "Categorical One-Hot Encoding: ", "Categorical attributes (Gender, Subscription Type, Contract Length) are transformed into binary indicator columns via OneHotEncoder(handle_unknown='ignore', sparse_output=False). This expands the 3 categorical variables into 8 binary features.")
    add_bullet(doc, "Standard Feature Scaling: ", "Numerical features have vastly differing magnitudes (e.g., Total Spend up to $1,000 vs. Support Calls up to 10). A StandardScaler() transforms all numeric inputs to zero mean and unit variance, fitted exclusively on training data to prevent data leakage.")
    add_bullet(doc, "Stratified Partitioning: ", "The dataset is partitioned into 80% training and 20% hold-out testing using stratify=y, strictly preserving the 56.7% / 43.3% churn-to-retention ratio across both splits.")

    add_heading_2(doc, "4.5 Models and Evaluation Design")
    t43_data = [
        ("Logistic Regression", "max_iter=1000, class_weight='balanced', solver='lbfgs', random_state=42", "Serves as a transparent linear probabilistic baseline, providing log-odds coefficients for direct risk attribution."),
        ("Decision Tree Classifier", "max_depth=6, min_samples_split=20, class_weight='balanced', random_state=42", "Models complex non-linear feature interactions and threshold cutoffs while remaining interpretable without overfitting.")
    ]
    t43 = doc.add_table(rows=len(t43_data)+1, cols=3)
    t43.style = 'Table Grid'
    t43.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, h_text in enumerate(["Algorithm", "Hyperparameters", "Architectural Rationale"]):
        cell = t43.rows[0].cells[idx]
        format_cell(cell, h_text, bold=True)
    for r_idx, row_vals in enumerate(t43_data):
        row = t43.rows[r_idx+1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            format_cell(cell, val, bold=(c_idx==0))
    add_p(doc, "Table 4.3: Machine Learning Model Hyperparameters and Design Rationales", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12).runs[0].italic = True

    add_heading_2(doc, "4.6 Application Data Flow")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("1. The user enters customer attributes via sliders and dropdowns or clicks 'Load Random Profile'.\n2. The web application structures the inputs into a single-row DataFrame matching the exact schema of the training set.\n3. The saved preprocessor.pkl transforms the input through the fitted imputer, OneHotEncoder, and StandardScaler.\n4. The serialized model (decision_tree.pkl or logistic_regression.pkl) calculates class probabilities.\n5. The application renders a color-coded status badge, a horizontal probability bar, and triggers rule-based prescriptive retention recommendations.")

    add_heading_2(doc, "4.7 Saved Model Artifacts")
    t44_data = [
        ("preprocessor.pkl", "Serialized ColumnTransformer", "Executes identical median imputation, one-hot encoding, and standard scaling on new user inputs."),
        ("decision_tree.pkl", "Serialized DecisionTreeClassifier", "Computes non-linear tree-based probability scores and predicted labels."),
        ("logistic_regression.pkl", "Serialized LogisticRegression", "Computes linear log-odds probabilities and feature coefficients."),
        ("feature_metadata.json", "JSON Metadata Document", "Stores ordered feature names, min/max slider ranges, unique category dropdown lists, and training stats."),
        ("metrics.json", "JSON Evaluation Document", "Stores precision, recall, F1, ROC-AUC, confusion matrices, and ROC coordinates for the dashboard scorecard."),
        ("sample_data.csv", "CSV Data Sample (5,000 records)", "Provides a lightweight, stratified sample for instant dashboard loading on Streamlit Community Cloud without memory overhead.")
    ]
    t44 = doc.add_table(rows=len(t44_data)+1, cols=3)
    t44.style = 'Table Grid'
    t44.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, h_text in enumerate(["File Name", "File Type", "Operational Role"]):
        cell = t44.rows[0].cells[idx]
        format_cell(cell, h_text, bold=True)
    for r_idx, row_vals in enumerate(t44_data):
        row = t44.rows[r_idx+1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            format_cell(cell, val, bold=(c_idx==0))
    add_p(doc, "Table 4.4: Serialized Model Artifacts and Operational Roles", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12).runs[0].italic = True

    doc.add_page_break()

    # ==================== CHAPTER 5 ====================
    add_heading_1(doc, "Chapter 5\nImplementation")
    
    add_heading_2(doc, "5.1 Software Environment and Dependencies")
    t51_data = [
        ("Python", "3.11 / 3.13", "Primary development language and runtime"),
        ("pandas", ">= 2.0.0", "Tabular dataset manipulation, cleaning, and aggregation"),
        ("numpy", ">= 1.24.0", "Numerical array manipulation and vectorized computations"),
        ("scikit-learn", ">= 1.3.0", "Preprocessing pipelines, classification models, and evaluation metrics"),
        ("plotly", ">= 5.15.0", "Interactive chart visualization and styling"),
        ("streamlit", ">= 1.28.0", "Web application delivery framework"),
        ("joblib", ">= 1.3.0", "High-performance serialization of models and pipelines"),
        ("GitHub", "Cloud Git Repository", "Version control, codebase hosting, and CI/CD triggers"),
        ("Streamlit Cloud", "Global Hosting Platform", "Cloud server runtime for worldwide web access")
    ]
    t51 = doc.add_table(rows=len(t51_data)+1, cols=3)
    t51.style = 'Table Grid'
    t51.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, h_text in enumerate(["Component", "Version / Spec", "Role in System Architecture"]):
        cell = t51.rows[0].cells[idx]
        format_cell(cell, h_text, bold=True)
    for r_idx, row_vals in enumerate(t51_data):
        row = t51.rows[r_idx+1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            format_cell(cell, val, bold=(c_idx==0))
    add_p(doc, "Table 5.1: Development Libraries, Platforms, and Runtime Versions", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12).runs[0].italic = True

    add_heading_2(doc, "5.2 Important Code Modules")
    add_heading_3(doc, "(a) Ingestion and Dynamic Cleaning (src/preprocess.py)")
    code_1 = """def clean_data(df: pd.DataFrame, target_col: str, id_cols: list) -> pd.DataFrame:
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
    return cleaned_df"""
    p_c1 = add_p(doc, code_1, space_after=10)
    p_c1.runs[0].font.name = 'Consolas'
    p_c1.runs[0].font.size = Pt(9)

    add_heading_3(doc, "(b) Model Training & Evaluation (src/train.py)")
    code_2 = """# Model 1: Logistic Regression
lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
y_prob_lr = lr.predict_proba(X_test)[:, 1]

# Model 2: Decision Tree Classifier
dt = DecisionTreeClassifier(max_depth=6, min_samples_split=20, class_weight="balanced", random_state=42)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
y_prob_dt = dt.predict_proba(X_test)[:, 1]"""
    p_c2 = add_p(doc, code_2, space_after=10)
    p_c2.runs[0].font.name = 'Consolas'
    p_c2.runs[0].font.size = Pt(9)

    add_heading_2(doc, "5.3 Exploratory Data Analysis")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("Exploratory Data Analysis revealed several critical business and statistical relationships:")
    add_bullet(doc, "Class Distribution: ", "The full training dataset contains 249,999 churned customers (56.71%) and 190,833 retained customers (43.29%), representing a balanced 1.31:1 ratio.")
    add_bullet(doc, "Contract Type Impact: ", "Customers on Month-to-Month contracts exhibit an alarming 100% historical churn rate in this cohort, whereas subscribers enrolled in Annual and Quarterly contracts maintain churn rates of only 46.08% and 46.03% respectively.")
    add_bullet(doc, "Support Ticket Surge: ", "Retained customers average only 1.59 support calls, whereas churned subscribers average 5.14 calls—a dramatic +224.3% surge indicating that unresolved technical friction directly triggers cancellations.")
    add_bullet(doc, "Correlation Analysis: ", "Support Calls exhibits the strongest positive correlation with churn (+0.5743), followed by Payment Delay (+0.3121). Conversely, Total Spend correlates negatively (-0.4294).")

    add_image_safe(doc, os.path.join(fig_dir, "fig_5_1_class_distribution.png"), width_in=4.8, caption="Figure 5.1: Class Distribution of the Customer Churn Dataset")
    add_image_safe(doc, os.path.join(fig_dir, "fig_5_2_contract_churn.png"), width_in=4.8, caption="Figure 5.2: Churn Rate by Contract Length (Annual, Monthly, Quarterly)")
    add_image_safe(doc, os.path.join(fig_dir, "fig_5_3_correlation.png"), width_in=5.2, caption="Figure 5.3: Correlation of Numerical Features with the Churn Target")

    add_heading_2(doc, "5.4 Results and Evaluation Metrics")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("Both models were benchmarked on the identical 20% hold-out test set comprising 20,000 customer records:")

    t52_data = [
        ("Accuracy", "89.85%", "97.95%", "+8.10%", "Decision Tree"),
        ("Precision", "94.10%", "100.00%", "+5.90%", "Decision Tree"),
        ("Recall", "87.59%", "96.39%", "+8.80%", "Decision Tree"),
        ("F1-Score", "90.73%", "98.16%", "+7.43%", "Decision Tree"),
        ("ROC-AUC", "0.9605", "0.9866", "+0.0261", "Decision Tree")
    ]
    t52 = doc.add_table(rows=len(t52_data)+1, cols=5)
    t52.style = 'Table Grid'
    t52.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, h_text in enumerate(["Metric", "Logistic Regression", "Decision Tree", "Variance", "Leading Model"]):
        cell = t52.rows[0].cells[idx]
        format_cell(cell, h_text, bold=True)
    for r_idx, row_vals in enumerate(t52_data):
        row = t52.rows[r_idx+1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            format_cell(cell, val, bold=(c_idx==2 or c_idx==4))
    add_p(doc, "Table 5.2: Performance Evaluation Metrics on the 20% Hold-out Test Set (20,000 Samples)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12).runs[0].italic = True

    add_image_safe(doc, os.path.join(fig_dir, "fig_5_4_model_comparison.png"), width_in=5.2, caption="Figure 5.4: Algorithmic Performance Comparison (Logistic Regression vs. Decision Tree)")

    t53_data = [
        ("Actual Retained (0)", "8,659 (True Negatives)", "0 (False Positives)"),
        ("Actual Churned (1)", "410 (False Negatives)", "10,931 (True Positives)")
    ]
    t53 = doc.add_table(rows=len(t53_data)+1, cols=3)
    t53.style = 'Table Grid'
    t53.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, h_text in enumerate(["Actual Ground Truth", "Predicted Retained (0)", "Predicted Churned (1)"]):
        cell = t53.rows[0].cells[idx]
        format_cell(cell, h_text, bold=True)
    for r_idx, row_vals in enumerate(t53_data):
        row = t53.rows[r_idx+1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            format_cell(cell, val, bold=(c_idx==0))
    add_p(doc, "Table 5.3: Confusion Matrix Contingency Values for Decision Tree Classifier", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12).runs[0].italic = True

    add_image_safe(doc, os.path.join(fig_dir, "fig_5_5_confusion_matrix.png"), width_in=4.4, caption="Figure 5.5: Confusion Matrix of the Decision Tree Classifier (20,000 Test Records)")

    add_heading_2(doc, "5.5 Model Interpretation and Feature Importance")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("The Decision Tree's top split is governed by Support Calls (Gini importance = 0.4160), followed by Total Spend (0.2638), Contract Length_Monthly (0.1384), Payment Delay (0.0989), and Age (0.0828). This confirms that support friction and contract flexibility are the primary drivers of churn.")

    add_image_safe(doc, os.path.join(fig_dir, "fig_5_6_feature_importance.png"), width_in=5.2, caption="Figure 5.6: Top Gini Feature Importances in the Decision Tree Model")

    add_heading_2(doc, "5.6 Deployment Architecture")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("The web application is deployed on Streamlit Community Cloud directly connected to GitHub repository chandelsaksham576/customer-churn-prediction. The deployment utilizes a Matte Carbon Design System (.streamlit/config.toml), Native Component Architecture (st.container(border=True), st.metric), and Zero-Latency In-Memory Inference (<15ms per prediction).")

    doc.add_page_break()

    # ==================== CHAPTER 6 ====================
    add_heading_1(doc, "Chapter 6\nSnapshots")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    p.add_run("Live Deployed Platform: ").bold = True
    p.add_run("https://github.com/chandelsaksham576/customer-churn-prediction")

    add_heading_2(doc, "6.1 Executive Overview Dashboard")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.2)
    p.add_run("The Overview tab presents 4 top KPI cards (Total Customers, Monthly Revenue at Risk, Overall Retention Rate, Churn Rate) and a balanced 2x2 Plotly grid visualizing contract breakdown, tier distribution, spending vs. tenure, and support call escalation.")
    add_image_safe(doc, os.path.join(fig_dir, "fig_6_1_dashboard.png"), width_in=5.8, caption="Figure 6.1: Executive Overview Dashboard (4 Top KPI Cards and 2x2 Plotly Grid)")

    add_heading_2(doc, "6.2 Customer Risk Lookup and Inference Tool")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.2)
    p.add_run("The Customer Risk Lookup tab provides a clean, 3-column bordered parameter input container (Account Profile, Service Subscriptions, Billing & Usage), a model selector radio, and a 'Load Random Profile' button.")
    add_image_safe(doc, os.path.join(fig_dir, "fig_6_3_risk_lookup.png"), width_in=5.8, caption="Figure 6.3: Customer Risk Lookup Form with 3-Column Parameter Inputs and Dual-Model Prediction")

    add_heading_2(doc, "6.3 Prescribed Retention Action Engine")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.2)
    p.add_run("Upon clicking 'Run Risk Assessment', the platform calculates class probabilities, renders a color-coded status badge ('High Churn Risk' or 'Low Churn Risk'), and outputs a prioritized retention playbook detailing specific mitigation actions and expected ROI impact.")

    doc.add_page_break()

    # ==================== CHAPTER 7 ====================
    add_heading_1(doc, "Chapter 7\nConclusion and Future Scope")
    
    add_heading_2(doc, "7.1 Conclusion")
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    p.add_run("In this mini project, a complete end-to-end Customer Churn Prediction and Retention System was successfully designed, evaluated, and deployed. Key achievements include:")
    add_bullet(doc, "End-to-End Scalable Pipeline: ", "Implemented dynamic data ingestion, cleaning, median imputation, one-hot encoding, standard scaling, and stratified 80/20 partitioning across large-scale subscription data.")
    add_bullet(doc, "Empirical Algorithmic Benchmarking: ", "Compared linear and tree-based classification architectures. The Decision Tree Classifier achieved an outstanding 97.95% accuracy, 100% precision, and a 0.9866 ROC-AUC, successfully catching 96.39% of churners with zero false alarms.")
    add_bullet(doc, "Prescriptive Action Engine: ", "Successfully bridged machine learning with executive decision-making by translating statistical probabilities into actionable corporate retention interventions.")
    add_bullet(doc, "Production Web Deployment: ", "Deployed a responsive, matte-dark web application on Streamlit Community Cloud with 100% native component styling and zero runtime errors.")

    add_heading_2(doc, "7.2 Future Scope")
    add_bullet(doc, "Ensemble Integration (XGBoost & LightGBM): ", "Incorporate gradient boosted decision trees to further minimize false negatives.")
    add_bullet(doc, "Automated CRM Integration: ", "Connect the prediction engine directly to enterprise CRM platforms (e.g., Salesforce, HubSpot) via REST APIs to automatically trigger automated email campaigns and support tickets.")
    add_bullet(doc, "Survival Analysis: ", "Implement Cox Proportional Hazards modeling to predict not only if a customer will churn, but the exact expected time until churn.")
    add_bullet(doc, "Explainable AI (SHAP & LIME): ", "Integrate SHAP waterfall plots into the web dashboard to visualize the exact numerical contribution of each feature toward an individual subscriber's risk score.")
    add_bullet(doc, "Automated PDF Export: ", "Enable customer success teams to export single-customer retention dossiers as formatted PDF reports with one click.")

    doc.add_page_break()

    # ==================== CHAPTER 8 ====================
    add_heading_1(doc, "Chapter 8\nReferences")
    
    refs = [
        "Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
        "Breiman, L., Friedman, J., Stone, C. J., and Olshen, R. A. (1984). Classification and Regression Trees. CRC Press.",
        "Hosmer Jr, D. W., Lemeshow, S., and Sturdivant, R. X. (2013). Applied Logistic Regression. John Wiley & Sons.",
        "McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference, 51-56.",
        "Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585(7825), 357-362.",
        "Plotly Technologies Inc. (2025). Collaborative Data Science: Plotly Python Open Source Graphing Library. https://plotly.com/python/",
        "Streamlit Inc. (2025). Streamlit: A faster way to build and share data apps. https://docs.streamlit.io/",
        "Kaggle Inc. (2024). Customer Churn Prediction Dataset. Kaggle Machine Learning Datasets. https://www.kaggle.com",
        "Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters, 27(8), 861-874.",
        "Savitribai Phule Pune University (SPPU). Curriculum and Guidelines for Third Year Engineering (T.E. Information Technology) Mini Project (2026-2027)."
    ]
    for idx, ref_text in enumerate(refs):
        p_ref = add_p(doc, f"[{idx+1}] {ref_text}", space_before=4, space_after=8, line_spacing=1.15)
        p_ref.runs[0].font.size = Pt(11)

    output_path = r"C:\Users\chand\.gemini\antigravity\scratch\customer-churn-prediction\Customer_Churn_Prediction_Report.docx"
    doc.save(output_path)
    print(f"Document saved successfully to {output_path} (size: {os.path.getsize(output_path):,} bytes)")

if __name__ == '__main__':
    create_report()
