import requests

API_KEY = "5b1fa55583460bf6627a02d84a745dd7"

def get_weather(city="Bangalore"):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url, timeout=5)
    data = response.json()

    # ✅ API working → use live data
    if response.status_code == 200 and "main" in data:
        return {
            "temperature": round(data["main"]["temp"], 1),
            "humidity": data["main"]["humidity"],
            "rain_chance": data.get("clouds", {}).get("all", 0)
        }

    # ❌ Only if API fails
    return {
        "temperature": 25,
        "humidity": 70,
        "rain_chance": 10
    }