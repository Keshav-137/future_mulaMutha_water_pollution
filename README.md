# 🌊 Mula-Mutha River Pollution Dataset Generator & Predictor

A Python-based **synthetic water-pollution dataset generation and prediction system** for the Mula-Mutha River system in **Pune, Maharashtra**.

This project generates structured seasonal pollution data across geographically ordered monitoring locations and provides a simple forecasting model to estimate pollution levels for the following year. The generated data is designed for **machine learning experimentation, data visualization, interactive maps, dashboards, and backend API development**.

> ⚠️ **Important:** This project generates synthetic data. The values are designed to represent realistic pollution patterns for development and experimentation and are **not actual measurements from the Mula-Mutha River**.

---

## 🚀 Features

* 📍 **10 geographically ordered monitoring locations**
* 📅 Historical dataset covering **2020–2026**
* 🌦️ Four seasonal categories:

  * Monsoon
  * Post-Monsoon
  * Winter
  * Summer
* 💧 Models seasonal water-flow dilution effects
* 🏭 Models downstream pollution accumulation
* 🌊 Simulates dilution around river-confluence locations
* 📈 Generates pollution trends over multiple years
* 🔮 Predicts pollution levels for **2027**
* 📊 Exports data in CSV and JSON formats
* 🗺️ Provides location metadata for map-based visualization
* 🔌 Designed for Flask/FastAPI backend integration
* 🎚️ Suitable for interactive year sliders and seasonal filters

---

## 🧠 Modeling Approach

The dataset generator incorporates two major environmental patterns.

### 1. Seasonal Dilution

River pollution concentration changes depending on seasonal water flow.

During the **Monsoon**, increased rainfall and river discharge can dilute pollutants, resulting in lower simulated concentration levels.

During **Summer**, lower water flow can result in higher pollutant concentrations.

Conceptually:

```text
High River Flow
      ↓
More Dilution
      ↓
Lower Pollution Concentration
```

and:

```text
Low River Flow
      ↓
Less Dilution
      ↓
Higher Pollution Concentration
```

---

### 2. Downstream Pollution Accumulation

As the river moves through urban areas, additional pollution sources are modeled along the river.

The simulation therefore generally follows:

```text
Upstream
   ↓
Monitoring Point 1
   ↓
Monitoring Point 2
   ↓
Urban / Industrial Areas
   ↓
Monitoring Point 3
   ↓
...
   ↓
Downstream
```

Pollution generally increases downstream as additional discharge sources are introduced.

At selected river-confluence locations, a temporary reduction is modeled to represent the effect of additional freshwater volume and dilution.

---

## 🔮 Prediction Model

The project includes a simple **per-location, per-season linear trend model**.

Historical pollution values from **2020–2026** are used to estimate the pollution level for **2027**.

The basic concept is:

```text
Historical Pollution Data
          ↓
Location + Season
          ↓
Linear Trend Analysis
          ↓
2027 Pollution Prediction
```

This approach is intentionally simple so that the generated predictions can easily be integrated into a visualization or application.

---

## 📂 Project Output

Running the generator produces the following files:

```text
output/
│
├── mula_mutha_pollution_2020_2026.csv
├── mula_mutha_pollution_2020_2026.json
├── mula_mutha_prediction_2027.csv
└── mula_mutha_locations.json
```

### `mula_mutha_pollution_2020_2026.csv`

Contains the complete historical synthetic dataset in **long-format CSV**.

Example structure:

```text
Year,Season,Location,Pollution_Level,...
2020,Monsoon,Location_1,...
2020,Winter,Location_1,...
2020,Summer,Location_1,...
...
```

---

### `mula_mutha_pollution_2020_2026.json`

Contains the same pollution data in a nested JSON structure organized by:

```text
Location
    └── Season
          └── Year
                └── Pollution Data
```

This format is useful for directly serving data to frontend applications.

---

### `mula_mutha_prediction_2027.csv`

Contains the predicted pollution values for 2027 for each monitoring location and season.

This file can be used to display forecast information on dashboards and maps.

---

### `mula_mutha_locations.json`

Contains metadata for the monitoring locations.

This can be used to place monitoring points on an interactive map.

Example structure:

```json
{
    "location": "Monitoring Point 1",
    "latitude": 18.0000,
    "longitude": 73.0000
}
```

---

## 🗺️ Application Use Case

The generated dataset can be connected to an interactive pollution-monitoring application.

A possible frontend workflow is:

```text
                ┌─────────────────────┐
                │  Pollution Dataset  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Flask / FastAPI  │
                │       Backend       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Web / Flutter    │
                │     Frontend        │
                └──────────┬──────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Map View      Year Slider   Season Filter
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                  Pollution Forecast
```

Users can select a particular **year and season** and visualize pollution conditions across different monitoring locations.

The 2027 prediction dataset can be used to display a forecast layer on the map.

---

## 🛠️ Technology Stack

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **CSV**
* **JSON**
* **Flask / FastAPI** *(optional backend integration)*
* **Map-based visualization** *(frontend integration)*

---

## 📋 Requirements

Python 3.9+ is recommended.

Install the required dependencies:

```bash
pip install pandas numpy scikit-learn
```

---

## ▶️ Running the Project

Clone the repository:

```bash
git clone <your-repository-url>
```

Navigate into the project:

```bash
cd <repository-name>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dataset generator:

```bash
python main.py
```

The generated files will be saved inside:

```text
output/
```

---

## 📊 Dataset Structure

The project is designed around the following dimensions:

| Dimension            | Coverage   |
| -------------------- | ---------- |
| Monitoring Locations | 10         |
| Years                | 2020–2026  |
| Prediction Year      | 2027       |
| Seasons              | 4          |
| Data Type            | Synthetic  |
| Historical Format    | CSV + JSON |
| Prediction Format    | CSV        |
| Location Format      | JSON       |

---

## 🔬 Why Synthetic Data?

Obtaining continuous, location-specific, seasonal water-quality measurements over several years can be difficult.

This project provides a controlled dataset for:

* Testing ML pipelines
* Developing dashboards
* Testing APIs
* Building map visualizations
* Developing frontend applications
* Testing time-series workflows
* Prototyping pollution prediction systems
* Demonstrating environmental-data applications

The synthetic generation process allows the same environmental patterns to be reproduced consistently during development.

---

## 🔌 Backend Integration

The generated JSON files can be served through a REST API using Flask or FastAPI.

For example:

```text
GET /api/pollution
GET /api/pollution?year=2025
GET /api/pollution?season=Monsoon
GET /api/prediction/2027
GET /api/locations
```

A frontend can then request the required data dynamically.

---

## 📱 Frontend Integration

The dataset can support an interface containing:

### Year Selection

```text
2020 ────────────────●──── 2026
```

### Season Selection

```text
[ Monsoon ] [ Post-Monsoon ] [ Winter ] [ Summer ]
```

### Map Visualization

```text
          Upstream
             ●
             │
             │
          ●  │
             │
        ●────┤
             │
          ●  │
             │
          ●  │
             │
          Downstream
```

Each monitoring point can display its corresponding pollution value.

---

## 📈 Future Improvements

Possible future extensions include:

* Real-world water-quality datasets
* More monitoring locations
* Real-time sensor integration
* Rainfall and river-discharge data
* Temperature and weather features
* Multiple water-quality parameters such as:

  * pH
  * BOD
  * COD
  * DO
  * TDS
  * Turbidity
  * Nitrate
  * Phosphate
* Advanced time-series models
* XGBoost/LightGBM forecasting
* LSTM/GRU-based prediction
* Pollution-risk classification
* Real-time pollution alerts
* Interactive GIS visualization
* Mobile application integration

---

## ⚠️ Limitations

This project is intended for **prototyping and experimentation**.

The generated values:

* Are synthetic
* Are not official environmental measurements
* Should not be used for environmental policy decisions
* Should not be interpreted as actual pollution readings
* Should be replaced with validated field or government data for real-world deployment

The prediction model is also a baseline forecasting approach and can be improved using real historical measurements and additional environmental variables.

---

## 📁 Suggested Repository Structure

```text
mula-mutha-pollution-predictor/
│
├── main.py
├── requirements.txt
├── README.md
│
├── output/
│   ├── mula_mutha_pollution_2020_2026.csv
│   ├── mula_mutha_pollution_2020_2026.json
│   ├── mula_mutha_prediction_2027.csv
│   └── mula_mutha_locations.json
│
└── .gitignore
```

---

## 🎯 Project Objective

The primary objective of this project is to create a **structured environmental-data simulation and prediction pipeline** that can serve as the foundation for an interactive river-pollution monitoring system.

It combines **seasonal modeling, geographical pollution patterns, historical trends, data generation, and forecasting** into a reusable dataset pipeline suitable for ML and application development.

---

## 👨‍💻 Author

**Keshav Sonawane**

Developed as a data/ML experimentation project focused on environmental monitoring, prediction, and visualization.

---

## ⭐ Contributions

Contributions, suggestions, and improvements are welcome.

If you have ideas for improving the pollution-generation logic, prediction model, dataset structure, visualization, or API integration, feel free to open an issue or submit a pull request.

---

## 📜 License

This project is intended for educational, research, and development purposes. Add an appropriate open-source license to the repository if you plan to distribute or reuse the project publicly.
