# from pathlib import Path
# import pandas as pd

# class DataLoader:
#     """
#     Responsible for loading datasets.

#     This class has only one responsibility:
#     Reading datasets from storage.
#     """

#     def __init__(self):
#         project_root = Path(__file__).resolve().parent.parent
#         self.data_path = project_root / "data" / "raw" / "incident_reports.csv"
        
#     def load_data(self):
#         # 1. Load the CSV into a DataFrame
#         df = pd.read_csv(self.data_path)

#         # 2. Force all column names to lowercase and replace spaces with underscores
#         #    This safely handles variations like "Report Text", "Report_Text", or "REPORT_TEXT"
#         df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

#         return df

import os
import pandas as pd

class DataLoader:
    """Handles secure loading operations for the incident dataset."""
    
    def __init__(self, file_path: str):
        """Initializes the loader with a specific target file path."""
        self.file_path = file_path

    def load_data(self) -> pd.DataFrame:
        """Loads the CSV data into a Pandas DataFrame, checking for existence."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Target data file not found at: {self.file_path}")
        
        df = pd.read_csv(self.file_path)
        print(f"[IO] Successfully loaded dataset with {len(df)} initial records.")
        return df