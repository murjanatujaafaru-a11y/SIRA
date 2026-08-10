import os
import pandas as pd
import requests


def download_raw_data_if_missing(target_path):
    """Automatically fetches the raw dataset from GitHub if it isn't in the data folder."""
    if not os.path.exists(target_path):
        print(f"[Setup] Raw dataset missing. Fetching directly from GitHub...")
        url = "https://raw.githubusercontent.com/devmab24/3Logy-NDI-AI-ML-Crash/main/datasets/incident_reports_1000.csv"
        try:
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            response = requests.get(url)
            if response.status_code == 200:
                with open(target_path, "wb") as f:
                    f.write(response.content)
                print(f"[Setup] Raw dataset successfully downloaded to: {target_path}")
            else:
                print(f"[Error] Failed to download file. Status code: {response.status_code}")
        except Exception as e:
            print(f"[Error] An error occurred while downloading: {e}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "data", "incident_reports_1000.csv")
    output_path = os.path.join(base_dir, "data", "incident_reports_clean.csv")

    # 1. Download raw data if missing
    download_raw_data_if_missing(input_path)

    # 2. Read raw dataset
    df = pd.read_csv(input_path)

    # 3. Strip whitespace from all string columns
    string_columns = df.select_dtypes(include=["object", "string"]).columns
    for col in string_columns:
        df[col] = df[col].astype(str).str.strip()

    # Reset string 'nan' and empty strings back to actual nulls
    df.replace({"nan": None, "": None, "None": None}, inplace=True)

    # 4. Standardize single-letter severity codes (M, L, H)
    severity_map = {"M": "MEDIUM", "L": "LOW", "H": "HIGH"}
    df["severity"] = df["severity"].replace(severity_map)

    # 5. Fix spelling typos in report_text
    typo_corrections = {
        r"\btemprature\b": "temperature",
        r"\btriggred\b": "triggered",
        r"\bmaintainance\b": "maintenance",
        r"\bPresssure\b": "Pressure",
        r"\bPipline\b": "Pipeline",
    }
    for typo, correction in typo_corrections.items():
        df["report_text"] = df["report_text"].str.replace(
            typo, correction, regex=True, case=False
        )

    # 6. Standardize casing
    cat_cols = [
        "location",
        "department",
        "severity",
        "incident_type",
        "shift",
        "status",
    ]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].str.upper()

    df["report_text"] = df["report_text"].str.lower()

    # 7. Fill missing values (Imputation for text/categorical)
    df["report_text"] = df["report_text"].fillna("no report provided")
    df["location"] = df["location"].fillna("UNKNOWN")
    df["reported_by"] = df["reported_by"].fillna("UNKNOWN")
    df["department"] = df["department"].fillna("UNKNOWN")

    # 8. Convert report_date to datetime and impute missing dates
    df["report_date"] = pd.to_datetime(df["report_date"], errors="coerce")
    df["report_date"] = df["report_date"].ffill().bfill()
    df["report_date"] = df["report_date"].dt.strftime("%Y-%m-%d")

    # 9. Deduplicate
    feature_cols = [col for col in df.columns if col != "incident_id"]
    df = df.drop_duplicates(subset=feature_cols)

    # 10. Save cleaned dataset
    df.to_csv(output_path, index=False)
    print(
        f"[Success] Data cleaned successfully! Saved {len(df)} clean rows to: {output_path}"
    )


if __name__ == "__main__":
    main()