import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

proj_name = os.getenv('PROJ_NAME')
region = os.getenv('AWS_REGION')
output_folder = os.getenv('OUPUT_FOLDER', 'output/')


def export_to_excel(excel_data: dict, service_name: str):

    df = pd.DataFrame(excel_data)

    # Converte datetime se houver
    for key in excel_data:
        if all(isinstance(item, datetime) for item in excel_data[key]):
            df[key] = df[key].apply(lambda a: pd.to_datetime(a).date())

    df.to_excel(
        f'{output_folder}{service_name}-{proj_name}-{region}.xlsx', index=False)


def join_files():
    # Pega todos os arquivos dentro da pasta de output que possuem o nome do projeto contido no nome do arquivo.
    file_list = [file for file in os.listdir(
        output_folder) if proj_name in file]

    writer = pd.ExcelWriter(output_folder + proj_name + '.xlsx')

    for file in file_list:
        service_name = file.split('-').pop(0)
        excel_file = pd.read_excel(output_folder + file)
        excel_file.to_excel(writer, sheet_name=service_name)

    writer.save()
