import boto3
import time

# 1. Create EC2 client
ec2 = boto3.client('ec2', region_name='us-east-1')  # change region if needed

# 2. Create a VPC
vpc_response = ec2.create_vpc(
    CidrBlock='10.0.0.0/16'
)
vpc_id = vpc_response['Vpc']['VpcId']
print("Created VPC ID:", vpc_id)

# Wait for VPC to be available
ec2.get_waiter('vpc_available').wait(VpcIds=[vpc_id])

# 3. Create a Subnet inside this VPC
subnet_response = ec2.create_subnet(
    CidrBlock='10.0.1.0/24',
    VpcId=vpc_id
)
subnet_id = subnet_response['Subnet']['SubnetId']
print("Created Subnet ID:", subnet_id)

# 4. Optional: Add a Name tag to subnet
ec2.create_tags(
    Resources=[subnet_id],
    Tags=[{'Key': 'Name', 'Value': 'MySubnet'}]
)

print("Subnet created and tagged successfully!")
