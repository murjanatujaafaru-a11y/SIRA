import pandas as pd
import numpy as np

class IncidentPreprocessor:
    """An automated, object-oriented pipeline engine to resolve data quality anomalies."""
    
    def __init__(self):
        pass

    def clean_text_and_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardizes casing, strips hidden whitespaces, and handles categorical fields."""
        df = df.copy()
        
        categorical_cols = ['location', 'incident_type', 'severity', 'department', 'status']
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.upper()
        
        if 'incident_type' in df.columns:
            df['incident_type'] = df['incident_type'].replace({'NAN': 'UNKNOWN', '': 'UNKNOWN', 'NONE': 'UNKNOWN'})
            
        return df

    def fix_timestamps(self, df: pd.DataFrame) -> pd.DataFrame:
        """Converts the real report_date column into uniform datetime objects."""
        df = df.copy()
        if 'report_date' in df.columns:
            df['report_date'] = pd.to_datetime(df['report_date'], errors='coerce')
            df['report_date'] = df['report_date'].ffill()
        return df

    def handle_numerical_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensures ID columns or any numerical codes present are stripped and formatted."""
        df = df.copy()
        if 'incident_id' in df.columns:
            df['incident_id'] = pd.to_numeric(df['incident_id'], errors='coerce')
        return df

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Runs the step-by-step cleaning lifecycle on the input DataFrame."""
        df = df.copy()
        
        df.columns = df.columns.str.strip().str.lower()
        print(f"[Pipeline] Processing columns: {list(df.columns)}")
        
        df = df.drop_duplicates().reset_index(drop=True)
        
        df = self.clean_text_and_categories(df)
        df = self.fix_timestamps(df)
        df = self.handle_numerical_anomalies(df)
        
        subset_cols = [col for col in ['report_date', 'location', 'incident_type'] if col in df.columns]
        df = df.drop_duplicates(subset=subset_cols).reset_index(drop=True)
        
        print(f"[Pipeline] Processing complete. Final record count: {len(df)} rows.")
        return df

# Alias so both class names work seamlessly
DataCleaner = IncidentPreprocessor
