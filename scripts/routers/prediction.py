import mlflow.sklearn
import pandas as pd
from fastapi import APIRouter
from typing import List
import logging
import os, time, requests
from scripts.schema.request import CarPriceRequest
from scripts.schema.response import CarPriceResponse
from scripts.lib.preprocessing import encode_cols, load_pickle
from scripts.config import MODEL_NAME, PATH_TO_PREPROCESSOR, ALIAS

logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:8080")

# MLFLOW_TRACKING_URI = os.getenv("OUR_MLFLOW_HOST", "http://0.0.0.0:8080")
mlflow.set_tracking_uri(uri=MLFLOW_TRACKING_URI)
mlflow.set_experiment("car_price_training")
model_uri = f"models:/{MODEL_NAME}@{ALIAS}"
# model_uri = os.getenv("MODEL_URI", "models:/car_price_predictor@the_best")

car_price_router = APIRouter(prefix="/car_price")

_model = None
_dv = None

# def _wait_for_mlflow(timeout=90):
#     url = MLFLOW_TRACKING_URI.rstrip("/") + "/health"
#     t0 = time.time()
#     while True:
#         try:
#             requests.get(url, timeout=2)
#             return
#         except Exception:
#             if time.time() - t0 > timeout:
#                 raise
#             time.sleep(2)

def _get_model():
    global _model, _dv
    if _model is None:
        # _wait_for_mlflow()
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        _dv = load_pickle(PATH_TO_PREPROCESSOR)
        _model = mlflow.sklearn.load_model(model_uri)
    return _model, _dv

@car_price_router.post("/predict", response_model=CarPriceResponse)
def run_inference(user_input: List[CarPriceRequest]) -> CarPriceResponse:
    model, dv = _get_model()
    # dv = load_pickle(PATH_TO_PREPROCESSOR)
    df = pd.DataFrame([x.dict() for x in user_input])
    df = encode_cols(df)
    X = dv.transform(df.to_dict(orient="records"))
    y = model.predict(X)
    return CarPriceResponse(predicted_price=float(y[0]))