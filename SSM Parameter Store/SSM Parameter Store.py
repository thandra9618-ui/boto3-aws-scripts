import boto3

# 1. Create SSM client
ssm = boto3.client('ssm', region_name='us-east-1')  # Change region if needed

# 2. Create a parameter
parameter_name = "/MyApp/Password"
parameter_value = "SuperSecret123"

try:
    ssm.put_parameter(
        Name=parameter_name,
        Value=parameter_value,
        Type='SecureString',   # Can also be 'String' or 'StringList'
        Overwrite=True         # Overwrite if already exists
    )
    print(f"Parameter '{parameter_name}' created successfully!")

except Exception as e:
    print("Error creating parameter:", e)

# 3. Retrieve the parameter
try:
    response = ssm.get_parameter(
        Name=parameter_name,
        WithDecryption=True   # Decrypt if SecureString
    )
    value = response['Parameter']['Value']
    print(f"Retrieved Parameter Value: {value}")

except Exception as e:
    print("Error retrieving parameter:", e)
