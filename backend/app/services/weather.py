import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import requests

if __name__ == "__main__" and __package__ is None:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.core.config import (
    DATA_DIR,
    DEFAULT_LATITUDE,
    DEFAULT_LONGITUDE,
    LOCAL_TIMEZONE,
    SNOW_DAY_DATES_PATH,
)

SNOW_DAYS = pd.read_csv(SNOW_DAY_DATES_PATH)
SNOW_DAY_SET = set(SNOW_DAYS["date"].astype(str))


def is_weekday(day: date) -> bool:
    return day.weekday() < 5

SNOW_WEATHER_CODES = {71, 73, 75, 77, 85, 86}
FREEZING_RAIN_CODES = {51, 53, 55, 61, 63, 65, 66, 67}
FIRST_SCHOOL_MORNING_HOURS = range(8)
FREEZING_RAIN_LOOKAHEAD_HOURS = 17


def format_weather_date(value: str | date | datetime) -> str:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        return value.isoformat()
    else:
        parsed = datetime.fromisoformat(value)

    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(ZoneInfo(LOCAL_TIMEZONE))

    return parsed.date().isoformat()


def fetch_weather(
    start_date: str,
    end_date: str,
    lat: float = DEFAULT_LATITUDE,
    lon: float = DEFAULT_LONGITUDE,
    use_forecast: bool = False,
) -> dict:

    if use_forecast:
        url = "https://api.open-meteo.com/v1/forecast"
    else:
        url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": lat,
        "longitude": lon,

        "start_date": start_date,
        "end_date": end_date,

        "daily": ["temperature_2m_min", "wind_gusts_10m_max"],
        "hourly": ["temperature_2m", "dew_point_2m", "precipitation", "snowfall",
                   "weather_code", "wind_speed_10m", "wind_gusts_10m"],

        "timezone": LOCAL_TIMEZONE,
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()


def safe_mean(values):
    values = [value for value in values if value is not None]
    return sum(values) / len(values) if values else 0


def safe_sum(values):
    values = [value for value in values if value is not None]
    return sum(values) if values else 0


def build_hourly_dataframe(hourly: dict) -> pd.DataFrame:
    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"])
    df["date"] = df["time"].dt.date.astype(str)
    return df


def build_daily_dataframe(daily: dict) -> pd.DataFrame:
    df = pd.DataFrame(daily)
    df["date"] = pd.to_datetime(df["time"]).dt.date.astype(str)
    return df.set_index("date")


def build_feature_row(
    day: str,
    hourly: pd.DataFrame,
    daily: pd.Series,
    previous_day_hourly: pd.DataFrame | None = None,
) -> dict:
    hourly = hourly.reset_index(drop=True)
    today_temp = hourly["temperature_2m"].tolist()
    today_precipitation = hourly["precipitation"].tolist()
    today_snow = hourly["snowfall"].tolist()
    today_wind = hourly["wind_speed_10m"].tolist()
    today_wind_gusts = hourly["wind_gusts_10m"].tolist()
    today_dew = hourly["dew_point_2m"].tolist()
    today_weather_code = hourly["weather_code"].tolist()

    previous_snow = (
        previous_day_hourly["snowfall"].tolist()
        if previous_day_hourly is not None
        else []
    )

    snowfall_overnight = safe_sum(today_snow[:8])
    snowfall_24h = safe_sum(today_snow)
    precipitation_overnight = safe_sum(today_precipitation[:8])
    precipitation_24h = safe_sum(today_precipitation)
    temp_min = daily["temperature_2m_min"]

    row = {
        "date": day,
        "snow_day": int(day in SNOW_DAY_SET),
        "snowfall_last_24h": (
            safe_sum(previous_snow[7:]) + snowfall_overnight
            if previous_snow
            else 0
        ),
        "snowfall_last_12h": (
            safe_sum(previous_snow[20:]) + snowfall_overnight
            if previous_snow
            else 0
        ),
        "snowfall_overnight": snowfall_overnight,
        "snowfall_24h": snowfall_24h,
        "precipitation_overnight": precipitation_overnight,
        "precipitation_24h": precipitation_24h,
        "no_snowfall_penalty": (
            2 if snowfall_24h == 0
            else 1 if snowfall_overnight < 1
            else 0
        ),
        "freezing_rain": (
            any(
                code in FREEZING_RAIN_CODES
                for code in today_weather_code[:FREEZING_RAIN_LOOKAHEAD_HOURS]
            )
            and -2 <= temp_min <= 1
        ),
        "temp_min_overnight": temp_min,
        "wind_speed_avg_overnight": safe_mean(today_wind[:8]),
        "wind_gusts_max_overnight": daily["wind_gusts_10m_max"],
        "dewpoint_avg_overnight": safe_mean(today_dew[:8]),
    }

    has_snow_weather_code = any(code in SNOW_WEATHER_CODES for code in today_weather_code)
    for hour in FIRST_SCHOOL_MORNING_HOURS:
        row[f"temperature{hour}"] = today_temp[hour] if hour < len(today_temp) else 0
        row[f"precipitation{hour}"] = (
            today_precipitation[hour] if hour < len(today_precipitation) else 0
        )
        row[f"snowfall{hour}"] = today_snow[hour] if hour < len(today_snow) else 0
        row[f"wind_speed{hour}"] = today_wind[hour] if hour < len(today_wind) else 0
        row[f"wind_gusts{hour}"] = (
            today_wind_gusts[hour] if hour < len(today_wind_gusts) else 0
        )
        row[f"weather_code{hour}"] = has_snow_weather_code

    return row


def weekdays_between(start_day: date, end_day: date):
    current = start_day
    while current <= end_day:
        if is_weekday(current):
            yield current.isoformat()
        current += timedelta(days=1)


def get_data_within_timerange(
    start_date: str,
    end_date: str,
    lat: float = DEFAULT_LATITUDE,
    lon: float = DEFAULT_LONGITUDE,
    use_forecast: bool = False,
) -> pd.DataFrame:

    print("REQUESTING:", start_date, "→", end_date)
    rows = []

    start_date = format_weather_date(start_date)
    end_date = format_weather_date(end_date)
    start_day = date.fromisoformat(start_date)
    end_day = date.fromisoformat(end_date)

    data = fetch_weather(
        start_date,
        end_date,
        lat=lat,
        lon=lon,
        use_forecast=use_forecast,
    )

    hourly_by_date = {
        group_date: group
        for group_date, group in build_hourly_dataframe(data["hourly"]).groupby("date")
    }
    daily_by_date = build_daily_dataframe(data["daily"])
    previous_day_hourly = None

    current_day = start_day
    while current_day <= end_day:
        day = current_day.isoformat()
        hourly = hourly_by_date.get(day)
        if hourly is None or day not in daily_by_date.index:
            current_day += timedelta(days=1)
            continue

        if is_weekday(current_day):
            rows.append(
                build_feature_row(day, hourly, daily_by_date.loc[day], previous_day_hourly)
            )

        previous_day_hourly = hourly
        current_day += timedelta(days=1)

    return pd.DataFrame(rows)


def t() -> pd.DataFrame:
    today = datetime.now(ZoneInfo(LOCAL_TIMEZONE)).date()
    monday = today - timedelta(days=today.weekday())
    friday = monday + timedelta(days=4)

    print(monday.day)
    return get_data_within_timerange(
        monday.isoformat(),
        friday.isoformat(),
        lat=DEFAULT_LATITUDE,
        lon=DEFAULT_LONGITUDE,
        use_forecast=True
    )

def get_this_weeks_data(lat: float = 0, lon: float = 0) -> pd.DataFrame:
    if lat == 0 and lon == 0:
        lat, lon = DEFAULT_LATITUDE, DEFAULT_LONGITUDE

    tz = ZoneInfo(LOCAL_TIMEZONE)
    now = datetime.now(tz)
    today = now.date()

    start = today if now.hour < 7 else today + timedelta(days=1)

    dates = []
    current = start

    while len(dates) < 5:
        if current.weekday() < 5:
            dates.append(current.isoformat())
        current += timedelta(days=1)

    df = get_data_within_timerange(
        dates[0],
        dates[-1],
        lat,
        lon,
        use_forecast=True
    )

    df = df[df["date"].isin(dates)]
    return df.reset_index(drop=True)

def save_to_file(data: pd.DataFrame, filename: str):
    """Save DataFrame to CSV."""
    data.to_csv(filename, index=False)
    print(f"Saved {len(data)} rows to {filename}")


def build_training_dataset(
    start_date: str = "2024-11-15",
    end_date: str = "2026-01-30",
    output_filename: str = "training_dataset_6.csv",
    lat: float = DEFAULT_LATITUDE,
    lon: float = DEFAULT_LONGITUDE,
) -> pd.DataFrame:
    data = get_data_within_timerange(
        start_date,
        end_date,
        lat=lat,
        lon=lon,
    )
    save_to_file(data, str(DATA_DIR / output_filename))
    return data


def main() -> None:
    build_training_dataset()


if __name__ == "__main__":
    main()
