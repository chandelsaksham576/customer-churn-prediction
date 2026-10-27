"""
src/preprocess.py
Data cleaning, dynamic schema inspection, feature engineering, scaling,
and stratified train-test split for Customer Churn Prediction.
"""

import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import joblib

# Force UTF-8 stdout encoding on Windows with line buffering
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

# Default project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Candidate target column names commonly found in churn datasets
TARGET_CANDIDATES = ["churn", "exited", "churn_value", "target", "churned", "is_churn"]

# Non-predictive identifier columns to automatically drop
ID_CANDIDATES = [
    "customerid", "customer_id", "client_id", "userid", "user_id",
    "rownumber", "row_number", "id", "surname", "unnamed: 0", "index"
]

def find_primary_dataset(raw_dir: Path = RAW_DATA_DIR) -> Path:
    """
    Locates the primary raw CSV dataset.
    Prioritizes training sets if multiple are found.
    """
    csv_files = list(raw_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {raw_dir}")

    # Prioritize files containing 'train' or 'master'
    for f in csv_files:
        fname = f.name.lower()
        if "train" in fname:
            return f
    for f in csv_files:
        if "test" not in f.name.lower():
            return f
    return csv_files[0]

def detect_target_and_id_columns(df: pd.DataFrame):
    """Dynamically detects the target churn column and any identifier columns."""
    target_col = None
    cols_lower = {col.lower(): col for col in df.columns}
    
    for candidate in TARGET_CANDIDATES:
        if candidate in cols_lower:
            target_col = cols_lower[candidate]
            break
            
    if target_col is None:
        # Fallback: find any binary column with name containing 'churn'
        for col in df.columns:
            if "churn" in col.lower():
                target_col = col
                break
                
    if target_col is None:
        raise ValueError(f"Could not identify a churn target column from: {list(df.columns)}")

    # Detect ID columns
    id_cols = [cols_lower[cand] for cand in ID_CANDIDATES if cand in cols_lower]
    return target_col, id_cols

def clean_data(df: pd.DataFrame, target_col: str, id_cols: list) -> pd.DataFrame:
    """
    Cleans raw dataframe:
    - Drops ID columns
    - Drops rows where target is missing
    - Encodes target into binary (0/1)
    - Converts numerical columns stored as strings (handling spaces, currencies, commas)
    - Imputes missing numerical values with median
    """
    cleaned_df = df.copy()

    # Drop ID columns
    cols_to_drop = [col for col in id_cols if col in cleaned_df.columns]
    if cols_to_drop:
        cleaned_df = cleaned_df.drop(columns=cols_to_drop)

    # Clean target: drop nulls and map to 0/1
    cleaned_df = cleaned_df.dropna(subset=[target_col])
    if cleaned_df[target_col].dtype == object or str(cleaned_df[target_col].dtype) == "category":
        # Handle "Yes"/"No", "True"/"False", "Churned"/"Retained", "1"/"0"
        mapping = {
            "yes": 1, "no": 0, "true": 1, "false": 0,
            "churn": 1, "retained": 0, "churned": 1, "1": 1, "0": 0, 1: 1, 0: 0
        }
        cleaned_df[target_col] = cleaned_df[target_col].astype(str).str.strip().str.lower().map(mapping)
    else:
        cleaned_df[target_col] = cleaned_df[target_col].astype(int)

    # Convert potential string numeric columns (e.g., TotalCharges with blank spaces or symbols)
    for col in cleaned_df.columns:
        if col == target_col:
            continue
        if not pd.api.types.is_numeric_dtype(cleaned_df[col]):
            # Check if this column consists largely of numeric strings
            s = cleaned_df[col].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False).str.strip()
            numeric_conv = pd.to_numeric(s, errors="coerce")
            valid_ratio = numeric_conv.notnull().sum() / len(cleaned_df)
            if valid_ratio > 0.6:  # Over 60% valid numbers -> convert to float
                cleaned_df[col] = numeric_conv
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())

    return cleaned_df

def build_preprocessor(categorical_features: list, numerical_features: list) -> ColumnTransformer:
    """
    Constructs ColumnTransformer pipeline:
    - Categorical: SimpleImputer (most_frequent) -> OneHotEncoder(handle_unknown='ignore')
    - Numerical: SimpleImputer (median) -> StandardScaler()
    """
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numerical_features),
            ("cat", cat_pipeline, categorical_features)
        ],
        remainder="drop"
    )
    return preprocessor

def get_encoded_feature_names(preprocessor: ColumnTransformer, numerical_features: list, categorical_features: list) -> list:
    """Extracts interpretable feature names post one-hot encoding and scaling."""
    feature_names = list(numerical_features)
    if categorical_features and "cat" in preprocessor.named_transformers_:
        onehot_step = preprocessor.named_transformers_["cat"].named_steps["onehot"]
        encoded_cats = onehot_step.get_feature_names_out(categorical_features)
        feature_names.extend(list(encoded_cats))
    return feature_names

def run_preprocessing(data_path: Path = None, sample_size: int = 100000, random_state: int = 42):
    """
    Full preprocessing execution:
    1. Loads data
    2. Identifies schema (target, categorical, numerical)
    3. Cleans data
    4. Stratified 80/20 train-test split
    5. Fits & saves preprocessor pipeline
    6. Extracts & saves feature metadata for UI and inference
    """
    if data_path is None:
        data_path = find_primary_dataset()

    print(f"📂 Loading dataset from: {data_path}")
    raw_df = pd.read_csv(data_path)
    print(f"   Raw shape: {raw_df.shape[0]:,} rows, {raw_df.shape[1]} columns")

    target_col, id_cols = detect_target_and_id_columns(raw_df)
    print(f"   🎯 Identified Target: '{target_col}'")
    print(f"   🆔 Identified ID Columns to drop: {id_cols}")

    cleaned_df = clean_data(raw_df, target_col, id_cols)

    # Subsample if dataset is extraordinarily massive to ensure swift training while retaining statistical power
    if sample_size and len(cleaned_df) > sample_size:
        print(f"   ⚡ Subsampling to representative stratified sample of {sample_size:,} rows for rapid optimal training...")
        cleaned_df, _ = train_test_split(
            cleaned_df, train_size=sample_size, stratify=cleaned_df[target_col], random_state=random_state
        )
        cleaned_df = cleaned_df.reset_index(drop=True)

    X = cleaned_df.drop(columns=[target_col])
    y = cleaned_df[target_col].astype(int)

    numerical_features = [col for col in X.columns if pd.api.types.is_numeric_dtype(X[col])]
    categorical_features = [col for col in X.columns if col not in numerical_features]

    print(f"   Categorical features ({len(categorical_features)}): {categorical_features}")
    print(f"   Numerical features ({len(numerical_features)}): {numerical_features}")
    print(f"   Churn rate: {(y.mean() * 100):.2f}% ({y.sum():,} churned / {len(y):,} total)")

    # Stratified Train-Test Split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=random_state
    )
    print(f"   Train split: {len(X_train):,} rows | Test split: {len(X_test):,} rows")

    # Fit preprocessor
    preprocessor = build_preprocessor(categorical_features, numerical_features)
    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)

    # Feature names
    encoded_feature_names = get_encoded_feature_names(preprocessor, numerical_features, categorical_features)

    # Collect metadata for UI controls and inference recommendations
    feature_metadata = {
        "target_column": target_col,
        "id_columns": id_cols,
        "numerical_features": numerical_features,
        "categorical_features": categorical_features,
        "encoded_feature_names": encoded_feature_names,
        "total_records": int(len(cleaned_df)),
        "train_records": int(len(X_train)),
        "test_records": int(len(X_test)),
        "churn_rate": float(y.mean()),
        "feature_stats": {
            col: {
                "min": float(X[col].min()),
                "max": float(X[col].max()),
                "median": float(X[col].median()),
                "mean": float(X[col].mean()),
                "default": float(X[col].median())
            } for col in numerical_features
        },
        "categorical_unique": {
            col: sorted([str(v) for v in X[col].dropna().unique().tolist()])
            for col in categorical_features
        }
    }

    # Save artifacts
    joblib.dump(preprocessor, MODELS_DIR / "preprocessor.pkl")
    with open(MODELS_DIR / "feature_metadata.json", "w", encoding="utf-8") as f:
        json.dump(feature_metadata, f, indent=4)

    # Save processed numpy arrays / test splits for model training and evaluation
    processed_data = {
        "X_train": X_train_trans,
        "X_test": X_test_trans,
        "y_train": y_train.values,
        "y_test": y_test.values,
        "X_train_df": X_train,
        "X_test_df": X_test,
        "raw_cleaned_sample": cleaned_df.head(10000)
    }
    joblib.dump(processed_data, MODELS_DIR / "processed_data.pkl")

    print(f"✅ Preprocessing complete! Artifacts saved to: {MODELS_DIR}")
    return preprocessor, feature_metadata, processed_data

if __name__ == "__main__":
    run_preprocessing()
