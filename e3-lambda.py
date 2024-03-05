import json
import boto3
from datetime import datetime, timezone

# Select Region
region = 'us-east-1'

# Initialize the clients
ec2 = boto3.client('ec2')
dynamodb = boto3.resource('dynamodb')

# Define the filter to find instances with a specific tag name and value (from Sloane)
filters = [{
    'Name': 'tag:Name',
    'Values': ['grant-lambda']
}]

# Reference your DynamoDB Table
table = dynamodb.Table('grant-dob-ec2-table')

def lambda_handler(event, context):
    # Describe all instances
    response = ec2.describe_instances(Filters=filters)

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Assuming you want to check instances in a running state
            if instance['State']['Name'] == 'running':
                launch_time = instance['LaunchTime']
                instance_id = instance['InstanceId']
                current_time = datetime.now(timezone.utc)

                # Example condition: stop instance if running more than 24 hours
                if (current_time - launch_time).total_seconds() > 10:
                    # Stop the instance
                    ec2.stop_instances(InstanceIds=[instance_id])
                    print(f'Stopping instance {instance_id}')

                try:
                    table.put_item(Item={
                        'Index': instance_id,
                        'launchTime': launch_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'currentState': 'stopped' if (current_time - launch_time).total_seconds() > 10 else 'running',
                    })
                except Exception as e:
                    print(f"Error updating DynamoDB: {str(e)}")


    return {
        'statusCode': 200,
        'body': 'Execution completed'
    }
