from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import joblib
import redis
import os

app = FastAPI()
host_name = os.getenv("REDIS_HOST", "localhost")
port_name = os.getenv("REDIS_PORT", 6379)
redis_client = redis.Redis(host=host_name, port=port_name, decode_responses=True)

try:
    model = joblib.load("spam_predictor.joblib")
except Exception:
    model = None

class PredictRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(input: PredictRequest):
    cached_prediction = redis_client.get(input.text)
    if cached_prediction is not None:
        return {"label": cached_prediction}
    if model is None:
        raise HTTPException(status_code=503, detail="Model hasn't been loaded")
    prediction = str(model.predict([input.text])[0])
    redis_client.setex(name=input.text, time=300, value=prediction)
    return {"label": prediction}

@app.get("/healthz", status_code = status.HTTP_200_OK)
def check_health():
    if model == None:
        raise HTTPException(status_code=503, detail="Model hasn't been loaded")
    return {"status" : "ok"}

