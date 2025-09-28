# 🌐 HimClimX API Overview

Welcome to the **Phase 1 HimClimX Backend API**.  
This API exposes climate analysis features for Himalayan regions.  

---

## ✅ Health Check
**GET** `/health`  
Verify the server is alive.

Response:
```json
{"status": "ok"}

📊 Metadata

#Variables

GET /meta/variables → list of supported climate variables.

Response:

[
  {"id": "tavg", "name": "Average Temperature", "units": "°C"},
  {"id": "prcp", "name": "Precipitation", "units": "mm"}
]

#Regions

GET /meta/regions → list of supported regions with bounding boxes.

Response:

[
  {"id": "L1", "name": "Ladakh", "bbox": [76.0, 32.0, 79.5, 35.2]}
]

📈 Analysis

POST /analyze
Run statistical analysis.

Request:

{
  "variable_id": "tavg",
  "region_id": "L1",
  "time_range": {"start": "2023-01-01", "end": "2024-12-31"},
  "options": ["trend", "quality"]
}

Response:

{
  "mean": 10.9,
  "std": 0.6,
  "trend_per_decade": 0.9,
  "pct_change": 19.0,
  "count": 24,
  "series_sample": [["2023-01-01", 10.0]],
  "quality": {"overall": 0.98}
}

🔮 Forecast

POST /forecast
Get a stub forecast.

Request:

{
  "variable_id": "tavg",
  "region_id": "L1",
  "horizon_years": 3
}

Response:

{
  "points": [
    {"date": "2026-01-01", "yhat": 12.05}
  ]
}
