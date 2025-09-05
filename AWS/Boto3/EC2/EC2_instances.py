import boto3

def list_ec2_instances(region_name='us-east-1'):
    ec2 = boto3.client('ec2', region_name=region_name)
    response = ec2.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance['InstanceId'])
    return instances

if __name__ == "__main__":
    print(list_ec2_instances())