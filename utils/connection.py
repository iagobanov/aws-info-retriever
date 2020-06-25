import boto3

def connect_aws_service(region, service):
    client = boto3.client(service, region_name=region)
    return client