# ❄️ Snow Day Predictor

Snow Day Predictor is a machine learning project that predicts the probability of school cancellations caused by winter weather in Ontario.

The project combines historical school cancellation data with historical and forecast weather data to train a model capable of estimating the probability of a snow day based on upcoming conditions.

## Current Project

The current prediction system uses a **Random Forest classifier** trained on historical weather and cancellation data.

Weather data is retrieved from the **Open-Meteo API**. Along with the raw forecast, the backend calculates additional features such as overnight snowfall, snow accumulation, average and minimum temperatures, wind speed, visibility, and other conditions leading into the school day.

The model returns a probability rather than a simple yes/no prediction.

### Current Stack

**Frontend**

* HTML
* CSS
* JavaScript

**Backend / ML**

* Python
* scikit-learn
* Random Forest classifier
* Open-Meteo API

The current site was originally built as a relatively simple interface around the prediction model. Most of the development so far has focused on building the data pipeline, experimenting with weather features, training the model, and getting the complete prediction system working.

---

## November 2026 Rebuild

Beginning in **November 2026**, Snow Day Predictor will receive a major rebuild for the 2026–27 winter season.

A major part of this will be replacing the existing HTML/CSS/JavaScript frontend with **Next.js, TypeScript, and Tailwind CSS**.

The goal is to turn the current proof-of-concept-style frontend into a more polished application while continuing to improve the underlying prediction system.

### Planned Stack

**Frontend**

* Next.js
* React
* TypeScript
* Tailwind CSS
* shadcn/ui

**Backend / ML**

* Python
* scikit-learn
* Open-Meteo
* Region-specific prediction models

The frontend and prediction backend will remain separate, allowing the ML system to be developed independently from the website.

---

## Planned Features

The November 2026 rebuild is planned to include:

* Region-specific models for different areas of Ontario
* Prediction confidence estimates
* Improved explanations for model predictions
* Predictions for multiple upcoming school days
* Environment Canada weather alerts
* Location-specific pages
* Community agree/disagree voting
* Previous prediction and accuracy tracking
* Comparison with other snow day predictors
* PWA/installable web app support
* A completely redesigned weather-focused interface

The exact feature set may change as the rebuild progresses.

---

## Project Goals

Snow Day Predictor is both a practical application and an ongoing machine learning project.

Development is focused on improving three areas:

1. **Prediction accuracy** — improving training data, feature engineering, and regional modelling.
2. **Transparency** — making it clear why the model produced a prediction and how confident that prediction is.
3. **Usability** — rebuilding the website into a fast, modern interface that makes the important information immediately accessible.

The next major version is planned to begin rolling out in **November 2026**.
