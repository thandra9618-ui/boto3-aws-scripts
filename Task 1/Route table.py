import boto3
import time

# 1. Create EC2 client
ec2 = boto3.client('ec2', region_name='us-east-1')  # change region if needed

# 2. Create a VPC (if you don't have one already)
vpc_response = ec2.create_vpc(
    CidrBlock='10.0.0.0/16'
)
vpc_id = vpc_response['Vpc']['VpcId']
print("Created VPC ID:", vpc_id)

# Wait until VPC is available
ec2.get_waiter('vpc_available').wait(VpcIds=[vpc_id])

# 3. Create Route Table in the VPC
route_table_response = ec2.create_route_table(
    VpcId=vpc_id
)
route_table_id = route_table_response['RouteTable']['RouteTableId']
print("Created Route Table ID:", route_table_id)

# 4. Optional: Tag the Route Table
ec2.create_tags(
    Resources=[route_table_id],
    Tags=[{'Key': 'Name', 'Value': 'MyRouteTable'}]
)

print("Route Table created and tagged successfully!")
