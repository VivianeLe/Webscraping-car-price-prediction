import pytest 
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_load_pickle():
    dv = MagicMock()
    dv.transform.return_value = [0.5]
    with patch("scripts.routers.prediction.load_pickle", return_value=dv):
        yield dv

@pytest.fixture
def mock_get_model():
    mock_model = MagicMock() 
    mock_model.predict.return_value = [15000.0]  # Giả lập giá dự đoán
    return mock_model

@pytest.fixture
def mock_mlflow_server(mock_get_model, mock_load_pickle):
    model = mock_get_model
    dv = mock_load_pickle
    mlflow_server = MagicMock()
    mlflow_server.sklearn.load_model.return_value = model
    with patch("scripts.routers.prediction.mlflow", mlflow_server): 
        yield mlflow_server

# @pytest.fixture
# def mock_pandas():
#     mock_pandas = MagicMock()
#     mock_pandas.DataFrame.return_value = {"test": [{
#         "Brand": "Toyota", "Name": "Camry", "Color": "Blue",
#         "Fuel": "Essence", "Gearbox": "Automatic",
#         "Year": 2018, "Km": 30000, "Fuel_consumption": 7.5,
#         "Co2_emission": 170, "Doors": 4
#     }]}
#     with patch("scripts.routers.prediction.pd", mock_pandas):
#         yield mock_pandas

def test_get_model(mock_get_model, mock_load_pickle, mock_mlflow_server):
    from scripts.routers.prediction import _get_model

    model, dv = _get_model()
    assert model == mock_get_model
    assert dv == mock_load_pickle
    data = dv.transform(['a', 'b', 'c'])
    result = model.predict([1,2,3])  
    assert data == [0.5]
    assert result == [15000.0]

def test_predict(mock_get_model, mock_load_pickle, mock_mlflow_server):
    import scripts.routers.prediction as pred
    pred._model = None
    pred._dv = None

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from scripts.routers.prediction import car_price_router

    app = FastAPI()
    app.include_router(car_price_router)
    client = TestClient(app)

    payload = [{
        "Brand": "Toyota","Name": "Camry","Color": "Blue",
        "Fuel": "Essence","Gearbox": "Automatic","Year": 2018,
        "Km": 30000,"Fuel_consumption": 7.5,"Co2_emission": 170,"Doors": 4
    }]

    # mock_load_pickle.transform.assert_called_once()

    resp = client.post("/car_price/predict", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"predicted_price": 15000.0}