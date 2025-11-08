import mlflow.sklearn
import pandas as pd
from fastapi import APIRouter
from typing import List
import logging
import os
from scripts.schema.request import CarPriceRequest
from scripts.schema.response import CarPriceResponse
from scripts.lib.preprocessing import encode_cols, load_pickle
from scripts.config import MODEL_NAME, PATH_TO_PREPROCESSOR, ALIAS

logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("OUR_MLFLOW_HOST", "http://localhost:5050")
print(f"MLFLOW_TRACKING_URI: {MLFLOW_TRACKING_URI}")

mlflow.set_tracking_uri(uri=MLFLOW_TRACKING_URI)
model_uri = f"models:/{MODEL_NAME}@{ALIAS}"

def get_model():
    """Lazy load the MLflow model only when needed."""
    global _model
    if _model is None:
        _model = mlflow.sklearn.load_model(model_uri)
    return _model

# model = mlflow.sklearn.load_model(model_uri)

# Load DictVectorizer
dv = load_pickle(PATH_TO_PREPROCESSOR)

car_price_router = APIRouter(prefix="/car_price")

# /car_price/predict
@car_price_router.post("/predict", response_model=CarPriceResponse)
def run_inference(user_input: List[CarPriceRequest]) -> CarPriceResponse:
    model = get_model()
    df = pd.DataFrame([x.dict() for x in user_input])
    df = encode_cols(df)
    dicts = df.to_dict(orient="records")
    X = dv.transform(dicts)
    y = model.predict(X)
    logger.info(f"Predicted car price: {y} USD")
    return CarPriceResponse(predicted_price=y[0])
