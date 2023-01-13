import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

proj_name = os.getenv('PROJ_NAME', 'None')
region = os.getenv('AWS_REGION', 'None')
output_folder = os.getenv('OUPUT_FOLDER', 'output/')
ext = '.xlsx'


def export_to_excel(excel_data: dict, service_name: str):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    df = pd.DataFrame(excel_data)

    # Converte datetime se houver
    for key in excel_data:
        if all(isinstance(item, datetime) for item in excel_data[key]):
            df[key] = df[key].apply(lambda a: pd.to_datetime(a).date())

    df.to_excel(
        f'{output_folder}{service_name}-{proj_name}-{region}{ext}', index=False)


def join_files():
    joined_file = output_folder + proj_name + '-' + region + ext
    # Cria pasta de output
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Remove o arquivo gerado anteriormente, se existe
    if os.path.exists(joined_file):
        os.remove(joined_file)

    # Pega todos os arquivos dentro da pasta de output que possuem o nome do projeto contido no nome do arquivo.
    file_list = [file for file in os.listdir(
        output_folder) if proj_name in file]

    writer = pd.ExcelWriter(joined_file)

    for file in file_list:
        # Ignora o arquivo gerado anteriormente
        if file == joined_file:
            continue

        service_name = file.split('-').pop(0)
        print(output_folder + file)
        excel_file = pd.read_excel(output_folder + file)
        excel_file.to_excel(writer, sheet_name=service_name)

    writer.save()

    print('')
    print('Output file: ' + os.path.abspath(output_folder +
          proj_name + '-' + region + ext))
    print('')
