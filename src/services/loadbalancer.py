import boto3
from dotenv import load_dotenv
import os
from src.common.excel import export_to_excel
from progress.bar import FillingSquaresBar

load_dotenv()

region = os.getenv('AWS_REGION')


def run():
    bar1 = FillingSquaresBar('LoadBalancer')

    elb = boto3.client('elbv2', region_name=region)

    response = elb.describe_load_balancers()

    elb_name = []
    elb_dnsname = []
    elb_state = []
    elb_vpc = []
    elb_az = []
    elb_type = []
    elb_createtime = []
    elb_scheme = []

    bar1.max = len(response['LoadBalancers']) + 1

    for loadbalancer in response['LoadBalancers']:
        bar1.next()
        provlist = []
        elb_name.append(loadbalancer['LoadBalancerName'])
        elb_dnsname.append(loadbalancer['DNSName'])
        elb_state.append(loadbalancer['State']['Code'])
        elb_vpc.append(loadbalancer['VpcId'])
        elb_type.append(loadbalancer['Type'])
        createtime = loadbalancer['CreatedTime']
        elb_createtime.append(createtime)
        elb_scheme.append(loadbalancer['Scheme'])
        for x in loadbalancer['AvailabilityZones']:
            zonename = x['ZoneName']
            provlist.append(zonename)

        convert = ",".join(map(str, provlist))
        elb_az.append(convert)

    bar1.next()
    bar1.finish()
    elb_dict = {
        "Nome": elb_name,
        "Nome do DNS": elb_dnsname,
        "Estado": elb_state,
        "AZ": elb_az,
        "Tipo": elb_type,
        "Criado em": elb_createtime,
        "Scheme": elb_scheme
    }

    export_to_excel(elb_dict, 'elb')
