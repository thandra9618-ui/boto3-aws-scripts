import boto3
from botocore.exceptions import ClientError
from typing import List, Dict, Any

def list_iam_groups() -> List[Dict[str, Any]]:
    """
    List all IAM groups in the AWS account.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing IAM group details
    """
    client: boto3.client = boto3.client('iam')
    groups: List[Dict[str, Any]] = []

    try:
        paginator = client.get_paginator('list_groups')
        for page in paginator.paginate():
            for group in page.get('Groups', []):
                groups.append({
                    "GroupName": group.get("GroupName", ""),
                    "GroupId": group.get("GroupId", ""),
                    "CreateDate": group.get("CreateDate", None)
                })
    except ClientError as e:
        print(f"AWS IAM Error: {e}")

    return groups


if __name__ == "__main__":
    iam_groups: List[Dict[str, Any]] = list_iam_groups()
    if iam_groups:
        print("IAM Groups Found:")
        for group in iam_groups:
            print(group)
    else:
        print("No IAM groups found or access denied.")
