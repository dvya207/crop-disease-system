import os
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.predict import predict_disease
from backend.recommendation import recommend_action
from backend.weather import get_weather

app = FastAPI()

# ----------------------
# Paths
# ----------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

templates = Jinja2Templates(directory="frontend/templates")

# ----------------------
# Static files
# ----------------------
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# ----------------------
# Routes
# ----------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/predict-ui", response_class=HTMLResponse)
async def predict_ui(
    request: Request,
    crop: str = Form(...),
    ph: float = Form(...),
    npk: str = Form(...),
    moisture: float = Form(...),
    image: UploadFile = File(...)
):
    try:
        # ----------------------
        # Save image
        # ----------------------
        image_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(image_path, "wb") as f:
            f.write(await image.read())

        # ----------------------
        # ML Prediction
        # ----------------------
        result = predict_disease(image_path, crop)

        # ----------------------
        # Soil data
        # ----------------------
        soil = {
            "ph": ph,
            "npk": npk,
            "moisture": moisture
        }

        # ----------------------
        # 🌦 Live Weather
        # ----------------------
        weather_data = get_weather("Bangalore")
        weather = {
            "temp": f"{weather_data['temperature']}°C",
            "humidity": f"{weather_data['humidity']}%",
            "rain": f"{weather_data['rain_chance']}%"
        }

        # ----------------------
        # Recommendation
        # ----------------------
        rec_raw = recommend_action(result, soil)

        if isinstance(rec_raw, str):
            recommendation = {
                "soil_condition": "Normal",
                "treatment": rec_raw,
                "fertilizer": "Organic manure",
                "next_crop": "Maize, Wheat"
            }
        else:
            recommendation = {
                "soil_condition": rec_raw.get("soil_condition", "Normal"),
                "treatment": rec_raw.get("treatment", "Follow standard treatment"),
                "fertilizer": rec_raw.get("fertilizer", "Organic manure"),
                "next_crop": rec_raw.get("next_crop_recommendation", "Maize")
            }

        # ----------------------
        # Render Dashboard
        # ----------------------
        return templates.TemplateResponse(
            request,
            "dashboard.html",
            {
                "crop": result["crop"],
                "disease": result["disease"],
                "confidence": result["confidence"],
                "severity": result["severity"],
                "category": result.get("category", "Unknown"),
                "explanation": result.get("explanation", "Leaf symptoms detected"),
                "image_url": f"/uploads/{image.filename}",
                "soil": soil,
                "weather": weather,
                "recommendation": recommendation
            }
        )

    except Exception as e:
        # ----------------------
        # Friendly error page
        # ----------------------
        error_html = f"""
        <!DOCTYPE html><html><head><title>Error</title>
        <style>
          body{{font-family:Segoe UI,sans-serif;background:#fff8f0;display:flex;
               justify-content:center;align-items:center;height:100vh;margin:0;}}
          .box{{background:#fff;padding:40px;border-radius:20px;max-width:600px;
                box-shadow:0 10px 30px rgba(0,0,0,0.1);text-align:center;}}
          h2{{color:#c0392b;}} pre{{background:#f5f5f5;padding:15px;border-radius:10px;
              text-align:left;font-size:13px;overflow:auto;}}
          a{{display:inline-block;margin-top:20px;padding:12px 28px;
             background:#2e7d32;color:#fff;border-radius:30px;text-decoration:none;}}
        </style></head><body>
        <div class="box">
          <h2>⚠️ Analysis Failed</h2>
          <p>Something went wrong during analysis. See the error below:</p>
          <pre>{str(e)}</pre>
          <a href="/">← Try Again</a>
        </div></body></html>
        """
        return HTMLResponse(content=error_html, status_code=500)