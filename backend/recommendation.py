# ======================================================
# SOIL ANALYSIS (COMMON FOR ALL CROPS)
# ======================================================
def analyze_soil(soil):
    ph = soil["ph"]
    moisture = soil["moisture"]

    # Parse NPK (expects format like "60-50-45")
    try:
        n, p, k = map(int, soil["npk"].split("-"))
    except:
        n, p, k = 0, 0, 0

    # -------------------------
    # Soil condition (pH)
    # -------------------------
    if ph < 5.5:
        soil_status = "Acidic soil"
    elif ph > 7.5:
        soil_status = "Alkaline soil"
    else:
        soil_status = "Neutral soil (Good condition)"

    # -------------------------
    # Fertilizer recommendation
    # -------------------------
    fertilizer = []

    if ph < 5.5:
        fertilizer.append("Apply lime to reduce soil acidity")
    elif ph > 7.5:
        fertilizer.append("Apply gypsum or organic compost")

    if n < 40:
        fertilizer.append("Nitrogen deficient: Apply urea or compost")
    if p < 30:
        fertilizer.append("Phosphorus deficient: Apply DAP or SSP")
    if k < 30:
        fertilizer.append("Potassium deficient: Apply MOP or potash")

    if moisture < 30:
        fertilizer.append("Low moisture: Improve irrigation")
    elif moisture > 80:
        fertilizer.append("High moisture: Improve drainage")

    fertilizer.append("Add organic manure or vermicompost")

    # -------------------------
    # Crop recommendation
    # -------------------------
    if 6.0 <= ph <= 7.0:
        next_crops = ["Maize", "Wheat", "Pulses", "Vegetables"]
    elif ph < 6.0:
        next_crops = ["Rice", "Potato", "Sugarcane"]
    else:
        next_crops = ["Barley", "Millets", "Cotton"]

    return soil_status, fertilizer, next_crops


# ======================================================
# DISEASE CATEGORY DETECTION (ALL CROPS)
# ======================================================
def detect_disease_category(disease_name):
    name = disease_name.lower()

    if any(x in name for x in ["bollworm", "worm", "borer", "stem fly", "army"]):
        return "Insect - Chewing"

    if any(x in name for x in ["aphid", "whitefly", "thrips", "mealy", "bug", "mite"]):
        return "Insect - Sucking"

    if any(x in name for x in [
        "blast", "rust", "blight", "wilt", "mildew",
        "smut", "scab", "leaf spot", "brown spot",
        "brownspot", "anthracnose", "rot"
    ]):
        return "Fungal"

    if "bacterial" in name:
        return "Bacterial"

    if any(x in name for x in ["virus", "mosaic", "leaf curl", "tungro"]):
        return "Viral"

    return "Unknown"


# ======================================================
# MAIN RECOMMENDATION ENGINE (SEVERITY-BASED)
# ======================================================
def recommend_action(result, soil):
    soil_status, fertilizer, next_crops = analyze_soil(soil)

    category = detect_disease_category(result["disease"])
    severity = result["severity"]   # ✅ FROM predict.py (Low / Medium / High)

    # -------------------------
    # Severity-based treatment
    # -------------------------
    if result["status"] == "Healthy":
        treatment = "Crop is healthy. No treatment required."

    elif severity == "Low":
        treatment = (
            "Use organic treatment such as neem oil spray, "
            "biopesticides, and maintain field hygiene."
        )

    elif severity == "Medium":
        treatment = (
            "Apply recommended chemical treatment in controlled dosage "
            "and monitor crop condition regularly."
        )

    else:  # High severity
        treatment = (
            "Immediate pesticide application is required. "
            "Isolate affected plants to prevent disease spread."
        )

    # -------------------------
    # Category-based SUPPORTING advice
    # -------------------------
    if category.startswith("Insect"):
        fertilizer.append("Avoid excess nitrogen; apply neem cake")

    elif category == "Fungal":
        fertilizer.append("Ensure proper drainage and avoid water stagnation")

    elif category == "Bacterial":
        fertilizer.append("Use disease-free seeds and follow crop rotation")

    elif category == "Viral":
        fertilizer.append("Control insect vectors and remove infected plants")

    return {
        "soil_condition": soil_status,
        "disease_category": category,
        "severity": severity,
        "treatment": treatment,
        "fertilizer": ", ".join(fertilizer),
        "next_crop_recommendation": ", ".join(next_crops)
    }