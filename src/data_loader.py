import io
import boto3
import pandas as pd

class DataLoader:
    """Encapsulates AWS S3 operations for reading and writing SIRA datasets."""

    def __init__(self, bucket_name: str, region_name: str = "eu-central-1"):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3", region_name=region_name)

    def load_csv_from_s3(self, s3_key: str) -> pd.DataFrame:
        """Retrieves a CSV object from S3 into a Pandas DataFrame."""
        print(f"[DataLoader] Fetching s3://{self.bucket_name}/{s3_key}...")
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            return pd.read_csv(io.BytesIO(response["Body"].read()))
        except Exception as e:
            print(f"[DataLoader] Error loading from S3: {e}")
            raise e

    def upload_csv_to_s3(self, df: pd.DataFrame, s3_key: str) -> None:
        """Uploads a Pandas DataFrame to S3 as a CSV object."""
        print(f"[DataLoader] Uploading dataset to s3://{self.bucket_name}/{s3_key}...")
        try:
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=csv_buffer.getvalue()
            )
            print(f"[DataLoader] Upload successful: s3://{self.bucket_name}/{s3_key}")
        except Exception as e:
            print(f"[DataLoader] Error uploading to S3: {e}")
            raise e
