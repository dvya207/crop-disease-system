import os
import json
import numpy as np
import tensorflow as tf
from backend.preprocess import preprocess_image

# ✅ Absolute path — works regardless of where uvicorn is launched from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# ✅ Model cache — load each crop model ONCE, reuse on every request
_model_cache = {}

# -------------------------------------------------
# DISEASE → CATEGORY MAP (FROM DATASET)
# -------------------------------------------------
DISEASE_CATEGORY_MAP = {
    # --- COTTON ---
    "healthy": "Healthy",
    "leaf curl": "Viral",
    "bacterial_blight in cotton": "Bacterial",
    "anthracnose on cotton": "Fungal",
    "bollrot on cotton": "Fungal",
    "wilt": "Fungal",
    "american bollworm on cotton": "Insect - Chewing",
    "bollworm on cotton": "Insect - Chewing",
    "pink bollworm in cotton": "Insect - Chewing",
    "army worm": "Insect - Chewing",
    "cotton aphid": "Insect - Sucking",
    "cotton mealy bug": "Insect - Sucking",
    "cotton whitefly": "Insect - Sucking",
    "thrips on cotton": "Insect - Sucking",
    "red cotton bug": "Insect - Sucking",

    # --- MAIZE ---
    "common_rust": "Fungal",
    "gray leaf spot": "Fungal",
    "maize ear rot": "Fungal",
    "maize fall armyworm": "Insect - Chewing",
    "maize stem borer": "Insect - Chewing",

    # --- RICE ---
    "bacterial blight in rice": "Bacterial",
    "brownspot": "Fungal",
    "rice blast": "Fungal",
    "tungro": "Viral",

    # --- SUGARCANE ---
    "mosaic sugarcane": "Viral",
    "redrot sugarcane": "Fungal",
    "redrust sugarcane": "Fungal",
    "yellow rust sugarcane": "Fungal",

    # --- WHEAT ---
    "flag smut": "Fungal",
    "leaf smut": "Fungal",
    "wheat black rust": "Fungal",
    "wheat brown leaf rust": "Fungal",
    "wheat_yellow_rust": "Fungal",
    "wheat leaf blight": "Fungal",
    "wheat powdery mildew": "Fungal",
    "wheat scab": "Fungal",
    "wheat aphid": "Insect - Sucking",
    "wheat stem fly": "Insect - Chewing",
    "wheat mite": "Mite"
}


# -------------------------------------------------
# LOAD MODEL WITH CACHING
# -------------------------------------------------
def load_model_and_classes(crop):
    crop = crop.lower()

    if crop not in _model_cache:
        model_path = os.path.join(MODEL_DIR, f"{crop}_model.h5")
        classes_path = os.path.join(MODEL_DIR, f"{crop}_classes.json")

        print(f"[INFO] Loading model for '{crop}' from: {model_path}")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        if not os.path.exists(classes_path):
            raise FileNotFoundError(f"Classes file not found: {classes_path}")

        model = tf.keras.models.load_model(model_path)
        with open(classes_path) as f:
            classes = json.load(f)

        _model_cache[crop] = (model, classes)
        print(f"[INFO] Model for '{crop}' loaded and cached ✅")
    else:
        print(f"[INFO] Using cached model for '{crop}' ⚡")

    return _model_cache[crop]


# -------------------------------------------------
# PREDICT DISEASE
# -------------------------------------------------
def predict_disease(image_path, crop):
    model, classes = load_model_and_classes(crop)

    img = preprocess_image(image_path)
    preds = model.predict(img)[0]

    idx = int(np.argmax(preds))
    confidence = float(preds[idx]) * 100
    label = classes[idx]
    label_lower = label.lower()

    is_healthy = label_lower == "healthy"

    # Severity
    if is_healthy:
        severity = "Low"
    elif confidence >= 80:
        severity = "High"
    elif confidence >= 50:
        severity = "Medium"
    else:
        severity = "Low"

    # Category
    category = DISEASE_CATEGORY_MAP.get(label_lower, "Fungal")

    explanation = (
        "The leaf shows no disease symptoms."
        if is_healthy else
        f"The model detected visual patterns corresponding to {label}."
    )

    return {
        "crop": crop.capitalize(),
        "status": "Healthy" if is_healthy else "Diseased",
        "disease": "None" if is_healthy else label,
        "confidence": round(confidence, 2),
        "severity": severity,
        "category": category,
        "explanation": explanation
    }