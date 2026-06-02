# Projetos Bq
PROJECT_ID = "beebrokers"
DATASET_ID_1 = "Warehouse"
DATASET_ID_2 = "Sheets"

SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/drive']

TABLE_MAPPINGS = {
    'VivaReal': 'busca_bee',
    'Recomendacoes': 'recomendacoes'}
