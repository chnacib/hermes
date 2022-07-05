import boto3
import pandas as pd
from datetime import date


ec2 = boto3.client('ec2',region_name='sa-east-1')


ami_name = []
ami_id = []
ami_origem = []
ami_visibilidade = []
ami_owner = []
ami_state = []
ami_creation = []
ami_architecture = []
ami_platform = []
ami_root_device_name = []
ami_root_device_type = []
ami_block_device = []
ami_description = []
ami_imagetype = []
ami_kernelid = []
ami_ramdiskid = []
ami_product = []
ami_virtualization = []
ami_usageoperation = []
ami_volumesize = []

response = ec2.describe_images(Owners=['self'])
for ami in response['Images']:
    try:
        ami_name.append(ami['Name'])
    except:
        ami_name.append("-")
    ami_id.append(ami['ImageId'])
    ami_origem.append(ami['ImageLocation'])
    vis_validate = str(ami['Public'])
    if vis_validate == "False":
        ami_visibilidade.append('Private')
    else:
        ami_visibilidade.append('Public')
    ami_owner.append(ami['OwnerId'])
    ami_state.append(ami['State'])
    ami_creation.append(ami['CreationDate'])
    ami_architecture.append(ami['Architecture'])
    ami_platform.append(ami['PlatformDetails'])
    ami_root_device_name.append(ami['RootDeviceName'])
    ami_root_device_type.append(ami['RootDeviceType'])
    try:
        ami_description.append(ami['Description'])
    except:
        ami_description.append("-")

    device_name = ami['BlockDeviceMappings'][0]['DeviceName']
    snapshot = ami['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
    volumesize = ami['BlockDeviceMappings'][0]['Ebs']['VolumeSize']
    ami_volumesize.append(volumesize)
    volumetype = ami['BlockDeviceMappings'][0]['Ebs']['VolumeType']
    encrypted = ami['BlockDeviceMappings'][0]['Ebs']['Encrypted']
    blockdevice = f'{device_name}={snapshot}:{volumesize}:{encrypted}:{volumetype}'
    ami_block_device.append(blockdevice)
    ami_imagetype.append(ami['ImageType'])
    ami_virtualization.append(ami['VirtualizationType'])
    ami_usageoperation.append(ami['UsageOperation'])

for id in ami_id:
    response = ec2.describe_image_attribute(Attribute='kernel',ImageId=id)
    if len(response['KernelId']) > 0:
        try:
            ami_kernelid.append(response['KernelId'][0]['Value'])
        except:
            ami_kernelid.append('-')
    else:
        ami_kernelid.append('-')
    response = ec2.describe_image_attribute(Attribute='ramdisk',ImageId=id)
    if len(response['RamdiskId']) > 0:
        try:
            ami_ramdiskid.append(response['RamdiskId'][0]['Value'])
        except:
            ami_ramdiskid.append('-')
    else:
        ami_ramdiskid.append('-')
    response = ec2.describe_image_attribute(Attribute='productCodes',ImageId=id)
    if len(response['ProductCodes']) > 0:
        try:
            ami_product.append(response['ProductCodeId'][0]['Value'])
        except:
            ami_product.append('-')
    else:
        ami_product.append('-')
   
print(len(ami_name))
print(len(ami_id))
print(len(ami_origem))
print(ami_visibilidade)
print(len(ami_owner))
print(len(ami_state))
print(len(ami_creation))
print(len(ami_architecture))
print(len(ami_platform))
print(len(ami_root_device_name))
print(len(ami_root_device_type))
print(len(ami_description))
print(len(ami_block_device))
print(len(ami_imagetype))
print(len(ami_kernelid))
print(len(ami_ramdiskid))
print(len(ami_product))
print(len(ami_virtualization))
print(len(ami_usageoperation))
print(len(ami_volumesize))



ami_dict = {"Nome da AMI":ami_name,
"ID da AMI":ami_id,
"Origem":ami_origem,
"Proprietário":ami_owner,
"Visibilidade":ami_visibilidade,
"Status":ami_state,
"Data de criação":ami_creation,
"Código de produto":ami_product,
"Arquitetura":ami_architecture,
"Descrição":ami_description,
"Plataforma":ami_platform,
"Nome de dispositivo raiz":ami_root_device_name,
"Tipo de dispositivo raiz":ami_root_device_type,
"Dispositivo de blocos":ami_block_device,
"Tipo de Imagem":ami_imagetype,
"ID de kernel":ami_kernelid,
"ID do disco RAM":ami_ramdiskid,
"Tamanho da imagem":ami_volumesize,
"Virtualização":ami_virtualization,
"Operação de uso":ami_usageoperation}

ami_df = pd.DataFrame(ami_dict)




ami_df.to_excel('ami.xlsx',index=False)
