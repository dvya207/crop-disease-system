# 🌿 AI Crop Disease Detection System

An AI-powered web application that detects crop diseases from leaf images using deep learning, provides severity analysis, live weather data, and smart agricultural recommendations.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)


## Features

- 🧠 **CNN-based disease detection** for 5 crops (Cotton, Rice, Maize, Wheat, Sugarcane)
- 📊 **Severity analysis** — Low / Medium / High
- 🌦️ **Live weather** via OpenWeatherMap API
- 🧪 **Soil analysis** — pH, NPK, Moisture-based recommendations
- 💊 **Treatment recommendations** based on disease category
- 🌾 **Next crop suggestions** based on soil condition


## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Uvicorn |
| ML | TensorFlow / Keras (.h5 models) |
| Image Processing | OpenCV + Pillow |
| Templating | Jinja2 |
| Weather API | OpenWeatherMap |
| Frontend | HTML + CSS (Jinja2 templates) |

## Project Structure
📁 crop_disease_system
├── 📁 backend
│   ├── 📄 app.py              # FastAPI server & routes
│   ├── 📄 predict.py          # ML inference + model caching
│   ├── 📄 preprocess.py       # Image preprocessing
│   ├── 📄 recommendation.py   # Soil & treatment logic
│   └── 📄 weather.py          # Live weather API
│
├── 📁 models
│   ├── 📄 cotton_model.h5
│   ├── 📄 maize_model.h5
│   ├── 📄 rice_model.h5
│   ├── 📄 sugarcane_model.h5
│   ├── 📄 wheat_model.h5
│   └── 📄 *_classes.json
│
├── 📁 frontend
│   ├── 📁 templates
│   │   ├── 📄 index.html
│   │   └── 📄 dashboard.html
│   └── 📁 static
│       └── 📁 css
│
├── 📁 uploads
│   └── 📄 Runtime image uploads (gitignored)
│
├── 📄 requirements.txt
└── 📄 README.md

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/crop-disease-system.git
cd crop-disease-system

### 2. Install dependencies
```bash
pip install -r requirements.txt

### 3. Run the server
```bash
uvicorn backend.app:app --reload
```

### 4. Open in browser
```
http://127.0.0.1:8000
```
## Supported Crops & Diseases

| Crop | Diseases Detected |
|------|------------------|
| **Cotton** | Leaf Curl, Bacterial Blight, Bollworm, Aphid, Whitefly, Anthracnose, Wilt |
| **Rice** | Blast, Brown Spot, Bacterial Blight, Tungro |
| **Maize** | Common Rust, Gray Leaf Spot, Ear Rot, Fall Armyworm |
| **Wheat** | Black Rust, Yellow Rust, Powdery Mildew, Smut, Aphid |
| **Sugarcane** | Mosaic, Red Rot, Red Rust, Yellow Rust |

## Requirements

```
tensorflow
opencv-python
numpy
fastapi
uvicorn
python-multipart
pillow
jinja2
requests

## 📸 How to Use

1. Select a **crop type**
2. Upload a **leaf image**
3. Enter **soil data** (pH, NPK ratio, Moisture %)
4. Click **Analyze Crop**
5. Get instant results on the dashboard

## ⚠️ Notes

- The `dataset/` folder is excluded from this repo (too large). The **pre-trained `.h5` models** are included and ready to use.
- Weather is currently hardcoded to **Bangalore**. You can change the city in `backend/weather.py`.
- Models are **cached in memory** after first load — subsequent predictions are instant.
