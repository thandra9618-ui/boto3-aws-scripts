import boto3

ec2 = boto3.client('ec2')

response = ec2.create_vpc(
    CidrBlock='10.0.0.0/16'
)

vpc_id = response['Vpc']['VpcId']
print("Created VPC with ID:", vpc_id)
