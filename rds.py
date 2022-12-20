import boto3
import pandas as pd
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

region = os.getenv('AWS_REGION')
proj_name = os.getenv('PROJ_NAME')

rds = boto3.client('rds',)

db_identifier = []
db_class = []
db_engine = []
db_status = []
db_master = []
db_endpoint = []
db_az = []
db_public = []
db_storage = []
db_storagetype = []

def list_instances():
    try:
        response = rds.describe_db_instances()
        for db in response['DBInstances']:
            db_identifier.append(db['DBInstanceIdentifier'])
            db_class.append(db['DBInstanceClass'])
            db_engine.append(db['Engine'])
            db_status.append(db['DBInstanceStatus'])
            db_master.append(db['MasterUsername'])
            db_endpoint.append(db['Endpoint']['Address'])
            db_storage.append(db['AllocatedStorage'])
            db_storagetype.append(db['StorageType'])
            db_az.append(db['AvailabilityZone'])
            db_public.append(db['PubliclyAccessible'])
            

    except:
        print("can't any find databases")

def convert_excel():
    rds_dict = {
        "Identificador de banco de dados":db_identifier,
        "Mecanismo":db_engine,
        "Região e AZ":db_az,
        "Tamanho":db_class,
        "Status":db_status,
        "Storagetype":db_storagetype,
        "Storage":db_storage,
        "Endpoint": db_endpoint,
        "Publico":db_public,
        "Master":db_master

    }

    rds_df = pd.DataFrame(rds_dict)
    rds_df.to_excel(f'rds-{proj_name}-{region}.xlsx',index=False)



list_instances()
convert_excel()