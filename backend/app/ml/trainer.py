import pickle
import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, train_test_split

if __name__ == "__main__" and __package__ is None:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.core.config import DATA_DIR, MODEL_PATH
from app.ml.explainer import get_explanations
from app.services import weather

# ---------------- CONFIG ----------------

BRAIN_CELLS = 100
SEED = 42
TEST_SIZE = 0.3
THRESHOLD = 0.35  # <---- KEY CHANGE (was implicitly 0.5 before)


# ----------------------------------------

def train(data):
    global MODEL

    x = data.drop(columns=["date", "snow_day"])
    y = data["snow_day"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y,
        test_size=TEST_SIZE,
        random_state=SEED,
        stratify=y,
    )

    # 🔍 GRID SEARCH
    param_grid = {
        "n_estimators": [100, 300, 500],
        "max_depth": [None, 6, 10, 15],
        "min_samples_split": [2, 5, 10],
        # removed class_weight from grid → we force balanced
    }

    base_model = RandomForestClassifier(
        random_state=SEED,
        class_weight="balanced"
    )

    grid = GridSearchCV(
        base_model,
        param_grid,
        cv=5,
        scoring="recall",  # snow days matter most
        n_jobs=-1
    )

    grid.fit(x_train, y_train)

    MODEL = grid.best_estimator_

    # with open(MODEL_PATH, "wb") as f:
    #     pickle.dump(MODEL, f)

    print("BEST MODEL SETTINGS:")
    print(grid.best_params_)
    print()

    # ---------------- EVALUATION ----------------

    probs = MODEL.predict_proba(x_test)[:, 1]
    y_pred = (probs >= THRESHOLD).astype(int)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Snow Day Recall:", recall_score(y_test, y_pred))
    print("Snow Day Precision:", precision_score(y_test, y_pred))
    print()

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    print(f"Predicted {tn}/{tn + fp} non-snow days")
    print(f"Predicted {tp}/{tp + fn} snow days")
    print()


def print_feature_importance(data):
    importances = MODEL.feature_importances_

    features = data.drop(columns=["date", "snow_day"]).columns
    importance_df = pd.DataFrame({
        "feature": features,
        "importance": importances
    }).sort_values(by="importance", ascending=False)

    print("\nTOP FACTORS THE MODEL USES:")
    for _, row in importance_df.head(8).iterrows():
        print(f"- {row['feature']}")


def test(data):
    X = data.drop(columns=["date", "snow_day"])

    with open(MODEL_PATH, "rb") as f:
        MODEL = pickle.load(f)

    all_explanations = get_explanations(X, MODEL)

    probs = MODEL.predict_proba(X)[:, 1]

    results = data.copy()
    results["snow_day_probability"] = probs

    print("SNOW DAY ODDS\n")

    for i, row in results.iterrows():
        weekday = pd.to_datetime(row["date"]).day_name()

        odds = row["snow_day_probability"] * 100

        print(
            f"{row['date']} ({weekday}) → {odds:.1f}% chance of snow day")

        explanations = all_explanations[i]

        explanation_list = [
            {"explanation": explanation["humanized_value"] + ("+" if explanation["direction"] == "up" else "-")}
            for explanation in explanations
        ]

        print("  Top factors:")
        print(" ", explanation_list)
        print()

def add_predictions(data):
    X = data.drop(columns=["date", "snow_day"])

    with open(MODEL_PATH, "rb") as f:
        MODEL = pickle.load(f)

    probs = MODEL.predict_proba(X)[:, 1]

    data["prob"] = (probs * 100).round().astype(int)

    data.to_csv(DATA_DIR / "training_dataset_7.csv", index=False)


def load_training_data(filename: str = "training_dataset_1.csv") -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / filename)


def main() -> None:
    training_data = load_training_data()
    train(training_data)
    print_feature_importance(training_data)


if __name__ == "__main__":
    main()
