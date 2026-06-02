import pandas as pd
import numpy  as np
import ast
from unidecode import unidecode

# Faz a limpeza de dados e mapeamento de amenidades antes da execucao do algoritmo
class Limpeza_Dados_Bee:
    def __init__(self, ln, busca_bee, busca_bee_link):
        self.ln = ln
        self.busca_bee = busca_bee
        self.busca_bee_link = busca_bee_link
        self.amenities_match = {"Area de Servico": "SERVICE_AREA","Copa Cozinha": "KITCHEN","Churrasqueira": "BARBECUE_GRILL",
                                "Despejo": "","Despensa": "PANTRY","Dorms Empregada": "","Escritorio": "HOME_OFFICE","Escritorio c WC": ["HOME_OFFICE", "SERVICE_BATHROOM"],
                                "Elevador": "ELEVATOR","Espaco Gourmet": "GOURMET_SPACE","Edicula": "EDICULE","Geminado": "","Lavabo": "LAVABO",
                                "Piscina": ["POOL", "ADULT_POOL", "CHILDRENS_POOL"],"Quintal": "BACKYARD","Spa": "SPA","Sala 2 Ambientes": "LARGE_ROOM",
                                "Sala de Jantar": "DINNER_ROOM","Sala Intima": "SMALL_ROOM","Sacada": "BALCONY","Suite Hidro, Closet": ["WHIRLPOOL", "CLOSET"],
                                "Varanda": "BALCONY","WC Empregada": "SERVICE_BATHROOM","WC Social": "BATHROOM_CABINETS","Adega": "","Alarme": "ALARM_SYSTEM",
                                "Aquecedor a Gas": "","Aquecedor Eletrico": "","Aquecedor Eletrico Solar": "SOLAR_ENERGY","Ar Condicionado": "AIR_CONDITIONING",
                                "Canil": "DOG_KENNEL","Camera de Seguranca": "SECURITY_CAMERA","Casa Caseiro": "CARETAKER_HOUSE",
                                "Campo de Futebol": "FOOTBALL_FIELD","Cachoeira": "","Cerca Eletrica": "FENCE","Interfone": "INTERCOM",
                                "Lago": "LAKE","Mobiliada": "FURNISHED","Poco Artesiano": "ARTESIAN_WELL","Pomar": "FRUIT_TREES",
                                "Playground": "PLAYGROUND","Portao Automatico": "ELECTRONIC_GATE","Quiosque": "","Quadra de Tenis": "TENNIS_COURT",
                                "Quadra Poliesportiva": "SPORTS_COURT","Sala de jogos": "GAMES_ROOM","Sala de Ginastica": "FITNESS_ROOM",
                                "Salao de festas": "PARTY_HALL","Sauna": "SAUNA","Ventilador de teto": "","Vestiario": "",
                                "Vista Panoramica": "PANORAMIC_VIEW","Academia": "GYM","Brinquedoteca": "","Camera de seguranca": "SECURITY_CAMERA",
                                "Campo de golfe": "GOLF_FIELD","Clube": "","Deposito": "STORAGE_ROOM","Espaço homem": "","Espaço mulher": "",
                                "Heliponto": "HELIPAD","Horta": "VEGETABLE_GARDEN","Jardim": "GARDEN","Lavanderia coletiva": "LAUNDRY",
                                "Salao de festas": "PARTY_HALL","Playground": "PLAYGROUND","Lago": "LAKE","Piscina adulto": "ADULT_POOL",
                                "Piscina infantil": "CHILDRENS_POOL","Portaria fisica": "","Portaria remota": "","Quadra poliesportiva": "SPORTS_COURT",
                                "Quadra de tenis": "TENNIS_COURT","Salao de jogos": "GAMES_ROOM","Sauna": "SAUNA","Segurança 24h": "SECURITY_24_HOURS",
                                "Solarium": "SOLARIUM"}
        
    def remove_aspas_virgulas(self, s):
        if isinstance(s, str):
            return s.replace("'", "").replace(",", "").replace("\"", "")
        else:
            return s

    def converte_amenidades(self, row):
        amenities = row.split(', ')
        converted = []
        for amenity in amenities:
            if amenity in self.amenities_match:
                match = self.amenities_match[amenity]
                if isinstance(match, list):
                    converted.extend(match)
                else:
                    converted.append(match)
        return ', '.join(converted)

    def amenidades_para_lista(self, amenities_str):
        try:
            return ast.literal_eval(amenities_str)
        except (ValueError, SyntaxError):
            return []

    def splita_strings_colunas(self, column):
        processed_column = []
        for item in column:
            if not pd.isnull(item):
                processed_items = [unidecode(word.strip().lower()) for word in item.split(',')]
                processed_column.append(', '.join(processed_items))
            else:
                processed_column.append(item)
        return processed_column

    def limpar_dados(self):
        self.ln['Amenidades'] = self.ln['Amenidades'].apply(lambda x: self.converte_amenidades(x) if pd.notnull(x) else x)
        self.busca_bee['SubTipo'] = self.busca_bee['SubTipo'].replace('Nao Informado', np.nan)
        self.busca_bee['SubTipo'] = self.busca_bee['SubTipo'].apply(self.remove_aspas_virgulas)
        self.ln['Municipio'] = self.splita_strings_colunas(self.ln['Municipio'])
        self.ln['Bairro'] = self.splita_strings_colunas(self.ln['Bairro'])
        self.busca_bee['Municipio'] = self.busca_bee['Municipio'].str.lower()
        self.busca_bee['Bairro'] = self.busca_bee['Bairro'].str.lower()

        return self.ln, self.busca_bee, self.busca_bee_link