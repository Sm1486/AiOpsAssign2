from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import joblib

app = FastAPI()
try:
    model = joblib.load("spam_predictor.joblib")
except Exception:
    model = None

class PredictRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(input: PredictRequest):
    prediction = model.predict([input.text])[0]
    return {"label": prediction}

@app.get("/healthz", status_code = status.HTTP_200_OK)
def check_health():
    if model == None:
        raise HTTPException(status_code=503, detail="Model hasn't been loaded")
    return {"status" : "ok"}

