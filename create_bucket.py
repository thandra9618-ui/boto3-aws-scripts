import boto3
from botocore.exceptions import ClientError

# Connect to S3
s3 = boto3.client("s3", region_name="us-east-1")  # change region if needed

bucket_name = "my-first-python-bucket-2025-siva"  # must be unique

try:
    # For us-east-1, CreateBucketConfiguration is not needed
    if s3.meta.region_name == 'us-east-1':
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': s3.meta.region_name}
        )
    print(f"Bucket '{bucket_name}' created successfully!")

except ClientError as e:
    print("Error creating bucket:", e)
