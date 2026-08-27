import pickle

from app.core.config import MODEL_PATH

if not MODEL_PATH.exists():
    raise RuntimeError(f"{MODEL_PATH.name} not found; deployment is misconfigured")

with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)
