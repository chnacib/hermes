import boto3
import pandas as pd
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()


region = os.getenv('AWS_REGION')
proj_name = os.getenv('PROJ_NAME')

ec2 = boto3.client('ec2', region_name=region)

response = ec2.describe_volumes()

ebs_name = []
ebs_volumeid = []
ebs_volumesize = []
ebs_volumetype = []
ebs_iops = []
ebs_thoughput = []
ebs_snapshot = []
ebs_creatime = []
ebs_az = []
ebs_state = []
ebs_instanceid = []
ebs_encrypt = []
ebs_kms = []
ebs_multiattach = []
ebs_volumestatus = []

for volume in response['Volumes']:
    ebs_volumeid.append(volume['VolumeId'])
    ebs_volumesize.append(volume['Size'])
    ebs_volumetype.append(volume['VolumeType'])
    try:
        ebs_iops.append(volume['Iops'])
    except:
        ebs_iops.append("-")
    try:
        ebs_thoughput.append(volume['Throughput'])
    except:
        ebs_thoughput.append("-")
    ebs_snapshot.append(volume['SnapshotId'])
    createtime = volume['CreateTime']
    ebs_creatime.append(createtime)
    ebs_az.append(volume['AvailabilityZone'])
    ebs_state.append(volume['State'])
    try:
        ebs_instanceid.append(volume['Attachments'][0]['InstanceId'])
    except:
        ebs_instanceid.append("-")
    ebs_encrypt.append(volume['Encrypted'])
    try:
        ebs_kms.append(volume['KmsKeyId'])    
    except:
        ebs_kms.append("-")    
    ebs_multiattach.append(volume['MultiAttachEnabled'])
    try:
        checktag = volume['Tags'][0]['Key']
    except:
        checktag = "-"
    if checktag == "Name":
        ebs_name.append(volume['Tags'][0]['Value'])
    else:
        ebs_name.append("-")
    

for id in ebs_volumeid:
    response = ec2.describe_volume_status(VolumeIds=[id])
    ebs_volumestatus.append(response['VolumeStatuses'][0]['VolumeStatus']['Status'])



    
ebs_dict = {"Name":ebs_name,
            "Volume ID":ebs_volumeid,
            "Size":ebs_volumesize,
            "Volume Type":ebs_volumetype,
            "IOPS":ebs_iops,
            "Throughput (MB/s)":ebs_thoughput,
            "Snapshot":ebs_snapshot,
            "Created":ebs_creatime,
            "Availability Zone":ebs_az,
            "State":ebs_state,
            "Instâncias anexadas":ebs_instanceid,
            "Status do volume":ebs_volumestatus,
            "Criptografia":ebs_encrypt,
            "ID da chave KMS":ebs_kms,
            "Vinculação múltipla habilitada":ebs_multiattach}

ebs_df = pd.DataFrame(ebs_dict)
ebs_df['Created'] = ebs_df['Created'].apply(lambda a: pd.to_datetime(a).date()) 

ebs_df.to_excel(f'ebs-{proj_name}-{region}.xlsx',index=False)
