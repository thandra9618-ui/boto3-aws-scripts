import boto3

# Create a session
session = boto3.Session()

# Connect to S3 service
s3 = session.client("s3")

# List buckets
response = s3.list_buckets()

print("Your S3 Buckets are:")
for bucket in response["Buckets"]:
    print(" -", bucket["Name"])
