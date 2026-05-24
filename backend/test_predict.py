import os
from predict import predict_disease

# -----------------------------
# CHANGE ONLY THESE 2 LINES
# -----------------------------
IMAGE_PATH = "test_images/rice.jpg"   # put image path here
CROP = "rice"                         # cotton / maize / wheat / rice / sugarcane


if not os.path.exists(IMAGE_PATH):
    print("❌ Image not found:", IMAGE_PATH)
else:
    result = predict_disease(IMAGE_PATH, CROP)

    print("\n🌿 PREDICTION RESULT")
    print("-------------------")
    print("Crop      :", result["crop"])
    print("Status    :", result["status"])
    print("Disease   :", result["disease"])
    print("Confidence:", result["confidence"], "%")
