import boto3
import pandas as pd
from datetime import date




iam = boto3.client('iam')
iam_r = boto3.resource('iam')



iam_users = []
users = iam.list_users()
for x in users['Users']:
    iam_users.append(x['UserName'])

iam_users_group = []
prov_group = []

for key in users['Users']:
    list_of_groups =  iam.list_groups_for_user(UserName=key['UserName'])
    validate = list_of_groups['Groups']
    if len(list_of_groups['Groups']) > 0:
        for key in list_of_groups['Groups']:
            key = key['GroupName']
            prov_group.append(key)
        
        convert = ",".join(map(str,prov_group))       
        iam_users_group.append(convert)
            
    else:
        iam_users_group.append('-')

iam_console_login = []

for x in users['Users']:
    try:
        console_login = x['PasswordLastUsed']
        console_login = console_login.date()
        console_login = str(console_login)
        iam_console_login.append(console_login)
    except:
        iam_console_login.append("-")
iam_key_age = []

for x in iam_users:
    username = x
    response = iam.list_access_keys(UserName=username)
    try:
        accesskeydate = response ['AccessKeyMetadata'][0]['CreateDate'].date()
        currentdate = date.today()
        active_days = currentdate - accesskeydate
        iam_key_age.append(f"{active_days.days} days")
    except:
        iam_key_age.append("-")

iam_mfa_device = []

for x in iam_users:
    list_devices = iam.list_mfa_devices(UserName=x)
    validate = list_devices['MFADevices']
    if len(list_devices['MFADevices']) > 0:
        for x in list_devices['MFADevices']:
            iam_mfa_device.append("Enabled")
    else:
        iam_mfa_device.append('None')

iam_access_key_id = []

for x in users['Users']:
    prov_key = []
    response = iam.list_access_keys(UserName=x['UserName'])
    validate = response['AccessKeyMetadata']
    if len(response['AccessKeyMetadata']) > 0:
        for x in response['AccessKeyMetadata']:
            if x['Status'] == "Active":
                key = x['AccessKeyId']
                prov_key.append(key)                    
            else:
                prov_key.append('Inactive') 
        convert = ",".join(map(str,prov_key))        
        iam_access_key_id.append(convert)
    else:
        iam_access_key_id.append('None')

iam_access_key_last_used = []


def get_last_use(key_id):
    
    try:
        response = iam_r.meta.client.get_access_key_last_used(AccessKeyId=key_id)
        last_used_date = response['AccessKeyLastUsed'].get('LastUsedDate', None)
        last_used_date = last_used_date.date()
        last_used_date = str(last_used_date)
        iam_access_key_last_used.append(last_used_date)
        
    except:
        iam_access_key_last_used.append('-')
    

for key_id in iam_access_key_id:
    get_last_use(key_id)

iam_user_create_date = []
iam_user_arn = []

for x in iam_users:
    response = iam.get_user(UserName=x)
    create_date = response['User'].get('CreateDate')
    create_date = create_date.date()
    create_date = str(create_date)
    iam_user_create_date.append(create_date)
    user_arn = response['User'].get('Arn')
    iam_user_arn.append(user_arn)

iam_console_access = []

for x in iam_users:
    try:
        response = iam.get_login_profile(UserName=x)
        iam_console_access.append('Enabled')
    except:
        iam_console_access.append('Disabled')

#print(len(iam_users))
##print(len(iam_users_group))
#print(iam_users_group)
##print(len(iam_mfa_device))
#print(len(iam_key_age))
#print(len(iam_console_login))
#print(len(iam_access_key_id))
#print(iam_access_key_id)
#print(len(iam_access_key_last_used))
#print(len(iam_user_arn))
#print(len(iam_user_create_date))
#print(len(iam_console_access))

iam_dict = {"Nome do usuário": iam_users,
            "Grupos": iam_users_group,
            "MFA": iam_mfa_device,
            "Idade da senha": iam_key_age,
            "Último login no console": iam_console_login,
            "ID da chave de acesso": iam_access_key_id,
            "Última chave de acesso utilizada": iam_access_key_last_used,
            "ARN": iam_user_arn,
            "Data de criação": iam_user_create_date,
            "Acesso ao console": iam_console_access}





iam_df = pd.DataFrame(iam_dict)




iam_df.to_excel('iam_teste.xlsx',index=False)
