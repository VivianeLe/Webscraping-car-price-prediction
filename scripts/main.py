from enum import Enum
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from routers import prediction
from schema import request, response
import mlflow.sklearn
import pandas as pd

app = FastAPI()
app.include_router(prediction.car_price_router)

@app.get("/")
def root():
    return {"message": "CAR PRICE PREDICTOR"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)