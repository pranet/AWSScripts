"""
Terminates all ec2 instances across all regions.
"""
import boto3


def get_regions():
    return ['ap-south-1', 'eu-west-3', 'eu-west-2', 'eu-west-1', 'ap-northeast-2', 'ap-northeast-1', 'sa-east-1',
            'ca-central-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'us-east-1', 'us-east-2', 'us-west-1',
            'us-west-2']


def get_ids(ec2):
    reservations = ec2.describe_instances()['Reservations']
    ids = []
    for reservation in reservations:
        for instance in reservation['Instances']:
            ids.append(instance['InstanceId'])
    return ids


def modify_permissions(ec2, ids):
    for id in ids:
        ec2.modify_instance_attribute(InstanceId=id, DisableApiTermination={
            'Value': False
        })


def terminate_instances(ec2, ids):
    response = ec2.terminate_instances(
        InstanceIds=ids
    )
    print(response)


AWS_ACCESS_KEY = ""
AWS_SECRET_ACCESS_KEY = ""

for region in get_regions():
    print ("Handling {}".format(region))
    ec2 = boto3.client('ec2', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       region_name=region)
    ids = get_ids(ec2)
    try:
        modify_permissions(ec2, ids) # might fail if instance is already terminated
    except Exception:
        pass
    terminate_instances(ec2, ids)
