# -*- coding: utf-8 -*-
import boto3
from dotenv import load_dotenv
import os
from src.common.excel import export_to_excel
from progress.bar import FillingSquaresBar

load_dotenv()

region = os.getenv('AWS_REGION')

ec2_instanceid = []
ec2_instancestate = []
ec2_instancetype = []
ec2_instance_az = []
ec2_privatednsname = []
ec2_privateip = []
ec2_publicdnsname = []
ec2_monitoring = []
ec2_sg_id = []
ec2_keyname = []
ec2_ownerid = []
ec2_volumeid = []
ec2_rootdevice = []
ec2_roottype = []
ec2_ebsoptimized = []
ec2_vpc = []
ec2_subnet = []
ec2_platform = []
ec2_virtualization = []
ec2_kernelid = []
ec2_ramdiskid = []
ec2_reservationid = []
ec2_hibernation = []
ec2_launchindex = []
ec2_launchtime = []
ec2_publicdnsname = []
ec2_network = []
ec2_publicip = []
ec2_elasticip = []
ec2_sg_name = []
ec2_imageid = []
ec2_architecture = []
ec2_name = []


def run():
    ec2 = boto3.client('ec2', region_name=region)

    response = ec2.describe_instances()

    bar1 = FillingSquaresBar('EC2 - Instances')
    bar1.max = len(response["Reservations"]) + 1

    for reservation in response["Reservations"]:
        bar1.next()
        for instance in reservation["Instances"]:
            if instance['State']['Name'] != "terminated":
                ec2_instancestate.append(instance['State']['Name'])
                ec2_reservationid.append(reservation['ReservationId'])
                ec2_instanceid.append(instance['InstanceId'])
                ec2_imageid.append(instance['ImageId'])
                ec2_instancetype.append(instance['InstanceType'])
                ec2_az = instance['Placement']['AvailabilityZone']
                ec2_instance_az.append(ec2_az)
                ec2_privatednsname.append(instance['PrivateDnsName'])
                try:
                    ec2_privateip.append(instance['PrivateIpAddress'])
                except:
                    ec2_privateip.append('-')
                ec2_monitoring.append(instance['Monitoring']['State'])
                ec2_architecture.append(instance['Architecture'])
                if len(instance['SecurityGroups']) > 0:
                    for sg in instance['SecurityGroups']:
                        prov_list = []
                        prov_list1 = []
                        sg_id = instance['SecurityGroups'][0]['GroupId']
                        sg_name = instance['SecurityGroups'][0]['GroupName']
                        prov_list.append(sg_id)
                        prov_list1.append(sg_name)
                    convert = ",".join(map(str, prov_list))
                    convert1 = ",".join(map(str, prov_list1))
                    ec2_sg_id.append(convert)
                    ec2_sg_name.append(convert1)
                else:
                    ec2_sg_id.append("-")
                try:
                    ec2_keyname.append(instance['KeyName'])
                except:
                    ec2_keyname.append("-")
                try:
                    ownerid = instance['NetworkInterfaces'][0]['OwnerId']
                    ec2_ownerid.append(ownerid)
                except:
                    ec2_ownerid.append('-')
                try:
                    volumeid = instance['BlockDeviceMappings'][0]['Ebs']['VolumeId']
                    ec2_volumeid.append(volumeid)
                except:
                    ec2_volumeid.append('-')
                ec2_rootdevice.append(instance['RootDeviceName'])
                ec2_roottype.append(instance['RootDeviceType'])
                ec2_ebsoptimized.append(instance['EbsOptimized'])
                try:
                    ec2_vpc.append(instance['VpcId'])
                    ec2_subnet.append(instance['SubnetId'])
                except:
                    ec2_vpc.append('-')
                    ec2_subnet.append('-')
                ec2_platform.append(instance['PlatformDetails'])
                ec2_virtualization.append(instance['VirtualizationType'])
                ec2_hibernation.append(
                    instance['HibernationOptions']['Configured'])
                ec2_launchindex.append(instance['AmiLaunchIndex'])
                launchtime = instance['LaunchTime']
                ec2_launchtime.append(launchtime)
                ec2_publicdnsname.append(instance['PublicDnsName'])
                try:
                    ec2_network.append(
                        instance['NetworkInterfaces'][0]['NetworkInterfaceId'])
                except:
                    ec2_network.append('-')
                try:
                    ec2_kernelid.append(instance['KernelId'])
                except:
                    ec2_kernelid.append("-")
                try:
                    ec2_ramdiskid.append(instance['RamdiskId'])
                except:
                    ec2_ramdiskid.append("-")

                try:
                    publicipv4 = instance['PublicIpAddress']
                    ec2_publicip.append(publicipv4)
                except:
                    ec2_publicip.append('-')
                if 'Tags' in instance and len(instance['Tags']) > 0:
                    tag_name = None

                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            ec2_name.append(tag['Value'])
                            tag_name = True
                    if tag_name == True:
                        tag_name = None
                    else:
                        ec2_name.append("-")
                else:
                    ec2_name.append("-")

    bar1.next()
    bar1.finish()
    bar2 = FillingSquaresBar('EC2 - Network')
    bar2.max = len(ec2_network) + 1

    for eni in ec2_network:
        bar2.next()
        try:
            response = ec2.describe_network_interfaces(
                NetworkInterfaceIds=[eni])
            elasticip = response['NetworkInterfaces'][0]['Association']['PublicIp']
            ec2_elasticip.append(elasticip)
        except:
            ec2_elasticip.append('-')

    bar2.next()
    bar2.finish()

    ec2_dict = {
        "Nome da instância": ec2_name,
        "ID de instância": ec2_instanceid,
        "Estado da instância": ec2_instancestate,
        "Tipo de instância": ec2_instancetype,
        "Zona de disponibilidade": ec2_instance_az,
        "DNS IPv4 público": ec2_publicdnsname,
        "Endereço IPv4 Público": ec2_publicip,
        "IP elástico": ec2_elasticip,
        "Nome de DNS privada": ec2_privatednsname,
        "Endereço IP privado": ec2_privateip,
        "Monitoramento": ec2_monitoring,
        "Nome do grupo de segurança": ec2_sg_name,
        "Ids de grupo de segurança": ec2_sg_id,
        "Nome da chave": ec2_keyname,
        "ID do proprietário": ec2_ownerid,
        "ID de volume": ec2_volumeid,
        "Nome de dispositivo raiz": ec2_rootdevice,
        "Tipo de dispositivo raiz": ec2_roottype,
        "Otimizadas para EBS": ec2_ebsoptimized,
        "ID da imagem": ec2_imageid,
        "ID de kernel": ec2_kernelid,
        "ID do disco RAM": ec2_ramdiskid,
        "Índice de execução de AMI": ec2_launchindex,
        "Data de lançamento": ec2_launchtime,
        "ID de reserva": ec2_reservationid,
        "ID da VPC": ec2_vpc,
        "IDs da sub-rede": ec2_subnet,
        "Arquitetura": ec2_architecture,
        "Tipo de virtualização": ec2_virtualization,
        "Plataforma": ec2_platform,
        "Hibernação": ec2_hibernation
    }

    export_to_excel(ec2_dict, 'ec2')
