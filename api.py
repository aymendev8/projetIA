from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

pipeline = joblib.load('./model/apartment_price_pipeline.pkl')


class ModelInput(BaseModel):
    ville: str
    surface_habitable: int
    n_pieces: int
    type_batiment: str


@app.post("/predict")
def predict(input_data: ModelInput):
    try:
       data = {
            "ville": [input_data.ville],
            "surface_habitable": [input_data.surface_habitable],
            "n_pieces": [input_data.n_pieces],
            "type_batiment": [input_data.type_batiment]
        }
       input_df = pd.DataFrame(data)
       prediction = pipeline.predict(input_df)
        
       return {"prediction": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)