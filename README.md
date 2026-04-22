# HimClimX (Monorepo)


# 🏔️ Himalayan Climate Analytics Dashboard (HimClimX)
Dynamic Dashboard For Himalayan Climate Monitoring
<img width="1919" height="951" alt="image" src="https://github.com/user-attachments/assets/0d6f1de4-e557-4ba5-8678-23c3be8e0033" />
<img width="1915" height="905" alt="image" src="https://github.com/user-attachments/assets/cdd9c7b3-5397-4624-a383-0f33d39ff446" />


A futuristic, research-grade web dashboard for visualizing climate change across the **Himalayan region** from **1901 to 2024**, powered by real NetCDF datasets.  
Interactively explore regional trends in temperature, precipitation, cloud cover, and more using time-series, decadal analysis, and statistical insights — all **hosted for free on GitHub Pages**.

---

## 🔍 Features

- 🌐 **Interactive Leaflet Map** with Himalayan zones
- 📈 **Plotly.js Charts** for:
  - Long-term trends
  - Linear regression
  - Seasonal & decadal comparisons
- 🧊 Real-world **climate data** extracted from NetCDF files
- 🎛️ Dynamic controls for:
  - Variable selection
  - Region/elevation filters
  - Time window selection
  - Analysis method (trend, anomaly, etc.)
- 💾 Export data to CSV
- ⚡ No backend needed – runs fully client-side

---

## 📊 Climate Variables

| Code | Full Name                         | Unit         |
|------|----------------------------------|--------------|
| TMP  | Mean Temperature                 | °C           |
| TMX  | Maximum Temperature              | °C           |
| TMN  | Minimum Temperature              | °C           |
| PRE  | Precipitation                    | mm/month     |
| CLD  | Cloud Cover                      | %            |
| DTR  | Diurnal Temperature Range        | °C           |
| WET  | Wet Days Frequency               | days/month   |
| VAP  | Vapor Pressure                   | hPa          |
| PET  | Potential Evapotranspiration     | mm/month     |
| FRS  | Frost Day Frequency              | days/month   |

> 📌 Data spans across elevation bands and Himalayan subregions.

---

## 🎥 Demo Preview
<!--
| 🗺️ Interactive Map | 📈 Trend Line | 📊 Seasonal Chart |
|-------------------|---------------|-------------------|
| ![](./assets/demo-map.png) | ![](./assets/demo-trend.png) | ![](./assets/demo-seasonal.png) |

### 📹 Video Walkthrough
[![Watch the video](https://img.youtube.com/vi/YOUR_VIDEO_ID/hqdefault.jpg)](https://youtube.com/watch?v=YOUR_VIDEO_ID)

---
-->
## 📂 Data Structure

All data lives inside the `data/` folder as static JSON:
data/
- TMP_1990-2024_central_high.json
- PRE_1990-2024_all.json
- himalaya_regions.geojson


Each JSON file contains:
- `years`: array of years
- `values`: array of corresponding measurements

---

## 🚀 Hosting It Yourself (Free on GitHub Pages)

1. Fork or clone this repo
2. Replace/add your data in `data/` folder
3. Commit `index.html` and all assets
4. Go to GitHub:
   - Settings → Pages → Source: `main` → `/ (root)`
5. Done! Your dashboard will be live at: https://<your-username>.github.io/himalayan-dashboard/


## 🧪 How It Works

- 📜 NetCDF files are sliced using Python (xarray)
- 🔁 JSON outputs are generated for each variable/region combo
- 🧠 HTML dashboard dynamically loads and visualizes the data
- No backend. No server. Everything runs in the browser.

---

## ⚙️ Tech Stack

- ⚛️ Vanilla HTML + JS + CSS
- 📍 [Leaflet.js](https://leafletjs.com) — Map rendering
- 📊 [Plotly.js](https://plotly.com/javascript/) — Interactive graphs
- 🧪 Python (`xarray`, `netCDF4`) — Data conversion
- ☁️ [GitHub Pages](https://pages.github.com/) — Free hosting

---




![CI](https://github.com/AmanDoesntCode/HimClimX/actions/workflows/ci.yml/badge.svg?branch=dev)
