from src.data_loader import DataLoader
from src.preprocessing import IncidentPreprocessor

class SIRAPipeline:
    """Object-Oriented Orchestrator for the SIRA Machine Learning Pipeline."""

    def __init__(self, bucket_name: str, raw_key: str, processed_key: str):
        self.bucket_name = bucket_name
        self.raw_key = raw_key
        self.processed_key = processed_key
        
        self.loader = DataLoader(bucket_name=self.bucket_name)
        self.preprocessor = IncidentPreprocessor()

    def run(self):
        print("=" * 60)
        print("          SIRA OOP PIPELINE EXECUTION STARTED         ")
        print("=" * 60)

        raw_df = self.loader.load_csv_from_s3(self.raw_key)
        print(f"[Pipeline] Loaded {len(raw_df)} initial records from S3.")

        cleaned_df = self.preprocessor.fit_transform(raw_df)

        print("\n" + "=" * 60)
        print("                CLEANED DATA PREVIEW                  ")
        print("=" * 60)
        print(cleaned_df.head(3))

        self.loader.upload_csv_to_s3(cleaned_df, self.processed_key)
        print("\n[Pipeline] OOP Pipeline execution finished successfully!")


if __name__ == "__main__":
    # Permitted SageMaker S3 bucket
    BUCKET = "amazon-sagemaker-037941994053-eu-central-1-d8ya19xhaqdz7v"  
    RAW_KEY = "raw/incident_reports_1000.csv"
    PROCESSED_KEY = "processed/incident_reports_clean.csv"

    pipeline = SIRAPipeline(bucket_name=BUCKET, raw_key=RAW_KEY, processed_key=PROCESSED_KEY)
    pipeline.run()
