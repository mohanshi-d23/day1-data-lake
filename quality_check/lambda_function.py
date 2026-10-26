import csv
import io

from botocore.config import Config
import boto3

s3 = boto3.client("s3", config=Config(retries={"max_attempts": 10, "mode": "standard"}, read_timeout=120))

# s3 = boto3.client("s3")

REQUIRED_COLUMNS = ["VIN (1-10)", "Model Year", "DOL Vehicle ID"]
ID_COLUMN = "DOL Vehicle ID"


def handler(event, context):
    bucket = event["detail"]["bucket"]["name"]
    key = event["detail"]["object"]["key"]

    body = s3.get_object(Bucket=bucket, Key=key)["Body"]
    reader = csv.DictReader(io.TextIOWrapper(body, encoding="utf-8", newline=""))

    # Check 1: required columns exist
    missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
    if missing:
        raise ValueError(f"Missing columns in {key}: {missing}")

    rows = 0
    null_rows = 0
    seen_ids = set()
    duplicate_ids = 0

    for row in reader:
        rows += 1
        # Check 3: no nulls in key columns
        if any(not (row.get(c) or "").strip() for c in REQUIRED_COLUMNS):
            null_rows += 1
        # Check 4: no duplicate IDs
        vid = (row.get(ID_COLUMN) or "").strip()
        if vid in seen_ids:
            duplicate_ids += 1
        else:
            seen_ids.add(vid)

    # Check 2: at least one data row
    if rows == 0:
        raise ValueError(f"{key} has no data rows")
    if null_rows:
        raise ValueError(f"{key}: {null_rows} rows have blank key columns")
    if duplicate_ids:
        raise ValueError(f"{key}: {duplicate_ids} duplicate {ID_COLUMN} values")

    return {"input_path": f"s3://{bucket}/{key}", "rows": rows}