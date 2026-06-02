import pandas as pd
import pydata_google_auth
import  requests

from google.cloud      import bigquery
from configs           import PROJECT_ID, SCOPES
from time              import sleep
from typing_extensions import Union

# Gera os links para o google maps
def gera_link_maps(lat_long):
    def convert_to_dms(decimal_degrees):
        degrees = int(abs(decimal_degrees))
        minutes = int((abs(decimal_degrees) - degrees) * 60)
        seconds = (abs(decimal_degrees) - degrees - minutes / 60) * 3600
        return degrees, minutes, seconds

    if pd.isna(lat_long) or not isinstance(lat_long, str) or ',' not in lat_long:
        return None
    try:
        lat, long = lat_long.split(", ")
        lat_deg, lat_min, lat_sec = convert_to_dms(float(lat))
        long_deg, long_min, long_sec = convert_to_dms(float(long))
        lat_dir = "S" if float(lat) < 0 else "N"
        long_dir = "W" if float(long) < 0 else "E"
        return f"https://www.google.com.br/maps/place/{lat_deg}%C2%B0{lat_min}'{lat_sec:.1f}%22{lat_dir}+{long_deg}%C2%B0{long_min}'{long_sec:.1f}%22{long_dir}"
    except ValueError:
        return None

# Autentica e gera os dataframes
    
# Function to fetch a table and create a DataFrame
def fetch_and_create_dataframe(client, project_id, dataset_id, table_id, output_name):
    query = f'SELECT * FROM `{project_id}.{dataset_id}.{table_id}`'
    df = client.query(query).to_dataframe()
    globals()[output_name] = df
    return df  # Return the DataFrame

def initialize_clients(scopes, project_id):
    # BigQuery client initialization
    client_1 = bigquery.Client(project=project_id)
    credentials = pydata_google_auth.get_user_credentials(scopes, auth_local_webserver=True)
    client_2 = bigquery.Client(project=project_id, credentials=credentials)
    return client_1, client_2

# Checa se imoveis estao online
def checa_imoveis_online(id: Union[int, str]) -> Union[bool, None]:
    """
    Checa o site se o imóvel referente ao id está ainda disponível ou não.

    Args:
        id (Union[int, str]): id do imóvel

    Returns:
        Union[bool, None]: True -> Disponível
                           False -> Indisponível ou Não encontrado
                           None -> Erro na requisição

    Example:
    >>> id_list = [
    >>>     2585183366,
    >>>     2615503248,
    >>>     2578624305
    >>> ]

    >>> df = pd.DataFrame({'id' : id_list})

    >>> df['availability'] = df['id'].apply(check_availability)

    >>> df.head()

    	        id	                status
    0	        2585183366	        True
    1	        2615503248	        False
    2	        2578624305	        False
    """
    sleep(0.5)
    base_url = 'https://www.vivareal.com.br/imovel/'

    headers = {
        "origin": "https://www.vivareal.com.br",
        "x-domain": "www.vivareal.com.br",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36"
    }

    try:
        if isinstance(id, str):
            new_id = int(id)

        else:
            new_id = id

        if new_id < 0:
            new_id += 4294967296

        response = requests.get(url=base_url+str(new_id), headers=headers)
        
        if response.status_code >= 400:
            print(f'{new_id} - {response.status_code}')
            return False
        
        if 'Você está vendo esta página porque o imóvel que buscava foi alugado ou está indisponível.' in response.content.decode():
            return False
        
        return True
    
    except Exception as e:
        print(f'Erro inesperado: {e}')
        return None
    