import os
from contextlib import asynccontextmanager
from typing import Dict, List

import joblib
import pandas as pd

import pymysql
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

model = None

def _get_model_dir():
    return os.getenv("MODEL_DIR", ".")


model = None
MODEL_PATH = os.path.join(_get_model_dir(), "iris_classifier.joblib")


def load_model():
    _model = joblib.load(MODEL_PATH)
    return _model


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = load_model()
    yield


app = FastAPI(lifespan=lifespan, root_path=os.getenv("TFY_SERVICE_ROOT_PATH", ""))


@app.get("/health")
async def health() -> Dict[str, bool]:
    return {"healthy": True}


@app.post("/predict")
def predict(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float):
    global model
    class_names = ["setosa", "versicolor", "virginica"]
    data = dict(
        sepal_length=sepal_length,
        sepal_width=sepal_width,
        petal_length=petal_length,
        petal_width=petal_width,
    )
    prediction = model.predict_proba(pd.DataFrame([data]))[0]
    predictions = []
    for label, confidence in zip(class_names, prediction):
        predictions.append({"label": label, "score": confidence})
    return {"predictions": predictions}


@app.get("/checkdb")
def checkdb():
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST")

    if not all([db_user, db_pass, db_host]):
        return {"status": "error", "message": "DB_USER, DB_PASS, or DB_HOST env variables not set"}

    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
        )
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            databases = [row[0] for row in cursor.fetchall()]
        connection.close()
        return {"status": "ok", "databases": databases}
    except Exception as e:
        return {"status": "error", "message": str(e)}
