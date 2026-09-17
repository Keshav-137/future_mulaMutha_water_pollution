"""
Mula-Mutha River Pollution Dataset Generator & Predictor
==========================================================
Generates a synthetic (but realistic) seasonal water-pollution dataset
for the Mula-Mutha river system (Pune, Maharashtra) covering:

  - 10 geographically ordered monitoring points, from the upstream
    source down to the confluence / downstream exit
  - 4 seasons: Monsoon, Post-Monsoon, Winter, Summer
  - Years: 2020 - 2026

Two real-world effects are built into the model:
  1. Seasonal dilution -> pollution drops sharply during Monsoon
     (high river flow dilutes effluent) and rises in Summer (lowest
     flow -> highest concentration).
  2. Downstream accumulation -> pollution generally rises as the
     river passes through the city (more sewage/industrial discharge
     joins in), with a brief natural dip right at river-confluence
     points (extra fresh water volume dilutes it).

A simple per-location, per-season linear trend model is also included
to *predict* the next year's pollution level -- exactly what you need
to drive a "drag the season / scrub the year" front-end and show a
forecast on a map.

Output files (written to ./output by default):
  - mula_mutha_pollution_2020_2026.csv   -> full dataset, long format
  - mula_mutha_pollution_2020_2026.json  -> same data, nested by
                                             location -> season -> year
  - mula_mutha_prediction_2027.csv       -> predicted next-year values
  - mula_mutha_locations.json            -> location metadata (for map)

Import this module in a Flask/FastAPI backend and serve the JSON to a
slider/scrubber UI, or just read the CSVs into any charting library.
"""

import json
import csv
import os

import numpy as np


# ----------------------------------------------------------------------
# 1. CONFIGURATION
# ----------------------------------------------------------------------

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

YEARS = list(range(2020, 2027))          # 2020 .. 2026
SEASONS = ["Monsoon", "Post-Monsoon", "Winter", "Summer"]

# Seasonal multiplier applied to the base pollution load.
# Monsoon dilutes pollution the most (lowest multiplier); summer
# concentrates it the most (highest multiplier).
SEASON_MULTIPLIER = {
    "Monsoon":      0.45,   # heavy dilution / "monsoon cleaning"
    "Post-Monsoon": 0.70,   # river still has decent flow
    "Winter":       0.95,   # flow drops, pollution creeps back up
    "Summer":       1.25,   # lowest flow -> highest concentration
}

# 10 geographically ordered points, upstream -> downstream.
# distance_km is cumulative distance from the source.
# base_pollution dips at confluence points because extra water volume
# joining the river dilutes concentration right there.
LOCATIONS = [
    dict(id=1,  name="Mulshi Dam (Mula Source)",                       distance_km=0,  base_pollution=8),
    dict(id=2,  name="Pashan Lake Inflow",                             distance_km=8,  base_pollution=15),
    dict(id=3,  name="Aundh",                                          distance_km=14, base_pollution=28),
    dict(id=4,  name="Bopodi",                                         distance_km=18, base_pollution=38),
    dict(id=5,  name="Sangam Bridge (Mula-Mutha Confluence)",          distance_km=21, base_pollution=30),
    dict(id=6,  name="Bund Garden",                                    distance_km=24, base_pollution=45),
    dict(id=7,  name="Mundhwa",                                        distance_km=29, base_pollution=58),
    dict(id=8,  name="Kharadi",                                        distance_km=34, base_pollution=66),
    dict(id=9,  name="Fursungi / Manjari",                             distance_km=41, base_pollution=74),
    dict(id=10, name="Confluence with Bhima River (Downstream Exit)",  distance_km=52, base_pollution=60),
]


def year_trend_factor(year: int) -> float:
    """
    Rising city effluent load (~3%/yr) pulls pollution up each year;
    from 2023 onward Pune's new STPs (sewage treatment plants) start
    clawing some of that back down -- a realistic policy effect.
    """
    growth = 1 + 0.03 * (year - 2020)
    stp_relief = 1 - 0.02 * (year - 2022) if year >= 2023 else 1.0
    return growth * stp_relief


def compute_sub_parameters(wpi: float):
    """
    Derive illustrative raw water-quality parameters from a single
    composite pollution index (WPI, 0-100, higher = worse) so the
    dataset feels like a real monitoring sheet.
    """
    bod = round(2 + wpi * 0.55 + np.random.normal(0, 1.5), 2)                   # mg/L
    cod = round(bod * 2.6 + np.random.normal(0, 2), 2)                          # mg/L
    do = round(max(0.5, 8.5 - wpi * 0.07 + np.random.normal(0, 0.3)), 2)        # mg/L
    fecal_coliform = int(max(50, (wpi ** 2) * 8 + np.random.normal(0, 500)))    # MPN/100ml
    ph = round(7.4 - wpi * 0.01 + np.random.normal(0, 0.1), 2)
    nitrate = round(1 + wpi * 0.12 + np.random.normal(0, 0.5), 2)               # mg/L
    return dict(BOD_mgL=bod, COD_mgL=cod, DO_mgL=do,
                FecalColiform_MPN100ml=fecal_coliform,
                pH=ph, Nitrate_mgL=nitrate)


# ----------------------------------------------------------------------
# 2. DATA GENERATION
# ----------------------------------------------------------------------

def generate_dataset():
    rows = []
    for loc in LOCATIONS:
        for year in YEARS:
            for season in SEASONS:
                base = loc["base_pollution"]
                season_mult = SEASON_MULTIPLIER[season]
                trend = year_trend_factor(year)
                noise = np.random.normal(0, 2.5)

                wpi = base * season_mult * trend + noise
                wpi = float(np.clip(wpi, 2, 98))  # keep on a 0-100 scale

                sub = compute_sub_parameters(wpi)

                rows.append({
                    "Year": year,
                    "Season": season,
                    "Location_ID": loc["id"],
                    "Location_Name": loc["name"],
                    "Distance_km": loc["distance_km"],
                    "WPI": round(wpi, 2),
                    **sub,
                })
    return rows


# ----------------------------------------------------------------------
# 3. NEXT-YEAR PREDICTION (simple linear trend per location & season)
# ----------------------------------------------------------------------

def predict_next_year(rows, target_year=2027):
    """
    Fits a simple linear regression (numpy polyfit, degree 1) on the
    WPI series of every (location, season) pair across YEARS, and uses
    it to forecast `target_year`. No extra dependencies needed to
    drive a "predicted next year" view in the UI.
    """
    predictions = []
    by_key = {}
    for r in rows:
        key = (r["Location_ID"], r["Season"])
        by_key.setdefault(key, []).append((r["Year"], r["WPI"]))

    for (loc_id, season), series in by_key.items():
        series.sort()
        xs = np.array([p[0] for p in series])
        ys = np.array([p[1] for p in series])

        slope, intercept = np.polyfit(xs, ys, 1)
        predicted_wpi = float(np.clip(slope * target_year + intercept, 2, 98))

        loc_name = next(l["name"] for l in LOCATIONS if l["id"] == loc_id)
        distance = next(l["distance_km"] for l in LOCATIONS if l["id"] == loc_id)

        trend_label = (
            "worsening" if slope > 0.15 else
            "improving" if slope < -0.15 else
            "stable"
        )

        predictions.append({
            "Year": target_year,
            "Season": season,
            "Location_ID": loc_id,
            "Location_Name": loc_name,
            "Distance_km": distance,
            "Predicted_WPI": round(predicted_wpi, 2),
            "Trend_per_year": round(float(slope), 3),
            "Trend_label": trend_label,
        })
    return predictions


def summarize_downstream_pattern(rows, year, season):
    """
    Returns the pollution profile along the river for one year+season,
    ordered source -> downstream, flagging points where pollution
    *drops* compared to the point just upstream of it (e.g. right
    after a confluence).
    """
    subset = [r for r in rows if r["Year"] == year and r["Season"] == season]
    subset.sort(key=lambda r: r["Distance_km"])

    profile = []
    prev_wpi = None
    for r in subset:
        change = None if prev_wpi is None else round(r["WPI"] - prev_wpi, 2)
        profile.append({
            "Location_Name": r["Location_Name"],
            "Distance_km": r["Distance_km"],
            "WPI": r["WPI"],
            "Change_vs_upstream": change,
            "Direction": (
                "start" if change is None else
                "reduces here" if change < 0 else
                "increases here"
            )
        })
        prev_wpi = r["WPI"]
    return profile


# ----------------------------------------------------------------------
# 4. EXPORT
# ----------------------------------------------------------------------

def export_all(output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    rows = generate_dataset()
    predictions = predict_next_year(rows, target_year=2027)

    # ---- CSV: main dataset (long format, great for a slider/scrubber UI)
    csv_path = os.path.join(output_dir, "mula_mutha_pollution_2020_2026.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # ---- JSON: nested by location -> season -> year (fast lookups for UI)
    nested = {}
    for r in rows:
        loc = nested.setdefault(r["Location_Name"], {})
        season = loc.setdefault(r["Season"], {})
        season[str(r["Year"])] = {k: v for k, v in r.items()
                                   if k not in ("Location_Name", "Season", "Year")}
    json_path = os.path.join(output_dir, "mula_mutha_pollution_2020_2026.json")
    with open(json_path, "w") as f:
        json.dump(nested, f, indent=2)

    # ---- CSV: 2027 prediction
    pred_path = os.path.join(output_dir, "mula_mutha_prediction_2027.csv")
    with open(pred_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(predictions[0].keys()))
        writer.writeheader()
        writer.writerows(predictions)

    # ---- JSON: location metadata (for plotting a map / route line)
    loc_path = os.path.join(output_dir, "mula_mutha_locations.json")
    with open(loc_path, "w") as f:
        json.dump(LOCATIONS, f, indent=2)

    print(f"Generated {len(rows)} rows -> {csv_path}")
    print(f"Nested JSON             -> {json_path}")
    print(f"2027 predictions        -> {pred_path}")
    print(f"Location metadata       -> {loc_path}")

    return rows, predictions


# ----------------------------------------------------------------------
# 5. QUICK CLI DEMO
# ----------------------------------------------------------------------

if __name__ == "__main__":
    rows, predictions = export_all()

    print("\nDownstream pollution profile, Monsoon 2026 (dilution effect):")
    for p in summarize_downstream_pattern(rows, 2026, "Monsoon"):
        print(f"  {p['Location_Name']:<45} WPI={p['WPI']:<6} {p['Direction']}")

    print("\nDownstream pollution profile, Summer 2026 (accumulation effect):")
    for p in summarize_downstream_pattern(rows, 2026, "Summer"):
        print(f"  {p['Location_Name']:<45} WPI={p['WPI']:<6} {p['Direction']}")

    print("\n2027 predictions (Summer season):")
    for p in [x for x in predictions if x["Season"] == "Summer"]:
        print(f"  {p['Location_Name']:<45} predicted WPI={p['Predicted_WPI']:<6} ({p['Trend_label']})")
