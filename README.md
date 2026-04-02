# Deploy Scikit-Learn Iris flower classification model with FastAPI

---

### Install requirements


1. Install requirements

```
rm -rf .venv
virtualenv -p python3.12 .venv
. .venv/bin/activate
pip install --upgrade pip

pip install -r requirements.txt
```

### Start the server

```shell
export MODEL_DIR="$(pwd)"
gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 server:app
```

### Example Inference Call

```shell
curl -X 'POST' \
  'http://0.0.0.0:8000/predict?sepal_length=5.3&sepal_width=5.4&petal_length=3.5&petal_width=4.6' \
  -H 'accept: application/json'
```
