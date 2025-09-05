import boto3

def list_ec2_instances(region_name='us-east-1'):
    ec2 = boto3.client('ec2', region_name=region_name)
    response = ec2.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance['InstanceId'])
    return instances

def list_iam_users():
    iam = boto3.client('iam')
    response = iam.list_users()
    users = [user['UserName'] for user in response['Users']]
    return users

def list_iam_groups():
    iam = boto3.client('iam')
    paginator = iam.get_paginator('list_groups')
    groups = []
    for page in paginator.paginate():
        groups.extend([group['GroupName'] for group in page['Groups']])
    return groups

def list_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response.get('Buckets', [])]
    return bucket_names

if __name__ == "__main__":
    print("EC2 Instances:", list_ec2_instances())
    print("IAM Users:", list_iam_users())
    print("IAM Groups:", list_iam_groups())
    print("S3 Buckets:", list_s3_buckets())