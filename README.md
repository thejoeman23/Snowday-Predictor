# ❄️ Snow Day Predictor

A machine-learning-powered snow day prediction tool built for Ontario students.

Snow Day Predictor uses historical weather and school cancellation data alongside upcoming weather forecasts to estimate the probability that school will be cancelled due to winter weather.

Rather than relying on a simple set of rules like *"X cm of snow = snow day,"* the project uses machine learning to learn from previous snow days and determine how combinations of snowfall, temperature, wind, visibility, and other conditions affect the likelihood of a cancellation.

> **Major redesign coming November 2026.**
> Snow Day Predictor is being rebuilt for the 2026–27 winter season with improved models, a completely redesigned interface, regional predictions, confidence estimates, community predictions, and accuracy tracking.

---

## What It Does Today

The current version of Snow Day Predictor provides a percentage estimate of the likelihood of a snow day based on forecast weather conditions.

### Machine Learning

The prediction system currently uses a **Random Forest classifier** trained using historical weather conditions and known school cancellation data.

Instead of returning only `snow day` or `no snow day`, the model returns a probability:

```text
Snow Day Probability: 72%
```

This makes the prediction much more useful when conditions are uncertain or borderline.

### Weather Data

Weather information is sourced from **Open-Meteo**, including both historical observations and forecast data.

The model considers conditions such as:

* Snowfall
* Snow accumulation
* Temperature
* Minimum temperature
* Wind speed
* Visibility
* Precipitation type
* Overnight weather conditions

Additional features are calculated from the raw hourly weather data, including:

* Overnight snowfall totals
* 24-hour snow accumulation
* Overnight average temperature
* Overnight minimum temperature
* Rolling weather windows

These features allow the model to consider the overall conditions leading into a school morning rather than relying on a single forecast value.

### Prediction Explanations

The predictor also examines the factors contributing to its prediction so users aren't given a percentage with no context.

The goal is not just to answer:

> **"Will tomorrow be a snow day?"**

but also:

> **"Why does the model think that?"**

---

# 🚧 November 2026 Update

Snow Day Predictor is undergoing a major redesign planned to begin rolling out in **November 2026**, in time for the 2026–27 Ontario winter season.

The update expands the project from a simple ML prediction interface into a much more complete snow-day forecasting tool.

## Regional Models

Ontario is huge, and school cancellations don't work the same way everywhere.

Different regions experience different:

* amounts of snowfall
* winter temperatures
* road conditions
* cancellation policies
* tolerances for severe weather

The new system will therefore move toward **region-specific machine learning models** trained using weather and cancellation data relevant to each area.

A storm that is unusual enough to cancel buses in one part of Ontario may be completely normal somewhere else.

Regional models should allow the predictor to account for that.

---

## Prediction Confidence

Alongside the snow day probability, predictions will include an estimate of how confident the model is in that prediction.

For example:

```text
78%
Chance of a Snow Day

High Confidence
```

This helps distinguish between predictions where the model sees a strong historical pattern and predictions where conditions are unusually difficult to classify.

---

## Completely Redesigned Website

The frontend will be rebuilt with **Next.js** and a new weather-focused interface inspired by the simplicity and information density of modern weather apps.

The prediction will remain the most important element on the page, while additional information will be available without overwhelming the user.

Planned elements include:

* Snow day probability
* Model confidence
* Hourly weather conditions
* Explanation of important prediction factors
* Future snow day probabilities
* Environment Canada weather warnings
* Regional information
* Location-specific pages
* Improved loading and navigation

The redesign is intended to make the site feel less like an ML demo and more like a polished weather product.

---

## Future Predictions

Instead of only predicting the next school day, the redesigned site will show upcoming possibilities as the forecast develops.

Because weather forecasts become less reliable farther into the future, longer-range predictions may be represented as ranges rather than misleadingly precise percentages.

For example:

```text
Monday       8%
Tuesday      25–40%
Wednesday    45–70%
```

Predictions can become more precise as the date approaches and better forecast data becomes available.

---

## Environment Canada Alerts

Relevant **Environment and Climate Change Canada** weather warnings will be surfaced directly alongside predictions.

This will provide additional context when major winter weather events are approaching, such as:

* Snowfall warnings
* Winter storm warnings
* Freezing rain warnings
* Blizzard warnings
* Extreme cold warnings

The machine-learning prediction remains separate from official government weather information.

---

## Community Predictions

Users will be able to compare their own intuition against the model.

After seeing a prediction, users may be able to vote on whether they think the model is right:

```text
AI Prediction
72%

Do you agree?

[ 👍 Yes ]    [ 👎 No ]
```

The following day, users can report whether their school actually had a snow day.

This creates a simple feedback loop while also making it possible to compare the model with the collective prediction of students using the site.

---

## Prediction Scoreboard

The redesign will introduce accuracy tracking so predictions can be judged by what actually happened.

Recent predictions will be recorded and compared against their outcomes.

A scoreboard may compare:

* Snow Day Predictor
* Other public snow day prediction services
* Community predictions
* Actual outcomes

Recent performance and prediction streaks will make the model's accuracy visible instead of simply claiming that it works.

---

## Installable Web App

The redesigned site is planned to work as a **Progressive Web App (PWA)**.

Users will be able to install Snow Day Predictor to their device and use it more like a dedicated weather app while keeping the project web-based.

Additional platform features, including widgets, are also being explored.

---

# Project Philosophy

Snow Day Predictor started as an experiment:

> **Can historical weather and cancellation data actually be used to predict snow days with machine learning?**

The project has since grown into an attempt to build a genuinely useful forecasting tool around that model.

The November 2026 update keeps the same core idea: **give students one useful number — their chance of a snow day — and make the reasoning and uncertainty behind that number understandable.**

No magic. No guaranteed snow days.

Just weather data, historical cancellations, and a model making its best prediction.

---

## Status

🟢 **Current predictor:** Functional
🧠 **Machine learning model:** Functional
🌦️ **Forecast integration:** Functional
🎨 **New frontend:** Planned
📍 **Regional models:** Planned
📊 **Confidence + accuracy tracking:** Planned
👥 **Community predictions:** Planned
📱 **PWA:** Planned

**Major update targeted for November 2026.**
