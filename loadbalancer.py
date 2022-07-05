from yaml import load
import boto3
import pandas as pd
from datetime import date

elb = boto3.client('elbv2',region_name="sa-east-1")

response = elb.describe_load_balancers()

elb_name = []
elb_dnsname = []
elb_state = []
elb_vpc = []
elb_az = []
elb_type = []
elb_createtime = []
elb_scheme = []

for loadbalancer in response['LoadBalancers']:
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
    
    convert = ",".join(map(str,provlist))        
    elb_az.append(convert)


elb_dict = {
    "Nome":elb_name,
    "Nome do DNS":elb_dnsname,
    "Estado":elb_state,
    "AZ":elb_az,
    "Tipo":elb_type,
    "Criado em":elb_createtime,
    "Scheme":elb_scheme
}

elb_df = pd.DataFrame(elb_dict)
elb_df['Criado em'] = elb_df['Criado em'].apply(lambda a: pd.to_datetime(a).date()) 

elb_df.to_excel('elb.xlsx',index=False)