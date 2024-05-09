import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.impute import SimpleImputer

test =  False

def getDataFrame():
    arrays = dict(np.load("./DataSets/transactions.npz"))
    data = {k: [s.decode("utf-8") for s in v.tobytes().split(b"\x00")] if v.dtype == np.uint8 else v for k, v in arrays.items()}
    return preprocessDf(pd.DataFrame.from_dict(data))
    
def getTestDf():
     return preprocessDf(pd.read_csv("./DataSets/transactions_sample.csv"))

def preprocessDf(df):
    drop_cols = ["id_transaction", "id_ville", "vefa", 
                 'id_parcelle_cadastre', 'latitude', 'longitude',
                 'surface_dependances', 'surface_locaux_industriels',
                 'surface_terrains_agricoles', 'surface_terrains_sols',
                 'surface_terrains_nature', 'adresse']
    df = df.drop(columns=drop_cols)
    df.dropna()
    df.drop_duplicates()
    df = df[df['date_transaction'] > '2023-06-29']
    return df

df = getTestDf() if test else getDataFrame()

print(df.tail())
print(len(df))


X = df.drop(columns=['prix','date_transaction'])  
y = df['prix']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical_features = ['departement', 'ville', 'code_postal', 'type_batiment']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Préprocesseur
numeric_features = ['n_pieces', 'surface_habitable']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_features = ['departement', 'ville', 'code_postal', 'type_batiment']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Préprocesseur global
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Création du pipeline avec un modèle de forêt aléatoire
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42))
])

# Recherche des hyperparamètres optimaux
param_grid = {
    'regressor__n_estimators': [100, 200, 300],
    'regressor__max_depth': [None, 10, 20, 30],
    'regressor__min_samples_split': [2, 5, 10],
    'regressor__min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Meilleur modèle
best_model = grid_search.best_estimator_

# Prédictions sur l'ensemble de test
y_pred = best_model.predict(X_test)

# Évaluation du modèle
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae:.2f} €')