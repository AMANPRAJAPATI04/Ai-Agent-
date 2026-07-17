"""
Weather Tool
------------
Tells you the current weather for any city.
Uses the Open-Meteo API (completely FREE, no API key required).
"""

import requests
import config

TOOL_SCHEMA = {
    "name": "get_weather",
    "description": "Gets the current weather (temperature, wind, condition) for any city or location.",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city name, e.g. 'London', 'New York', 'Mumbai'"
            }
        },
        "required": ["city"]
    }
}

# Open-Meteo weather codes converted into readable text
WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail"
}


def get_weather(city: str) -> str:
    try:
        # Step 1: Get lat/long for the city (geocoding)
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_resp = requests.get(geo_url, params={"name": city, "count": 1}, timeout=config.REQUEST_TIMEOUT)
        geo_data = geo_resp.json()

        if not geo_data.get("results"):
            return f"Couldn't find a place called '{city}'. Please check the spelling."

        place = geo_data["results"][0]
        lat, lon = place["latitude"], place["longitude"]
        full_name = f"{place['name']}, {place.get('country', '')}"

        # Step 2: Fetch the weather
        weather_url = "https://api.open-meteo.com/v1/forecast"
        w_resp = requests.get(
            weather_url,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True
            },
            timeout=config.REQUEST_TIMEOUT
        )
        w_data = w_resp.json()
        current = w_data.get("current_weather", {})

        temp = current.get("temperature")
        wind = current.get("windspeed")
        code = current.get("weathercode")
        condition = WEATHER_CODES.get(code, "Unknown")

        return (
            f"Weather in {full_name}:\n"
            f"- Temperature: {temp}°C\n"
            f"- Condition: {condition}\n"
            f"- Wind Speed: {wind} km/h"
        )

    except Exception as e:
        return f"Error fetching weather: {str(e)}"


if __name__ == "__main__":
    print(get_weather("London"))
