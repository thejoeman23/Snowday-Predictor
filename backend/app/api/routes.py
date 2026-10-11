from fastapi import APIRouter

from app.ml.model import model
from app.services.weather import get_this_weeks_data

router = APIRouter()

# TODO: Create a route to get the raw weather data for a given location (lat, lon)
# TODO: Connect predictions to database to reduce the number of API calls to the weather service

@router.get("/predict")
async def predict(lat: float, lon: float):
    data = get_this_weeks_data(lat, lon)

    features = data.drop(columns=["date", "snow_day"], errors="ignore")
    probabilities = model.predict_proba(features)[:, 1]
    data["snow_day_probability"] = probabilities

    results = []
    for _, row in data.iterrows():
        result = {
            "weekday": row["date"],
            "snow_day_probability": float(round(row["snow_day_probability"] * 100)),
        }
        results.append(result)

    return results