import boto3
import os
import json

def load_credentials(credentials_file):
  """Loads AWS credentials from a JSON file."""
  with open(credentials_file, 'r') as f:
    credentials = json.load(f)
  return credentials

def sync_directory_to_s3(local_dir, bucket_name, prefix=''):
  """Syncs a local directory to an S3 bucket.

  Args:
    local_dir: The local directory to sync.
    bucket_name: The name of the S3 bucket.
    prefix: The optional prefix for the S3 objects.
  """
  credentials_file = "/home/mainframe/.creds/aws.json"
  credentials = load_credentials(credentials_file)
  session = boto3.Session(
      aws_access_key_id=credentials['aws_access_key_id'],
      aws_secret_access_key=credentials['aws_secret_access_key'],
      region_name=credentials.get('region_name', 'us-east-1')
  )

  s3 = session.client('s3')

  for root, dirs, files in os.walk(local_dir):
    for file in files:
      local_path = os.path.join(root, file)
      relative_path = os.path.relpath(local_path, local_dir)
      s3_path = os.path.join(prefix, relative_path)

      try:
        s3.upload_file(local_path, bucket_name, s3_path)
        print(f"Uploaded {local_path} to s3://{bucket_name}/{s3_path}")
      except Exception as e:
        print(f"Error uploading {local_path}: {e}")

if __name__ == "__main__":
  local_dir = '/home/mainframe/IOTstack'
  bucket_name = 'wycloud-backup'
  prefix = 'theflame/IOTstack'  # Optional

  sync_directory_to_s3(local_dir, bucket_name, prefix)