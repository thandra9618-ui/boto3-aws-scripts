import boto3

# 1. Create SNS client
sns = boto3.client('sns', region_name='us-east-1')  # change region if needed

# 2. Create an SNS Topic
topic_response = sns.create_topic(Name='MySNSTopic')
topic_arn = topic_response['TopicArn']
print("Created SNS Topic ARN:", topic_arn)

# 3. Subscribe an email to the topic (replace with your email)
subscribe_response = sns.subscribe(
    TopicArn=topic_arn,
    Protocol='email',      # Options: 'email', 'sms', 'lambda', 'sqs', 'https'
    Endpoint='your-email@example.com'  
)
subscription_arn = subscribe_response['SubscriptionArn']
print("Subscription ARN (pending confirmation):", subscription_arn)

# 4. Publish a message to the topic
publish_response = sns.publish(
    TopicArn=topic_arn,
    Message='Hello from Python SNS!',
    Subject='Test Notification'
)
print("Message ID:", publish_response['MessageId'])
