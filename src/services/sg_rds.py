import boto3
from dotenv import load_dotenv
import os
from src.common.excel import export_to_excel
from progress.bar import FillingSquaresBar


load_dotenv()

region = os.getenv('AWS_REGION')

ec2 = boto3.client('ec2', region_name=region)
rds = boto3.client('rds', region_name=region)

bar1 = FillingSquaresBar('RDS - Security groups')

sg_ids = []
sg_names = []

# to excel
groups_id = []
rules_id = []
types = []
ip_protocol = []
from_port = []
to_port = []
ipranges = []
ipv6_cidr = []
ipv4_cidr = []
source_sg = []


def list_securitygroups(response):
    for db in response["DBInstances"]:
        if len(db['VpcSecurityGroups']) > 0:
            for sg in db['VpcSecurityGroups']:
                sg_id = sg['VpcSecurityGroupId']
                if sg_id not in sg_ids:
                    sg_ids.append(sg_id)


def describe_rules():
    for group_id in sg_ids:
        bar1.next()
        response = ec2.describe_security_group_rules(Filters=[{
            'Name': 'group-id',
            'Values': [group_id]
        }])
        for rule in response['SecurityGroupRules']:
            try:
                source_sg.append(rule['ReferencedGroupInfo']['GroupId'])
            except:
                source_sg.append('-')
            try:
                ipv4_cidr.append(rule['CidrIpv4'])
            except:
                ipv4_cidr.append('-')
            try:
                ipv6_cidr.append(rule['CidrIpv6'])
            except:
                ipv6_cidr.append('-')

            if rule['IsEgress'] == False:
                t = "Inbound"
            else:
                t = "Outbound"
            if rule['IpProtocol'] == "-1":
                ip = "all traffic"
            else:
                ip = rule['IpProtocol']
            if rule['FromPort'] == -1:
                fp = "all"
                tp = "all"
            else:
                fp = rule['FromPort']
                tp = rule['ToPort']
            groups_id.append(group_id)
            rules_id.append(rule['SecurityGroupRuleId'])
            types.append(t)
            ip_protocol.append(ip)
            from_port.append(fp)
            to_port.append(tp)


def run():
    response = rds.describe_db_instances()
    list_securitygroups(response)
    bar1.max = len(sg_ids) + 1
    bar1.next()
    describe_rules()
    bar1.finish()

    sg_dict = {
        "Security group id": groups_id,
        "Securiy group rule id": rules_id,
        "Tipo": types,
        "Protocolo": ip_protocol,
        "From Port": from_port,
        "To Port": to_port,
        "Ipv4 range": ipv4_cidr,
        "Ipv6 range": ipv6_cidr,
        "SG origem": source_sg
    }
    export_to_excel(sg_dict, 'sg_rds')
