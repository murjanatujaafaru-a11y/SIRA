import os
import pandas as pd
import requests
from src.data_loader import DataLoader
from src.preprocessing import IncidentPreprocessor

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
    
    print("=========================================")
    print("Starting SIRA Automated Processing Pipeline")
    print("=========================================")
    
    # Check and automatically pull down the raw dataset if needed
    download_raw_data_if_missing(input_path)
    
    # 1. Load Data
    loader = DataLoader(input_path)
    raw_df = loader.load_data()
    
    # 2. Preprocess Data
    processor = IncidentPreprocessor()
    cleaned_df = processor.fit_transform(raw_df)
    
    # 3. Export Clean Data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cleaned_df.to_csv(output_path, index=False)
    print(f"[Export] Saved final cleaned version to: {output_path}")
    print("=========================================")

if __name__ == "__main__":
    main()