# 🚗 Car Price Prediction — Web Scraping, Machine Learning & MLOps Deployment

This project provides a **full end-to-end MLOps pipeline** for predicting car prices using scraped data, trained ML models, deployed API services, automated CI/CD workflows, and containerized infrastructure.

It includes:

- **Web scraping** from car marketplaces  
- **Data preprocessing & ML training**  
- **MLflow model registry**  
- **FastAPI inference API**  
- **Docker / Docker Compose orchestration**  
- **CI/CD with GitHub Actions**  
- **Deployment to Google Cloud Run**

---

## 📑 Table of Contents
1. [Project Architecture](#project-architecture)  
2. [Features](#features)  
3. [Technologies Used](#technologies-used)  
4. [Machine Learning Pipeline](#machine-learning-pipeline)  
5. [MLOps Workflow](#mlops-workflow)  
6. [FastAPI Inference Service](#fastapi-inference-service)  
7. [Docker & Docker Compose](#docker--docker-compose)  
8. [CI/CD — GitHub Actions](#cicd--github-actions)  
9. [Google Cloud Run Deployment](#google-cloud-run-deployment)  
10. [Future Work](#future-work)  
11. [License](#license)  
12. [Contact](#contact)

---

# 🏗️ Project Architecture
📦 car-price-prediction
│
├── data/                     # Raw & cleaned scraped datasets
├── notebooks/                # EDA, prototyping, experiments
│
├── scripts/
│   ├── scraping/             # Web scraping scripts
│   ├── training/             # Model training + MLflow logging
│   ├── lib/                  # Preprocessing (encode, load_pickle, etc.)
│   ├── routers/              # FastAPI routers (prediction API)
│   └── main.py               # FastAPI entrypoint
│
├── mlruns/                   # Local MLflow experiment tracking
│
├── Dockerfile                # Build API Docker image
├── docker-compose.yml        # MLOps infrastructure (API + MLflow + MinIO + Postgres)
│
├── .github/
│   └── workflows/            # GitHub Actions CI/CD pipelines
│
└── README.md

---

# ✨ Features

### ✔ Web Scraping  
- Selenium + BeautifulSoup  
- Auto User-Agent rotation  
- Save as CSV / Parquet

### ✔ Data Preprocessing  
- Outlier handling  
- Categorical encoding with DictVectorizer  
- Feature engineering on brand/model, mileage, gearbox, etc.

### ✔ Machine Learning  
- Linear Regression  
- Random Forest  
- Gradient Boosting / XGBoost  
- Hyperparameter tuning  
- Auto-logging to MLflow

### ✔ FastAPI Serving  
- Real-time car price inference  
- Pydantic validation  
- MLflow model loading

### ✔ MLOps  
- MLflow: tracking + model registry  
- PostgreSQL: MLflow metadata  
- MinIO (S3): artifact storage  
- Docker Compose orchestration  

### ✔ CI/CD  
- Automated testing  
- Linting  
- Docker image build & push  
- Deployment to Google Cloud Run

---

# 🔬 Machine Learning Pipeline

### 1️⃣ Data Collection  
Scrape car listings from online marketplaces.

### 2️⃣ Preprocessing  
- Handle missing values  
- Encode categorical variables  
- Standardize numerical features  
- Build DictVectorizer transformer  

### 3️⃣ Model Training

```bash
python scripts/training/train.py
```

### 4️⃣ Model Registry (MLflow)
Models are registered with alias:

```bash
models:/car_price_predictor@the_best
```

# ⚙️ MLOps Workflow

### Components

| Component       | Description |
|----------------|-------------|
| **MLflow** | Model tracking, experiment logging, model registry |
| **PostgreSQL** | Backend store for MLflow metadata |
| **MinIO (S3)** | Storage for ML artifacts (models, preprocessors, datasets) |
| **Docker Compose** | Orchestration of MLflow + S3 + API services |
| **GitHub Actions** | CI/CD automation for testing, building, deploying |
| **Google Cloud Run** | Final deployment of the prediction API |

This architecture allows fully reproducible machine learning workflows with versioned models, automated builds, and scalable deployment.

---

# 🧠 Machine Learning Lifecycle

The full ML lifecycle implemented:

1. **Data ingestion** from web scraping  
2. **Preprocessing pipeline** (DictVectorizer, cleaning, encoding)  
3. **Training** regression models with hyperparameter tuning  
4. **Logging** metrics, parameters, and artifacts to MLflow  
5. **Registering** the best model under an alias (e.g., `@the_best`)  
6. **Deployment** via FastAPI using MLflow’s model registry  
7. **Serving** predictions in production through Cloud Run  

---

# ⚡ FastAPI Inference Service

The prediction service is developed using **FastAPI**.

### Start service locally

```bash
uvicorn scripts.main:app --host 0.0.0.0 --port 8080
```

Example prediction request:
```json
POST /car_price/predict
[
  {
    "Brand": "Toyota",
    "Name": "Camry",
    "Color": "Blue",
    "Fuel": "Essence",
    "Gearbox": "Automatic",
    "Year": 2018,
    "Km": 30000,
    "Fuel_consumption": 7.5,
    "Co2_emission": 170,
    "Doors": 4
  }
]
```

# 🐳 Docker & Docker Compose

The entire infrastructure—including MLflow, PostgreSQL, MinIO (S3), and the FastAPI inference service—is containerized using Docker and orchestrated with Docker Compose.

---

### 📦 Build API Docker Image

To build the FastAPI service image:

```bash
docker build -t car-price-api .
```

### ▶️ Run API Container Locally
```bash
docker run -p 8080:8080 car-price-api
```

This exposes the FastAPI prediction endpoint at:
```bash
http://localhost:8080/car_price/predict
```

# 🏗️ Launch Full MLOps Stack (MLflow + PostgreSQL + MinIO + API)
```bash
docker compose up --build
```
This will start the following services:

| Service           | Description                                             |
| ----------------- | ------------------------------------------------------- |
| **mlflow-server** | MLflow tracking and model registry                      |
| **postgres**      | Backend metadata store for MLflow                       |
| **minio**         | S3-compatible artifact store (model files, vectorizers) |
| **our-app**       | FastAPI car price prediction API                        |

After startup:

- MLflow UI → http://localhost:5050

- MinIO Console → http://localhost:9001

- FastAPI Docs → http://localhost:8080/docs

# 🚀 CI/CD — GitHub Actions

A complete CI/CD workflow is provided using GitHub Actions.
The pipeline automates:

🔧 Installing dependencies

🧪 Running unit tests via pytest

🧹 Linting using flake8

🐳 Building Docker images

📦 Pushing images to Google Artifact Registry

🌍 Deploying the latest API version to Google Cloud Run

### ☁️ Google Cloud Run Deployment
The model inference API is deployed on Google Cloud Run, a fully managed serverless platform that scales automatically.

### ⭐ Benefits of Cloud Run

- Automatic scaling to zero

- Built-in HTTPS

- High availability

- Integrated with Google Artifact Registry

- Pay-per-use (cost-efficient)

# 🔮 Future Work

- Build an interactive Streamlit UI for price visualization

- Integrate LLM-based natural language car value queries

- Add Airflow / Cloud Composer for automated retraining

- Implement Prometheus + Grafana monitoring

- Expand dataset from multiple car marketplaces

- Enhance modeling with LightGBM / CatBoost

# 📄 License

This repository is licensed under the MIT License.
See the LICENSE file for full details.

### 👩‍💻 Contact

Viviane Le
📧 Email: anhlv.fpt@gmail.com

🐙 GitHub: https://github.com/VivianeLe