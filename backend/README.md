# Snow Day Predictor Backend

FastAPI backend for Snow Day Predictor. This is intentionally close to the original working backend: it loads the existing Random Forest model, fetches Open-Meteo forecast data, computes snow-day features, exposes prediction/explanation endpoints, and fetches Environment Canada alerts.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

The API will be available at `http://localhost:8080`.

## Docker

Build and run from this `backend/` directory:

```bash
docker build -t snowday-backend .
docker run --rm -p 8080:8080 snowday-backend
```

## Endpoints

- `GET /predict?lat=44.569&lon=-80.98`
- `GET /explain?lat=44.569&lon=-80.98`
- `GET /alert?lat=44.569&lon=-80.98`
- `GET /count`
