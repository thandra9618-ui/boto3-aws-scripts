import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def main():
    try:
        # Create a session using default AWS profile
        session = boto3.Session()

        # Connect to S3 service
        s3 = session.client("s3")

        # List all S3 buckets
        response = s3.list_buckets()

        print("Your S3 Buckets:")
        for bucket in response.get("Buckets", []):
            print(" -", bucket["Name"])

    except NoCredentialsError:
        print("Error: No AWS credentials found. Run 'aws configure' first.")
    except ClientError as e:
        print("AWS Error:", e)

if __name__ == "__main__":
    main()
