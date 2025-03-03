import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

bucket_name = 'your-bucket-name'
object_key = 'your-object-key'

try:
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    print(response['Body'].read().decode('utf-8'))

except ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchKey':
        print(f"Object '{object_key}' not found in bucket '{bucket_name}'.")
    else:
        # Handle other potential errors
        print(f"Unexpected error: {e}")
