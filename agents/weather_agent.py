# agents/weather_agent.py

import requests
import os

def run(previous_data: dict) -> dict:
    """
    Gets weather data at the launch location.
    Requires coordinates or resolved location from SpaceX agent.
    """
    # Dummy fallback coordinates (will be resolved better later)
    lat, lon = 28.562302, -80.577356  # Kennedy Space Center
    api_key = os.getenv("WEATHER_API_KEY")

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    weather_summary = {
        "temperature": data["main"]["temp"],
        "wind_speed": data["wind"]["speed"],
        "clouds": data["clouds"]["all"],
        "condition": data["weather"][0]["description"]
    }

    previous_data.update({"weather": weather_summary})
    return previous_data
