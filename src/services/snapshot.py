import boto3
from dotenv import load_dotenv
import os
from src.common.excel import export_to_excel
from progress.bar import FillingSquaresBar


load_dotenv()

region = os.getenv('AWS_REGION')


def run():
    ec2 = boto3.client('ec2', region_name=region)

    bar1 = FillingSquaresBar('Snapshots')

    response = ec2.describe_snapshots(OwnerIds=['self'])
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

    bar1.max = len(response['Snapshots']) + 1

    for snapshot in response['Snapshots']:
        bar1.next()
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
            checktag = snapshot['Tags'][0]['Key']
        except:
            checktag = "-"
        if checktag == "Name":
            snapshot_name.append(snapshot['Tags'][0]['Value'])
        else:
            snapshot_name.append("-")

    bar1.next()
    bar1.finish()

    snapshot_dict = {
        "Name": snapshot_name,
        "ID do snapshot": snapshot_id,
        "Tamanho": snapshot_size,
        "Descrição": snapshot_description,
        "Nível de armazenamento": snapshot_tier,
        "Status do snapshot": snapshot_state,
        "Iniciado": snapshot_starttime,
        "Andamento": snapshot_progress,
        "Tempo de expiração da restauração": snapshot_restore,
        "ID do volume": snapshot_volumeid,
        "Proprietário": snapshot_ownerid,
        "Alias do proprietário": snapshot_owneralias,
        "Criptografia": snapshot_encrypted,
        "ID da chave do KMS": snapshot_kms,
        "ARN de Outposts": snapshot_outpostarn
    }

    export_to_excel(snapshot_dict, 'snapshot')
