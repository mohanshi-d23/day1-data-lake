import os
import sys

import boto3

BUCKET = os.environ["BUCKET"]          # set with: export BUCKET=...
PROFILE = "data-engineer"


def upload(local_path: str, bucket: str, key: str) -> None:
    session = boto3.Session(profile_name=PROFILE)
    s3 = session.client("s3")

    size_mb = os.path.getsize(local_path) / 1_000_000
    print(f"Uploading {local_path} ({size_mb:.1f} MB) to s3://{bucket}/{key}")

    # upload_file automatically uses multipart upload for large files
    s3.upload_file(local_path, bucket, key)
    print("Upload complete.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_raw.py <local_file>")
        sys.exit(1)

    local_file = sys.argv[1]
    if not os.path.isfile(local_file):
        print(f"File not found: {local_file}")
        sys.exit(1)

    key = "raw/" + os.path.basename(local_file)
    upload(local_file, BUCKET, key)