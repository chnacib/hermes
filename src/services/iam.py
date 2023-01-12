import boto3
from datetime import date
from src.common.excel import export_to_excel
from progress.bar import FillingSquaresBar

iam_users = []
iam_users_group = []
iam_console_login = []
iam_key_age = []
iam_mfa_device = []
iam_access_key_last_used = []
iam_user_create_date = []
iam_user_arn = []
iam_console_access = []
iam_access_key_id = []


def run():
    def get_last_use(key_id):
        try:
            response = iam_r.meta.client.get_access_key_last_used(
                AccessKeyId=key_id)
            last_used_date = response['AccessKeyLastUsed'].get(
                'LastUsedDate', None)
            last_used_date = last_used_date.date()
            last_used_date = str(last_used_date)
            iam_access_key_last_used.append(last_used_date)

        except Exception as e:
            iam_access_key_last_used.append('-')

    iam = boto3.client('iam')
    iam_r = boto3.resource('iam')

    users = iam.list_users()

    bar1 = FillingSquaresBar('IAM - Users')

    bar1.max = len(users['Users']) + 1

    for user in users['Users']:
        bar1.next()
        username = user['UserName']

        iam_users.append(username)

        list_of_groups = iam.list_groups_for_user(UserName=username)

        # 1. Grupos
        if len(list_of_groups['Groups']) > 0:
            for group_item in list_of_groups['Groups']:
                prov_group = []
                group_name = group_item['GroupName']
                prov_group.append(group_name)
            convert = ",".join(map(str, prov_group))
            iam_users_group.append(convert)
        else:
            iam_users_group.append('-')

        # 2. Senha
        try:
            console_login = user['PasswordLastUsed']
            console_login = console_login.date()
            console_login = str(console_login)
            iam_console_login.append(console_login)
        except:
            iam_console_login.append("-")

        # 3. Access Key
        response = iam.list_access_keys(UserName=username)

        try:
            if len(response['AccessKeyMetadata']) > 0:
                accesskeydate = response['AccessKeyMetadata'][0]['CreateDate'].date(
                )
                currentdate = date.today()
                active_days = currentdate - accesskeydate
                iam_key_age.append(f"{active_days.days} days")

                prov_key = []

                for x in response['AccessKeyMetadata']:
                    if x['Status'] == "Active":
                        key = x['AccessKeyId']
                        prov_key.append(key)
                    else:
                        prov_key.append('Inactive')
                convert = ",".join(map(str, prov_key))
                iam_access_key_id.append(convert)
            else:
                iam_key_age.append("-")
                iam_access_key_id.append('None')

        except:
            pass

        # 4. MFA
        list_devices = iam.list_mfa_devices(UserName=username)
        if len(list_devices['MFADevices']) > 0:
            for x in list_devices['MFADevices']:
                iam_mfa_device.append("Enabled")
        else:
            iam_mfa_device.append('None')

        # 6. Create Date
        response = iam.get_user(UserName=username)
        create_date = response['User'].get('CreateDate')
        create_date = create_date.date()
        create_date = str(create_date)
        iam_user_create_date.append(create_date)

        # 7. Arn
        user_arn = response['User'].get('Arn')
        iam_user_arn.append(user_arn)

        # 8. Console Access
        try:
            response = iam.get_login_profile(UserName=username)
            iam_console_access.append('Enabled')
        except:
            iam_console_access.append('Disabled')

    bar1.next()
    bar1.finish()

    bar2 = FillingSquaresBar('IAM - Access Keys')

    bar2.max = len(iam_access_key_id) + 1

    for key_id in iam_access_key_id:
        bar2.next()
        get_last_use(key_id)

    bar2.next()
    bar2.finish()


    iam_dict = {"Nome do usuário": iam_users,
                "Grupos": iam_users_group,
                "MFA": iam_mfa_device,
                "Idade da senha": iam_key_age,
                "Último login no console": iam_console_login,
                "ID da chave de acesso":  iam_access_key_id,
                "Última chave de acesso utilizada": iam_access_key_last_used,
                "ARN": iam_user_arn,
                "Data de criação": iam_user_create_date,
                "Acesso ao console": iam_console_access}

    # bar1.finish()

    export_to_excel(iam_dict, 'iam')
