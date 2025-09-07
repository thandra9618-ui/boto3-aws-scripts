import boto3

# 1. Lambda client
lambda_client = boto3.client('lambda', region_name='us-east-1')  # change region

# 2. Read zipped Lambda code
with open('lambda_function.zip', 'rb') as f:
    zipped_code = f.read()

# 3. IAM Role ARN with Lambda execution permission
role_arn = 'arn:aws:iam::<ACCOUNT_ID>:role/<LAMBDA_EXECUTION_ROLE>'  # replace with your role ARN

# 4. Create Lambda Function
response = lambda_client.create_function(
    FunctionName='MyLambdaFunction',
    Runtime='python3.9',
    Role=role_arn,
    Handler='lambda_function.lambda_handler',  # filename.function_name
    Code={'ZipFile': zipped_code},
    Description='My first Lambda created with boto3',
    Timeout=10,
    MemorySize=128,
)

print("Created Lambda Function Name:", response['FunctionName'])
print("Lambda ARN:", response['FunctionArn'])
