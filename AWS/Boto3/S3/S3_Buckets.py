import boto3

def list_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response.get('Buckets', [])]
    return bucket_names

if __name__ == "__main__":
    print(list_s3_buckets())