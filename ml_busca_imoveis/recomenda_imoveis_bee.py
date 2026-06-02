import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors    import NearestNeighbors

class Recomenda_Imoveis_Bee:
    def __init__(self, num_cols=['Area_Construida_m2', 'Preco']):
        self.num_cols = num_cols

    def aplica_hard_filters(self, busca_bee, ln_row):
        filter_columns = ['Tipo_Negocio', 'Tipo', 'SubTipo', 'Tipo_Uso', 'Municipio', 'Bairro']
        temp_df = busca_bee
        for col in filter_columns:
            if col in ln_row.index and pd.notna(ln_row[col]):
                value_list = [v.strip() for v in str(ln_row[col]).split(',')]
                temp_df = temp_df[temp_df[col].isin(value_list) | temp_df[col].isna()]
        return temp_df

    def aplica_knn(self, ln, busca_bee, busca_bee_link):
        final_recommendations = pd.DataFrame()

        for index, ln_row in ln.iterrows():
            filtered_busca_bee = self.aplica_hard_filters(busca_bee, ln_row)
            ln_num = ln_row[self.num_cols].fillna(0).to_frame().T
            filtered_busca_bee_num = filtered_busca_bee[self.num_cols].fillna(0)

            if filtered_busca_bee_num.shape[0] > 0:
                scaler = StandardScaler()
                filtered_busca_bee_scaled = scaler.fit_transform(filtered_busca_bee_num)
                ln_scaled = scaler.transform(ln_num)

                n_neighbors = min(100000, filtered_busca_bee_scaled.shape[0])
                knn = NearestNeighbors(n_neighbors=n_neighbors)
                knn.fit(filtered_busca_bee_scaled)
                distances, indices = knn.kneighbors(ln_scaled)

                similar_rows = filtered_busca_bee.iloc[indices[0]].copy()
                similar_rows['Similaridade'] = distances[0].argsort().argsort() + 1
                similar_rows['Email_Corretor'] = ln_row['Email_Corretor']
                similar_rows['Nome_Cliente'] = ln_row['Nome_Cliente']
                similar_rows['CPF_Cliente'] = ln_row['CPF_Cliente']

                final_recommendations = pd.concat([final_recommendations, similar_rows], ignore_index=True)
            else:
                print(f"Nenhum imóvel encontrado que atenda aos critérios de busca para a linha {index}.")

        final_recommendations = final_recommendations.merge(busca_bee_link, left_index=True, right_index=True, how='left')
        for col in final_recommendations.columns:
            if final_recommendations[col].dtype == 'object':
                final_recommendations[col] = final_recommendations[col].astype(str)

        return final_recommendations

