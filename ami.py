from inspect import Attribute
from tracemalloc import Snapshot
import boto3
import pandas as pd
from datetime import date


ec2 = boto3.client('ec2')

client = boto3.client('ec2', region_name='us-east-1')

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

response = client.describe_images(Owners=['self'])
for ami in response['Images']:
    try:
        ami_name.append(ami['Name'])
    except:
        ami_name.append("-")
    ami_id.append(ami['ImageId'])
    ami_origem.append(ami['ImageLocation'])
    if ami['Public'] == "False":
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
    ami_description.append(ami['Description'])
    device_name = ami['BlockDeviceMappings'][0]['DeviceName']
    snapshot = ami['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
    volumesize = ami['BlockDeviceMappings'][0]['Ebs']['VolumeSize']
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
print(len(ami_visibilidade))
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



