import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

proj_name = os.getenv('PROJ_NAME')
region = os.getenv('AWS_REGION')


def export_to_excel(excel_data: dict, service_name: str):

    df = pd.DataFrame(excel_data)

    # Converte datetime se houver
    for key in excel_data:
        if all(isinstance(item, datetime) for item in excel_data[key]):
            df[key] = df[key].apply(lambda a: pd.to_datetime(a).date())

    df.to_excel(
        f'output/{service_name}-{proj_name}-{region}.xlsx', index=False)
