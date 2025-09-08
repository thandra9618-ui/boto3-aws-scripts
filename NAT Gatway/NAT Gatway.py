import boto3
import time

# Create EC2 client
ec2 = boto3.client('ec2', region_name='us-east-1')  # replace with your region

# --- Step 1: Create VPC ---
vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc_response['Vpc']['VpcId']
print("Created VPC:", vpc_id)

# Wait for VPC to become available
ec2.get_waiter('vpc_available').wait(VpcIds=[vpc_id])

# --- Step 2: Create a Public Subnet ---
subnet_response = ec2.create_subnet(
    CidrBlock='10.0.1.0/24',
    VpcId=vpc_id
)
subnet_id = subnet_response['Subnet']['SubnetId']
print("Created Subnet:", subnet_id)

# --- Step 3: Allocate Elastic IP ---
eip_response = ec2.allocate_address(Domain='vpc')
allocation_id = eip_response['AllocationId']
print("Allocated Elastic IP:", eip_response['PublicIp'])

# --- Step 4: Create NAT Gateway ---
nat_response = ec2.create_nat_gateway(
    SubnetId=subnet_id,
    AllocationId=allocation_id
)
nat_id = nat_response['NatGateway']['NatGatewayId']
print("Creating NAT Gateway:", nat_id)

# --- Step 5: Wait until NAT Gateway is available ---
print("Waiting for NAT Gateway to become available...")
waiter = ec2.get_waiter('nat_gateway_available')
waiter.wait(NatGatewayIds=[nat_id])

print("NAT Gateway is now available:", nat_id)
