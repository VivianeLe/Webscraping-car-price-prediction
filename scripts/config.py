import os
from pathlib import Path

MODEL_VERSION = "1"
MODEL_NAME = "car_price_predictor"
ALIAS = "the_best"
PATH_TO_MODEL = f"./scripts/model/model__v{MODEL_VERSION}.pkl"
PATH_TO_PREPROCESSOR = f"./scripts/model/dv__v{MODEL_VERSION}.pkl"

# Paths
PROJECT_ROOT = Path(os.getcwd())
DATA_PATH = "./data/car-price2.csv"
ARTIFACT_DIR = PROJECT_ROOT / "scripts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = ARTIFACT_DIR / "model" / "car_price_linear.joblib"

TEXT_COLS = ['Name', 'Color']
CATEGORICAL_COLS = ['Brand', 'Name', 'Color', 'Fuel', 'Gearbox']
NUMERICAL_COLS = ['Year', 'Km', 'Fuel_consumption', 'Co2_emission', 'Doors']