"""
data/extract_data.py
Auto-detects Kaggle customer churn .zip files in the workspace / data directories,
extracts them into data/raw/, and inspects schema and summary stats.
"""

import os
import sys
import glob
import zipfile
import pandas as pd
from pathlib import Path

# Force UTF-8 stdout encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def get_base_dirs():
    """Return relevant directories to search for zip files and save extracted data."""
    script_dir = Path(__file__).resolve().parent
    project_dir = script_dir.parent
    raw_dir = script_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    return project_dir, script_dir, raw_dir

def find_zip_files():
    """Locate any .zip files in root, data/, or parent scratch/brain directories."""
    project_dir, data_dir, _ = get_base_dirs()
    search_paths = [
        str(project_dir / "*.zip"),
        str(data_dir / "*.zip"),
        str(project_dir.parent / "*.zip"),
        # Also check user upload folder if applicable
        r"C:\Users\chand\.gemini\antigravity\brain\3d2d8420-122d-4418-9e46-a1057ba864c6\.user_uploaded\*.zip"
    ]
    
    zip_files = []
    for pattern in search_paths:
        for match in glob.glob(pattern):
            if match not in zip_files:
                zip_files.append(match)
    return zip_files

def extract_and_inspect():
    project_dir, data_dir, raw_dir = get_base_dirs()
    print("=" * 70)
    print("🔍 DATA EXTRACTION & SCHEMA INSPECTION")
    print("=" * 70)
    print(f"Project directory: {project_dir}")
    print(f"Target raw directory: {raw_dir}")

    zip_candidates = find_zip_files()
    if not zip_candidates:
        print("⚠️ No .zip files detected directly. Checking if CSV files already exist in data/raw/...")
    else:
        print(f"📦 Found {len(zip_candidates)} zip archive(s):")
        for zf_path in zip_candidates:
            print(f"   - {zf_path}")
            try:
                with zipfile.ZipFile(zf_path, 'r') as zip_ref:
                    file_list = zip_ref.namelist()
                    print(f"     Archive contents: {file_list}")
                    for file_info in zip_ref.infolist():
                        if file_info.filename.lower().endswith(".csv") and not file_info.filename.startswith("__MACOSX"):
                            target_path = raw_dir / Path(file_info.filename).name
                            with open(target_path, "wb") as out_f:
                                out_f.write(zip_ref.read(file_info.filename))
                            print(f"     ✅ Extracted: {target_path.name} ({target_path.stat().st_size:,} bytes)")
            except Exception as e:
                print(f"     ❌ Error extracting {zf_path}: {e}")

    # Inspect all extracted CSV files in data/raw/
    csv_files = list(raw_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {raw_dir} after extraction.")

    print("\n" + "=" * 70)
    print("📊 DATASET SCHEMA INSPECTION")
    print("=" * 70)

    inspected_datasets = {}
    for csv_file in csv_files:
        print(f"\n📄 Inspecting: {csv_file.name}")
        df = pd.read_csv(csv_file, nrows=5000)  # fast sample inspection
        total_rows = sum(1 for _ in open(csv_file, encoding='utf-8', errors='ignore')) - 1
        
        print(f"   - File size: {csv_file.stat().st_size:,} bytes")
        print(f"   - Total rows: {total_rows:,}, Columns: {len(df.columns)}")
        print(f"   - Exact Column Names: {list(df.columns)}")
        print("\n   - Data Types & Missing Values (First 5000 sample):")
        summary_table = pd.DataFrame({
            "DataType": df.dtypes,
            "NullCount": df.isnull().sum(),
            "NullPct": (df.isnull().sum() / len(df) * 100).round(2),
            "SampleValue": df.iloc[0]
        })
        print(summary_table.to_string())

        print("\n   - First 5 Rows Preview:")
        print(df.head(5).to_string())
        print("-" * 70)
        inspected_datasets[csv_file.name] = {
            "path": str(csv_file),
            "columns": list(df.columns),
            "shape": (total_rows, len(df.columns))
        }

    return inspected_datasets

if __name__ == "__main__":
    extract_and_inspect()
