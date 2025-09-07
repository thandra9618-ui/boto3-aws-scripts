import boto3

# 1. Create SQS client
sqs = boto3.client('sqs', region_name='us-east-1')  # change region if needed

# 2. Create a Queue
queue_name = 'MyQueue'
response = sqs.create_queue(
    QueueName=queue_name,
    Attributes={
        'DelaySeconds': '0',          # optional: delay messages
        'MessageRetentionPeriod': '86400'  # optional: 1 day
    }
)

queue_url = response['QueueUrl']
print("Created SQS Queue URL:", queue_url)

# 3. Send a message to the queue
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody='Hello from boto3 SQS!'
)

print("Message sent successfully!")

# 4. Receive a message from the queue
messages = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,
    WaitTimeSeconds=2
)

if 'Messages' in messages:
    for msg in messages['Messages']:
        print("Received message:", msg['Body'])

        # Delete the message after processing
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg['ReceiptHandle']
        )
        print("Message deleted from queue")
else:
    print("No messages in queue")
