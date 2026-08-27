from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
from fastapi import APIRouter

from app.ml.explainer import get_explanations
from app.ml.model import model
from app.services.alerts import get_alerts_for_coords
from app.services.weather import get_this_weeks_data

router = APIRouter()

ALERT_PERCENTAGE_BUCKET = {
    "Special Weather Statement": 0,
    "Fog Advisory": 90,
    "Extreme Cold Warning": 75,
    "Freezing Drizzle Advisory": 90,
    "Freezing Rain Warning": 99,
    "Arctic Outflow Warning": 75,
    "Snowfall Warning": 80,
    "Blowing Snow Advisory": 80,
    "Winter Storm Watch": 99,
    "Snow Squall Warning": 90,
}

COUNTER = {
    "value": 0,
    "last_date": None,
    "hour": None,
}


@router.get("/predict")
async def predict(lat: float, lon: float):
    data = get_this_weeks_data(lat, lon)
    print(lat, lon)

    features = data.drop(columns=["date", "snow_day"], errors="ignore")
    probabilities = model.predict_proba(features)[:, 1]
    data["snow_day_probability"] = probabilities

    results = []
    for _, row in data.iterrows():
        result = {
            "weekday": describe_day(row["date"]),
            "snow_day_probability": float(round(row["snow_day_probability"] * 100)),
        }
        results.append(result)
        print(results[0])

    return results


@router.get("/alert")
async def alert(lat: float, lon: float):
    main_alert = get_primary_alert(lat, lon)
    print(main_alert)

    if main_alert is None:
        return None

    main_alert["polygons"] = None
    return main_alert


@router.get("/explain")
async def explain(lat: float, lon: float):
    data = get_this_weeks_data(lat, lon)

    features = data.drop(columns=["date", "snow_day"], errors="ignore")
    features = features.iloc[:1]

    all_explanations = get_explanations(features, model)
    explanations = all_explanations[0]

    results = []
    for explanation in explanations:
        if explanation["humanized_value"] is not None:
            results.append({"reason": explanation["humanized_value"]})

    return results


@router.get("/count")
async def update_counter():
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    hour = now.hour

    if COUNTER["last_date"] != today_str:
        COUNTER["value"] = 0
        COUNTER["last_date"] = today_str
    elif COUNTER["hour"] is not None and COUNTER["hour"] < 7 and hour >= 7:
        COUNTER["value"] = 0

    COUNTER["hour"] = hour
    COUNTER["value"] += 1

    return COUNTER["value"]


def get_primary_alert(lat, lon):
    alerts = get_alerts_for_coords(lat, lon)

    max_alert = None
    max_alert_value = 0
    for alert_item in alerts:
        alert_name = alert_item["type"]
        alert_value = ALERT_PERCENTAGE_BUCKET.get(alert_name, 0)
        alert_item["percentage"] = alert_value
        print(alert_name)

        if alert_value > max_alert_value:
            max_alert = alert_item
            max_alert_value = alert_value

    return max_alert


def describe_day(target_date):
    now = datetime.now(ZoneInfo("America/Toronto"))

    date = pd.to_datetime(target_date).date()
    today = now.date()

    diff = (date - today).days

    if diff == 0:
        return "Today"
    if diff == 1:
        return "Tomorrow"

    return pd.Timestamp(date).day_name()
