import pandas as pd
import joblib

# Chargement du pipeline complet
pipeline = joblib.load('./model/apartment_price_pipeline.pkl')
df = pd.read_csv('DataSets/transactions2020.csv')

X = df.drop(columns=['prix'])
y = df['prix']


# Prédiction des prix
def predictAllPriceData():
    meanDifference = 0
    y_pred = pipeline.predict(X)
    for i in range(len(y)):
        meanDifference += abs(y_pred[i] - y[i])
    print(f"Mean Absolute Error: {round(meanDifference/len(y))}")

# Fonction de prédiction
def predict_price(new_data):
    new_data = pd.DataFrame(new_data, index=[0])
    return pipeline.predict(new_data)[0]

# Exemple d'utilisation
new_apartment = {
    'ville': 'PARIS',
    'surface_habitable': 98,
    'n_pieces': 4,
    'type_batiment': 'Appartement'
}

predicted_price = predict_price(new_apartment)
print(f"Predicted Price: {predicted_price}")




 