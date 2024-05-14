import numpy as np  
import pandas as pd

arrays = dict(np.load("./DataSets/transactions.npz"))
data = {k: [s.decode("utf-8") for s in v.tobytes().split(b"\x00")] if v.dtype == np.uint8 else v for k, v in arrays.items()}


drop_cols = ["id_transaction", "id_ville", "vefa", 
                 'id_parcelle_cadastre', 'latitude', 'longitude',
                 'surface_dependances', 'surface_locaux_industriels',
                 'surface_terrains_agricoles', 'surface_terrains_sols',
                 'surface_terrains_nature', 'adresse','departement','code_postal']

df  = pd.DataFrame.from_dict(data)
df = df.drop(columns=drop_cols)
df = df.dropna()
df = df.drop_duplicates()
df = df[df['date_transaction'] > '2020-01-01']
# df = df[df['date_transaction'] < '2023-01-01']
df = df.drop(columns=['date_transaction'])

# 40 plus grosses ville de france  Array 
big_cities = ['LYON', 'TOULOUSE', 'NICE', 'NANTES', 'STRASBOURG', 'MONTPELLIER', 'BORDEAUX', 'LILLE', 'RENNES', 'REIMS', 'LE HAVRE', 'TOULON', 'GRENOBLE', 'DIJON', 'ANGERS', 'NIMES', 'VILLEURBANNE', 'SAINT-DENIS', 'LE MANS', 'AIX EN PROVENCE', 'BREST', 'CLERMONT FERRAND', 'TOURS', 'AMIENS', 'LIMOGES', 'ANNEMASSE', 'PERPIGNAN', 'BESANCON', 'ORLEANS', 'METZ', 'ROUEN', 'SAINT-DENIS', 'AVIGNON', 'NANCY', 'ARGENTEUIL', 'MULHOUSE', 'ROUBAIX', 'TOULOUSE','PARIS 01', 'PARIS 02', 'PARIS 03', 'PARIS 04', 'PARIS 05', 'PARIS 06', 'PARIS 07', 'PARIS 08', 'PARIS 09', 'PARIS 10', 'PARIS 11', 'PARIS 12', 'PARIS 13', 'PARIS 14', 'PARIS 15', 'PARIS 16', 'PARIS 17', 'PARIS 18', 'PARIS 19', 'PARIS 20', 'MARSEILLE 1ER' , 'MARSEILLE 2EME', 'MARSEILLE 3EME', 'MARSEILLE 4EME', 'MARSEILLE 5EME', 'MARSEILLE 6EME', 'MARSEILLE 7EME', 'MARSEILLE 8EME', 'MARSEILLE 9EME', 'MARSEILLE 10EME', 'MARSEILLE 11EME', 'MARSEILLE 12EME', 'MARSEILLE 13EME', 'MARSEILLE 14EME', 'MARSEILLE 15EME', 'MARSEILLE 16EME', 'MARSEILLE 1ER', 'MARSEILLE 2EME', 'MARSEILLE 3EME', 'MARSEILLE 4EME', 'MARSEILLE 5EME', 'MARSEILLE 6EME', 'MARSEILLE 7EME', 'MARSEILLE 8EME', 'MARSEILLE 9EME', 'MARSEILLE 10EME', 'MARSEILLE 11EME', 'MARSEILLE 12EME', 'MARSEILLE 13EME', 'MARSEILLE 14EME', 'MARSEILLE 15EME', 'MARSEILLE 16EME', 'LYON 1ER ','LYON 2EME', 'LYON 3EME', 'LYON 4EME', 'LYON 5EME', 'LYON 6EME', 'LYON 7EME', 'LYON 8EME', 'LYON 9EME', 'LYON 1ER', 'LYON 2EME', 'LYON 3EME', 'LYON 4EME', 'LYON 5EME', 'LYON 6EME', 'LYON 7EME', 'LYON 8EME', 'LYON 9EME']

df = df[df['ville'].isin(big_cities)]
df = df.reset_index(drop=True)

print(f"nb lignes: {df.shape[0]}")

df.to_csv('./DataSets/transactions2020.csv', index=False)