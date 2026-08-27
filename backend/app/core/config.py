from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

SNOW_DAY_DATES_PATH = DATA_DIR / "snow_day_dates.csv"
MODEL_PATH = MODELS_DIR / "snow_day_random_forest.pkl"

DEFAULT_LATITUDE = 44.569
DEFAULT_LONGITUDE = -80.98
LOCAL_TIMEZONE = "America/Toronto"

CORS_ORIGINS = [
    "https://snowdaypredictor.io",
    "http://127.0.0.1:5500",
    "http://192.168.2.129:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
