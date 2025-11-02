import logging
# Import ML libraries and requirements
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
# from sklearn.pipeline import Pipeline
import xgboost as xgb
import numpy as np
import joblib
import mlflow
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from config import DATA_PATH, ARTIFACT_DIR, MODEL_PATH, PATH_TO_MODEL, PATH_TO_PREPROCESSOR
from lib.preprocessing import *
import pandas as pd

mlflow.set_tracking_uri(uri="http://localhost:8080")
# mlflow.set_tracking_uri("file:./mlruns")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("car_price_prediction")

def train():
    mlflow.set_experiment("car_price_training")
    logger.info(f"Data path: {DATA_PATH}")
    logger.info(f"Artifact dir: {ARTIFACT_DIR}")

    logger.info("Loading dataset...")
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    logger.info("Preparing features and target...")

    df = clean_data(df)

    X, Y, dv = run_encode_task(df)
    save_pickle(PATH_TO_PREPROCESSOR, dv)
    
    logger.info("Splitting train/test...")
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    logger.info("Building model...")
    # Define model parameters
    learning_rate = 0.5
    n_estimators=150
    max_depth=3
    subsample=1 
    colsample_bytree=1

    # Define model
    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        max_depth=max_depth,
        subsample=subsample, 
        colsample_bytree=colsample_bytree
    )

    logger.info("Training model...")
    with mlflow.start_run(run_name="car_price_xgb_3"):
        mlflow.log_param('learning_rate', learning_rate)
        mlflow.log_param('n_estimators', n_estimators)
        mlflow.log_param('max_depth', max_depth)
        mlflow.log_param('subsample', subsample)
        mlflow.log_param('colsample_bytree', colsample_bytree)

        model.fit(x_train, y_train)
        save_pickle(PATH_TO_MODEL, model)

        # Evaluate model performance
        logger.info("Evaluating model performance...")

        # Make predictions on training and test sets
        y_train_pred = model.predict(x_train)
        y_test_pred = model.predict(x_test)

        # Calculate metrics for training set
        train_mse = mean_squared_error(y_train, y_train_pred)
        train_mae = mean_absolute_error(y_train, y_train_pred)
        train_rmse = round(np.sqrt(mean_squared_error(y_train, y_train_pred)), 2)
        train_r2 = r2_score(y_train, y_train_pred)

        # Calculate metrics for test set
        test_mse = mean_squared_error(y_test, y_test_pred)
        test_mae = mean_absolute_error(y_test, y_test_pred)
        test_rmse = round(np.sqrt(mean_squared_error(y_test, y_test_pred)), 2)
        test_r2 = r2_score(y_test, y_test_pred)

        # Log training metrics
        logger.info("Training set metrics:")
        logger.info(f"  MSE: {train_mse:.4f}")
        logger.info(f"  RMSE: {train_rmse:.4f}")
        logger.info(f"  MAE: {train_mae:.4f}")
        logger.info(f"  R²: {train_r2:.4f}")

        # Log test metrics
        logger.info("Test set metrics:")
        logger.info(f"  MSE: {test_mse:.4f}")
        logger.info(f"  RMSE: {test_rmse:.4f}")
        logger.info(f"  MAE: {test_mae:.4f}")
        logger.info(f"  R²: {test_r2:.4f}")

        # Log model performance summary
        logger.info("Model performance summary:")
        logger.info(f"  Training R²: {train_r2:.4f}, Test R²: {test_r2:.4f}")
        logger.info(
            f"  Training RMSE: {train_rmse:.4f}, Test RMSE: {test_rmse:.4f}"
        )

        # save the model
        joblib.dump(model, MODEL_PATH)
        logger.info(f"Model saved to: {MODEL_PATH}")
        mlflow.log_metric("train_mse", train_mse)
        mlflow.log_metric("train_mae", train_mae)
        mlflow.log_metric("train_rmse", train_rmse)
        mlflow.log_metric("train_r2", train_r2)

        mlflow.log_metric("test_mse", test_mse)
        mlflow.log_metric("test_mae", test_mae)
        mlflow.log_metric("test_rmse", test_rmse)
        mlflow.log_metric("test_r2", test_r2)
        mlflow.log_artifact(MODEL_PATH, "artifacts")
        mlflow.sklearn.log_model(model, "model")

if __name__ == "__main__":
    train()
