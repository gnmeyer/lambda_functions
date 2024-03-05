import json
import boto3

def lambda_handler(event, context):

    # Select Region
    region = 'us-east-1'

    # Create an EC2 client
    ec2 = boto3.client('ec2', region_name=region)

    # Define the filter to find instances with a specific tag name and value (from Sloane)
    filters = [{
        'Name': 'tag:Name',
        'Values': ['test-grant-lambda']
    }]

    # Example: Describe all EC2 instances
    response = ec2.describe_instances(Filters=filters)

    # Iterate over reservations (a reservation contains one or more instances)
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Print instance ID
            print("Instance ID:", instance['InstanceId'])
            # Print instance type
            print("Instance Type:", instance['InstanceType'])
            # Print instance state
            print("Instance State:", instance['State']['Name'])
            # Print tags (if any)
            if 'Tags' in instance:
                print("Tags:")
                for tag in instance['Tags']:
                    print("\tKey:", tag['Key'], "\tValue:", tag['Value'])
            print("---------------------------------------------")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
