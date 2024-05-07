# import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def getDataFrame():
  # arrays = dict(np.load(self.file))
  # data = {k: [s.decode("utf-8") for s in v.tobytes().split(b"\x00")] if v.dtype == np.uint8 else v for k, v in arrays.items()}
  # return self.preprocessDf(pd.DataFrame.from_dict(data))
  return preprocessDf(pd.read_csv("./DataSets/transactions_sample.csv"))


def preprocessDf(df):
  df = df.drop(columns=["id_transaction", "date_transaction", "id_ville", "vefa", 
    'id_parcelle_cadastre', 'latitude', 'longitude',
    'surface_dependances', 'surface_locaux_industriels',
    'surface_terrains_agricoles', 'surface_terrains_sols',
    'surface_terrains_nature'])
  df = df.dropna()
  df = df.drop_duplicates()
  return df

df = getDataFrame()

X = df[df.columns]
y = df['prix']


categorical_features = ['Departement', 'Ville', 'Type_batiment']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

numeric_features = ['n_pieces', 'surface_habitable']
numeric_transformer = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                 ('regressor', keras.Sequential([
                                     keras.layers.Dense(64, activation='relu', input_shape=[len(df.columns)]),
                                     keras.layers.Dense(64, activation='relu'),
                                     keras.layers.Dense(1)
                                 ]))
                                ])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model_pipeline['regressor'].compile(optimizer='adam',
                                    loss='mean_squared_error',
                                    metrics=['mean_absolute_error'])

model_pipeline.fit(X_train, y_train, epochs=10, validation_split=0.1)


model_loss, model_mae = model_pipeline.evaluate(X_test, y_test)
print("Perte moyenne sur les tests:", model_loss)
print("Erreur absolue moyenne sur les tests:", model_mae)


# input_data = {
#     'date_transaction': ['2021-06-01'],
#     'Departement': ['Paris'],
#     'id_ville': [1],
#     'Ville': ['Paris'],
#     'code_postal': [75001],
#     'Adresse': ['123 rue de exemple'],
#     'Type_batiment': ['Appartement'],
#     'n_pieces': [3],
#     'surface_habitable': [75]
# }
# input_df = pd.DataFrame(input_data)
# predicted_price = model_pipeline.predict(input_df)
# print("Prix prédit:", predicted_price)
