import json
import os

from test_metabase.settings import GOOGLE_SERVICE_FILE, BUCKET_NAME, BASE_DIR
from google.cloud import storage
from google.oauth2 import service_account

with open(os.path.join(BASE_DIR, GOOGLE_SERVICE_FILE)) as f:
    gcp_json_credentials_dict = json.load(f)
credentials = service_account.Credentials.from_service_account_info(gcp_json_credentials_dict)
storage_client = storage.Client(project=gcp_json_credentials_dict['project_id'], credentials=credentials)


def download_google_bucket_blob(file_name: str) -> str:
    """Downloads a blob from the bucket."""
    bucket_name = BUCKET_NAME
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    return blob.download_as_text()

