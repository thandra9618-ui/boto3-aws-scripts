import boto3
from botocore.exceptions import ClientError
from typing import List, Dict, Any


def list_ec2_instances(region_name: str = "us-east-1") -> List[Dict[str, Any]]:
    """
    List all EC2 instances in the given AWS region.

    Args:
        region_name (str): AWS region to query (default: us-east-1)

    Returns:
        List[Dict[str, Any]]: A list of dictionaries with instance details
    """
    ec2 = boto3.client("ec2", region_name=region_name)
    instances: List[Dict[str, Any]] = []

    try:
        response = ec2.describe_instances()
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instances.append({
                    "InstanceId": instance.get("InstanceId", ""),
                    "State": instance.get("State", {}).get("Name", ""),
                    "InstanceType": instance.get("InstanceType", ""),
                    "PrivateIP": instance.get("PrivateIpAddress", "N/A"),
                    "PublicIP": instance.get("PublicIpAddress", "N/A")
                })
    except ClientError as e:
        print(f"AWS Error: {e}")

    return instances


if __name__ == "__main__":
    ec2_list: List[Dict[str, Any]] = list_ec2_instances()
    if ec2_list:
        print("EC2 Instances Found:")
        for inst in ec2_list:
            print(inst)
    else:
        print("No EC2 instances found or access denied.")
