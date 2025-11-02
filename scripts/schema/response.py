from pydantic import BaseModel

class CarPriceResponse(BaseModel):
    predicted_price: float
