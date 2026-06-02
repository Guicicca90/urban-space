import pandas as pd
from configs               import PROJECT_ID, DATASET_ID_1, DATASET_ID_2, TABLE_MAPPINGS, SCOPES
from utils                 import fetch_and_create_dataframe, initialize_clients,gera_link_maps
from limpeza_dados_bee     import Limpeza_Dados_Bee
from recomenda_imoveis_bee import Recomenda_Imoveis_Bee
from concurrent            import futures

# Inicializa os clientes do BigQuery
client_1, client_2 = initialize_clients(SCOPES, PROJECT_ID)

results = {}
with futures.ThreadPoolExecutor() as executor:
    future_to_table = {executor.submit(fetch_and_create_dataframe, client_1, PROJECT_ID, DATASET_ID_1, table_id, output_name): table_id
                       for table_id, output_name in TABLE_MAPPINGS.items()}
    for future in futures.as_completed(future_to_table):
        table_id = future_to_table[future]
        try:
            results[table_id] = future.result()
        except Exception as exc:
            pass  # Tratamento de erro opcional

# Define as tabelas
busca_bee     = results.get('VivaReal', None)
recomendacoes = results.get('Recomendacoes', None)

# Busca dados da Sheets.LnProprietario para o segundo cliente
ln = client_2.query(f'SELECT * FROM `{PROJECT_ID}.{DATASET_ID_2}.LnProprietario`').to_dataframe()

# --------------------------------------------------------------------------------------- #

# Filtra para buscar imoveis apenas para aqueles novos preenchimentos de ficha
ln = ln[~ln['Nome_Cliente'].isin(recomendacoes['Nome_Cliente'])]

# Cria as tabelas
# Só com as características para performar a busca
ln = ln[['Tipo_Negocio','Tipo','SubTipo','Tipo_Uso','Municipio',
         'Bairro','Amenidades','Num_Quartos','Num_Banheiros',
         'Num_Suites','Num_Vagas_Est','Area_Total_m2',
         'Area_Construida_m2','Condominio_Mensal','Iptu_Anual',
         'Preco','Email_Corretor','Nome_Cliente','CPF_Cliente']]

# Guarda o link e whatsapp dos imoveis recomendados 
busca_bee_link = busca_bee[['Link_Imovel','Tipo_Pessoa','WhatsApp','Lat_Long']]

# Seleciona a busca_bee relevante para o algoritmo
busca_bee = busca_bee[['Tipo_Negocio','Tipo','SubTipo','Tipo_Uso',
                        'Municipio','Bairro','Amenidades',
                        'Num_Quartos','Num_Banheiros',
                        'Num_Suites','Num_Vagas_Est',
                        'Area_Total_m2','Area_Construida_m2',
                        'Condominio_Mensal','Iptu_Anual','Preco']]

# Aplica a limpeza nos dados do formulario
ln_limpo, busca_bee_limpo, busca_bee_link_limpo = Limpeza_Dados_Bee(ln, busca_bee, busca_bee_link).limpar_dados()

# Gera as recomendacoes
recomenda_bee = Recomenda_Imoveis_Bee().aplica_knn(ln_limpo, busca_bee_limpo, busca_bee_link_limpo)

# Aplicar a função para gerar links do Google Maps
recomenda_bee['Google_Maps'] = recomenda_bee['Lat_Long'].apply(gera_link_maps)
recomenda_bee['CPF_Cliente'] = recomenda_bee['CPF_Cliente'].astype(str)

# --------------------------------------------------------------------------------------- #

# Importa pro bq
recomenda_bee.to_gbq('Warehouse.Recomendacoes', project_id='beebrokers', if_exists='append')