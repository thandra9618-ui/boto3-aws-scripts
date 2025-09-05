import boto3

def list_iam_users():
    iam = boto3.client('iam')
    response = iam.list_users()
    users = [user['UserName'] for user in response['Users']]
    return users

if __name__ == "__main__":
    print(list_iam_users())