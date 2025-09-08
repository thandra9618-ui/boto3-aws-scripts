import boto3
import time

# ======================================================
# AWS Lambda Function Creation
# ======================================================
def create_lambda_function():
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    with open('lambda_function.zip', 'rb') as f:
        zipped_code = f.read()

    role_arn = 'arn:aws:iam::<ACCOUNT_ID>:role/<LAMBDA_EXECUTION_ROLE>'  # replace with your IAM role ARN

    response = lambda_client.create_function(
        FunctionName='MyLambdaFunction',
        Runtime='python3.9',
        Role=role_arn,
        Handler='lambda_function.lambda_handler',
        Code={'ZipFile': zipped_code},
        Description='My first Lambda created with boto3',
        Timeout=10,
        MemorySize=128,
    )

    print("Created Lambda Function Name:", response['FunctionName'])
    print("Lambda ARN:", response['FunctionArn'])


# ======================================================
# Create VPC + Subnet + NAT Gateway
# ======================================================
def create_vpc_with_nat():
    ec2 = boto3.client('ec2', region_name='us-east-1')

    # VPC
    vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc_response['Vpc']['VpcId']
    print("Created VPC:", vpc_id)

    ec2.get_waiter('vpc_available').wait(VpcIds=[vpc_id])

    # Subnet
    subnet_response = ec2.create_subnet(
        CidrBlock='10.0.1.0/24',
        VpcId=vpc_id
    )
    subnet_id = subnet_response['Subnet']['SubnetId']
    print("Created Subnet:", subnet_id)

    # Elastic IP
    eip_response = ec2.allocate_address(Domain='vpc')
    allocation_id = eip_response['AllocationId']
    print("Allocated Elastic IP:", eip_response['PublicIp'])

    # NAT Gateway
    nat_response = ec2.create_nat_gateway(
        SubnetId=subnet_id,
        AllocationId=allocation_id
    )
    nat_id = nat_response['NatGateway']['NatGatewayId']
    print("Creating NAT Gateway:", nat_id)

    print("Waiting for NAT Gateway to become available...")
    waiter = ec2.get_waiter('nat_gateway_available')
    waiter.wait(NatGatewayIds=[nat_id])
    print("NAT Gateway is now available:", nat_id)


# ======================================================
# Create Route Table in VPC
# ======================================================
def create_route_table():
    ec2 = boto3.client('ec2', region_name='us-east-1')

    vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc_response['Vpc']['VpcId']
    print("Created VPC ID:", vpc_id)

    ec2.get_waiter('vpc_available').wait(VpcIds=[vpc_id])

    route_table_response = ec2.create_route_table(VpcId=vpc_id)
    route_table_id = route_table_response['RouteTable']['RouteTableId']
    print("Created Route Table ID:", route_table_id)

    ec2.create_tags(
        Resources=[route_table_id],
        Tags=[{'Key': 'Name', 'Value': 'MyRouteTable'}]
    )

    print("Route Table created and tagged successfully!")


# ======================================================
# Create SNS Topic and Publish Message
# ======================================================
def create_sns_topic():
    sns = boto3.client('sns', region_name='us-east-1')

    topic_response = sns.create_topic(Name='MySNSTopic')
    topic_arn = topic_response['TopicArn']
    print("Created SNS Topic ARN:", topic_arn)

    subscribe_response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint='your-email@example.com'  # replace with your email
    )
    print("Subscription ARN (pending confirmation):", subscribe_response['SubscriptionArn'])

    publish_response = sns.publish(
        TopicArn=topic_arn,
        Message='Hello from Python SNS!',
        Subject='Test Notification'
    )
    print("Message ID:", publish_response['MessageId'])


# ======================================================
# Create SQS Queue and Send/Receive Messages
# ======================================================
def create_sqs_queue():
    sqs = boto3.client('sqs', region_name='us-east-1')

    queue_name = 'MyQueue'
    response = sqs.create_queue(
        QueueName=queue_name,
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '86400'
        }
    )

    queue_url = response['QueueUrl']
    print("Created SQS Queue URL:", queue_url)

    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody='Hello from boto3 SQS!'
    )
    print("Message sent successfully!")

    messages = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=2
    )

    if 'Messages' in messages:
        for msg in messages['Messages']:
            print("Received message:", msg['Body'])
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg['ReceiptHandle']
            )
            print("Message deleted from queue")
    else:
        print("No messages in queue")


# ======================================================
# Create and Retrieve SSM Parameter
# ======================================================
def manage_ssm_parameter():
    ssm = boto3.client('ssm', region_name='us-east-1')

    parameter_name = "/MyApp/Password"
    parameter_value = "SuperSecret123"

    try:
        ssm.put_parameter(
            Name=parameter_name,
            Value=parameter_value,
            Type='SecureString',
            Overwrite=True
        )
        print(f"Parameter '{parameter_name}' created successfully!")
    except Exception as e:
        print("Error creating parameter:", e)

    try:
        response = ssm.get_parameter(
            Name=parameter_name,
            WithDecryption=True
        )
        print(f"Retrieved Parameter Value: {response['Parameter']['Value']}")
    except Exception as e:
        print("Error retrieving parameter:", e)


# ======================================================
# Create Subnet in VPC
# ======================================================
def create_subnet():
    ec2 = boto3.client('ec2', region_name='us-east-1')

    vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc_response['Vpc']['VpcId']
    print("Created VPC ID:", vpc_id)

    ec2.get_waiter('vpc_available').wait(VpcIds=[vpc_id])

    subnet_response = ec2.create_subnet(
        CidrBlock='10.0.1.0/24',
        VpcId=vpc_id
    )
    subnet_id = subnet_response['Subnet']['SubnetId']
    print("Created Subnet ID:", subnet_id)

    ec2.create_tags(
        Resources=[subnet_id],
        Tags=[{'Key': 'Name', 'Value': 'MySubnet'}]
    )
    print("Subnet created and tagged successfully!")


# ======================================================
# MAIN EXECUTION
# ======================================================
if __name__ == "__main__":
    # Uncomment the functions you want to run

    # create_lambda_function()
    # create_vpc_with_nat()
    # create_route_table()
    # create_sns_topic()
    # create_sqs_queue()
    # manage_ssm_parameter()
    # create_subnet()
    pass
