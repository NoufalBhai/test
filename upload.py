import csv
import json
import base64
from io import StringIO, BytesIO

def is_valid_csv(content):
    try:
        # Decode bytes to string for CSV parsing
        content_str = content.decode('utf-8')
        csv_reader = csv.reader(StringIO(content_str))
        # Validate by attempting to read the first row
        headers = next(csv_reader, None)
        if headers:
            return True
    except Exception as e:
        print(f"CSV validation error: {e}")
    return False

def lambda_handler(event, context):
    try:
        # Decode the raw binary content if Base64-encoded
        is_base64 = event.get("isBase64Encoded", False)
        file_content = base64.b64decode(event["body"]) if is_base64 else event["body"].encode()

        # Validate if the file is a CSV
        if not is_valid_csv(file_content):
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Uploaded file is not a valid CSV."}),
            }

        # Process the CSV file
        file_size = len(file_content)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "CSV file uploaded successfully.",
                "file_size": file_size
            }),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
