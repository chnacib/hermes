import boto3
import pandas as pd
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()


region = os.getenv('AWS_REGION')
proj_name = os.getenv('PROJ_NAME')

s3 = boto3.client('s3')


response = s3.list_buckets()

s3_name = []
s3_create = []
s3_versioning = []
s3_region = []



def list_buckets():
    for bucket in response['Buckets']:
        s3_name.append(bucket['Name'])
        creationdate = bucket['CreationDate']
        s3_create.append(s3_create)


def check_buckets():
    for bucket in s3_name:
        response = s3.get_bucket_versioning(Bucket=bucket)
        location = s3.get_bucket_location(Bucket=bucket)
        try:
            s3_versioning.append(response['Status'])
        except:
            s3_versioning.append('Disabled')
        regions3 = location['LocationConstraint']
        if regions3 is None:
            s3_region.append(region)
        else:
            s3_region.append(regions3)

def check_access():
    for bucket in s3_name:
        try:
            response = s3.get_public_access_block(Bucket=bucket)
            print(response['PublicAccessBlockConfiguration']['BlockPublicAcls'])
            print(response['PublicAccessBlockConfiguration']['BlockPublicPolicy'])
            print(f"{bucket} can be public")
        except:
            print(f"{bucket} Public")

def check_policy():
    for bucket in s3_name:
        response = s3.get_bucket_acl(Bucket=bucket)
        print(response)
           

list_buckets()
check_buckets()
#check_access()
check_policy()