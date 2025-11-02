import mlflow.sklearn
import pandas as pd
from fastapi import APIRouter
from sklearn.base import BaseEstimator
from schema.request import CarPriceRequest
from schema.response import CarPriceResponse
from sklearn.feature_extraction import DictVectorizer
from typing import List
import numpy as np
import logging
from lib.preprocessing import encode_cols, load_pickle
from config import MODEL_NAME, PATH_TO_PREPROCESSOR, ALIAS

logger = logging.getLogger(__name__)
mlflow.set_tracking_uri(uri="http://localhost:8080")
model_uri = f"models:/{MODEL_NAME}@{ALIAS}"
model = mlflow.sklearn.load_model(model_uri)

# Load DictVectorizer
dv = load_pickle(PATH_TO_PREPROCESSOR)

car_price_router = APIRouter(prefix="/car_price")

# /car_price/predict
@car_price_router.post("/predict", response_model=CarPriceResponse)
def run_inference(user_input: List[CarPriceRequest]) -> CarPriceResponse:
    df = pd.DataFrame([x.dict() for x in user_input])
    df = encode_cols(df)
    dicts = df.to_dict(orient="records")
    X = dv.transform(dicts)
    y = model.predict(X)
    logger.info(f"Predicted car price: {y} USD")
    return CarPriceResponse(predicted_price=y[0])
