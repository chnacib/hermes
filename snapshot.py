import boto3
import pandas as pd
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()


region = os.getenv('AWS_REGION')
proj_name = os.getenv('PROJ_NAME')
account_id = os.getenv('ACCOUNT_ID')

ec2 = boto3.client('ec2', region_name=region)

response = ec2.describe_snapshots(OwnerIds=[account_id])


snapshot_id = []
snapshot_size = []
snapshot_ownerid = []
snapshot_description = []
snapshot_tier = []
snapshot_state = []
snapshot_starttime = []
snapshot_encrypted = []
snapshot_progress = []
snapshot_volumeid = []
snapshot_owneralias = []
snapshot_outpostarn = []
snapshot_name = []
snapshot_restore = []
snapshot_kms = []


for snapshot in response['Snapshots']:
    snapshot_id.append(snapshot['SnapshotId'])
    snapshot_size.append(snapshot['VolumeSize'])
    snapshot_ownerid.append(snapshot['OwnerId'])
    snapshot_description.append(snapshot['Description'])
    snapshot_tier.append(snapshot['StorageTier'])
    snapshot_state.append(snapshot['State'])
    startime = snapshot['StartTime']
    snapshot_starttime.append(startime)
    snapshot_encrypted.append(snapshot['Encrypted'])
    snapshot_progress.append(snapshot['Progress'])
    snapshot_volumeid.append(snapshot['VolumeId'])
    try:
        snapshot_restore.append(snapshot['RestoreExpiryTime'])
    except:
        snapshot_restore.append('-')
    try:
        snapshot_owneralias.append(snapshot['OwnerAlias'])
    except:
        snapshot_owneralias.append('-')
    try:
        snapshot_outpostarn.append(snapshot['OutpostArn'])
    except:
        snapshot_outpostarn.append('-')
    try:
        snapshot_kms.append(snapshot['KmsKeyId'])
    except:
        snapshot_kms.append('-')
    try:
        checktag = instance['Tags'][0]['Key']
    except:
        checktag = "-"
    if checktag == "Name":
        snapshot_name.append(snapshot['Tags'][0]['Value'])
    else:
        snapshot_name.append("-")


snapshot_dict = {
    "Name":snapshot_name,
    "ID do snapshot":snapshot_id,
    "Tamanho":snapshot_size,
    "Descrição":snapshot_description,
    "Nível de armazenamento":snapshot_tier,
    "Status do snapshot":snapshot_state,
    "Iniciado":snapshot_starttime,
    "Andamento":snapshot_progress,
    "Tempo de expiração da restauração":snapshot_restore,
    "ID do volume":snapshot_volumeid,
    "Proprietário":snapshot_ownerid,
    "Alias do proprietário":snapshot_owneralias,
    "Criptografia":snapshot_encrypted,
    "ID da chave do KMS":snapshot_kms,
    "ARN de Outposts":snapshot_outpostarn
}

snapshot_df = pd.DataFrame(snapshot_dict)
snapshot_df['Iniciado'] = snapshot_df['Iniciado'].apply(lambda a: pd.to_datetime(a).date()) 

snapshot_df.to_excel(f'snapshot-{proj_name}-{region}.xlsx',index=False)



