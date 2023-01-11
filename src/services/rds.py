import boto3
from dotenv import load_dotenv
import os
from src.common.excel import export_to_excel
from progress.bar import FillingSquaresBar

load_dotenv()

region = os.getenv('AWS_REGION')


def run():
    rds = boto3.client('rds', region_name=region)

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

    bar2 = FillingSquaresBar('RDS - Instances')

    def list_instances():
        try:
            response = rds.describe_db_instances()
            bar2.max = len(response['DBInstances']) + 1

            for db in response['DBInstances']:
                bar2.next()

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

    list_instances()

    bar2.next()
    bar2.finish()

    rds_dict = {
        "Identificador de banco de dados": db_identifier,
        "Mecanismo": db_engine,
        "Região e AZ": db_az,
        "Tamanho": db_class,
        "Status": db_status,
        "Storagetype": db_storagetype,
        "Storage": db_storage,
        "Endpoint": db_endpoint,
        "Publico": db_public,
        "Master": db_master

    }

    export_to_excel(rds_dict, 'rds')
