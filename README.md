# pramith-python-api

A simple FastAPI-based Python API project.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Endpoints

- `GET /` - returns a welcome message
- `GET /health` - returns a health status

## Tests

```bash
pytest
```
