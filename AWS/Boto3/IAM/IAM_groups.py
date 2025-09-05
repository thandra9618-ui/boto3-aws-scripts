import boto3

def list_iam_groups():
    client = boto3.client('iam')
    paginator = client.get_paginator('list_groups')
    groups = []
    for page in paginator.paginate():
        groups.extend(page['Groups'])
    return groups