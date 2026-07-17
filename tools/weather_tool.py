"""
Weather Tool
------------
Gets the current weather using Open-Meteo API.
No API key required.
"""

import requests
import config

TOOL_SCHEMA = {
    "name": "get_weather",
    "description": "Get the current weather for any city.",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name"
            }
        },
        "required": ["city"]
    }
}

WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Heavy Drizzle",
    61: "Light Rain",
    63: "Rain",
    65: "Heavy Rain",
    71: "Light Snow",
    73: "Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    81: "Moderate Rain Showers",
    82: "Heavy Rain Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Hail",
    99: "Heavy Thunderstorm"
}


def get_weather(city: str):

    # Step 1: Get Latitude & Longitude
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo = requests.get(
        geo_url,
        params={
            "name": city,
            "count": 1
        },
        timeout=config.REQUEST_TIMEOUT
    ).json()

    if "results" not in geo:
        return {"error": f"City '{city}' not found."}

    place = geo["results"][0]

    lat = place["latitude"]
    lon = place["longitude"]

    # Step 2: Get Current Weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather = requests.get(
        weather_url,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,wind_speed_10m,weather_code,relative_humidity_2m"
        },
        timeout=config.REQUEST_TIMEOUT
    ).json()

    current = weather["current"]

    return {
        "city": place["name"],
        "country": place["country"],
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "condition": WEATHER_CODES.get(current["weather_code"], "Unknown")
    }


def execute(arguments: dict):
    city = arguments.get("city")

    if not city:
        return {"error": "City is required"}

    return get_weather(city)


if __name__ == "__main__":

    result = get_weather("London")

    if "error" in result:
        print(result["error"])
    else:
        print(f"""
Current weather in {result['city']}, {result['country']}

🌡 Temperature : {result['temperature']}°C
☁ Condition   : {result['condition']}
💧 Humidity   : {result['humidity']}%
💨 Wind Speed : {result['wind_speed']} km/h
""")
