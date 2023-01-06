from progress.bar import FillingSquaresBar
import json
import os
from dotenv import load_dotenv
import boto3
from src.common.excel import export_to_excel

load_dotenv()

region = os.getenv('AWS_REGION')


s3 = boto3.client('s3')


bar = FillingSquaresBar('S3 - Buckets')


s3_name = []
s3_create = []
s3_versioning = []
s3_region = []
s3_access = []


def list_buckets(buckets):
    for bucket in buckets:
        s3_name.append(bucket['Name'])
        creationdate = bucket['CreationDate']

        s3_create.append(creationdate)

        check_bucket_info(bucket['Name'])
        check_bucket_access(bucket['Name'])

        bar.next()


def check_bucket_info(bucket):
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


def check_bucket_access(bucket):
    acs_url = 'http://acs.amazonaws.com/groups/global/'

    security_level = 0

    # 1. Verifica se existe regra na ACL para permitir acesso público, se tiver, é considerado público
    res_acl = s3.get_bucket_acl(Bucket=bucket)

    for grant in res_acl['Grants']:
        if grant['Grantee']['Type'] == 'Group':
            if grant['Grantee']['URI'] == acs_url + 'AllUsers' or grant['Grantee']['URI'] == acs_url + 'AuthenticatedUsers':
                if grant['Permission'] == 'READ' or grant['Permission'] == 'READ_ACP':
                    security_level = 3

    # 2. Verifica se existe política 'Allow' com  Principal '*' para esse bucket, se tiver, é considerado público
    try:
        res_policy = s3.get_bucket_policy(Bucket=bucket)

        # print('Possui Policy')
        policy = json.loads(res_policy['Policy'])
        if policy['Statement'] is not None:
            for statement in policy['Statement']:
                if statement['Effect'] == 'Allow' and statement['Principal'] == '*' and statement['Resource'] == 'arn:aws:s3:::'+bucket+'/*':
                    security_level = 3
    except Exception as e:
        pass
        # print(e)
        # print('Não possui Policy')

        # 3. Verifica se possui Public Access Block
    try:
        res_public_access_block = s3.get_public_access_block(Bucket=bucket)

        pab_config = res_public_access_block['PublicAccessBlockConfiguration']
        # print('Possui Public Access Block')

        # Se possui, é preciso verificar se todos os bloqueios estão ativos

        if pab_config['BlockPublicAcls'] and pab_config['BlockPublicPolicy'] and pab_config['IgnorePublicAcls'] and pab_config['RestrictPublicBuckets']:
            # print(' Bloqueio Total')
            # Se estão, e o bucket está público segundo as outras regras, passa para 'Only authorized users of this account'

            if security_level == 3:
                security_level = 2
        else:
            # Se não estão, e o bucket está 'Bucket and objects not public', passa para 'Objects can be public'

            # print(' Bloqueio Parcial')
            if security_level == 0:
                security_level = 1

    except:
        # Se não possui Access Block, e o bucket está 'Bucket and objects not public', passa para 'Objects can be public'
        # print('Não possui Public Access Block')
        if security_level == 0:
            security_level = 1

    result = ''

    if security_level == 0:
        result = 'Bucket and objects not public'
    elif security_level == 1:
        result = 'Objects can be public'
    elif security_level == 2:
        result = 'Only authorized users of this account'
    elif security_level == 3:
        result = 'Public'

    s3_access.append(result)


def run():
    response = s3.list_buckets(region=region)

    bar.max = len(response['Buckets']) + 1

    list_buckets(response['Buckets'])
    s3_dict = {
        "Nome do Bucket": s3_name,
        "Data de Criação": s3_create,
        "Região": s3_region,
        "Versionamento": s3_versioning,
        "Acesso": s3_access
    }

    export_to_excel(s3_dict, 's3')

    bar.next()
    bar.finish()
