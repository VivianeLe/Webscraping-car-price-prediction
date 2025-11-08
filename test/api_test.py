import pytest 
from fastapi.testclient import TestClient
from scripts import main

client = TestClient(main.app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "CAR PRICE PREDICTOR"}