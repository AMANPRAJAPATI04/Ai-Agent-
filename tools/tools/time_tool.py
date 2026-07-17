"""
Time Tool
---------
Tells you the current date & time for any city/timezone.
Uses Python's built-in zoneinfo module — no API key required.
"""

from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones
import config

TOOL_SCHEMA = {
    "name": "get_time",
    "description": "Gets the current date and time for any city or timezone (e.g. 'Asia/Kolkata', 'America/New_York').",
    "input_schema": {
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": "IANA timezone name, e.g. 'Asia/Kolkata', 'America/New_York', 'Europe/London'. If the user only gives a city name (e.g. 'Delhi'), use the nearest matching timezone."
            }
        },
        "required": ["timezone"]
    }
}

# Common city name -> IANA timezone mapping (in case the model doesn't know the exact timezone)
CITY_ALIASES = {
    "delhi": "Asia/Kolkata",
    "mumbai": "Asia/Kolkata",
    "india": "Asia/Kolkata",
    "new york": "America/New_York",
    "london": "Europe/London",
    "tokyo": "Asia/Tokyo",
    "dubai": "Asia/Dubai",
    "sydney": "Australia/Sydney",
    "los angeles": "America/Los_Angeles",
    "paris": "Europe/Paris",
    "singapore": "Asia/Singapore",
}


def get_time(timezone: str = None) -> str:
    try:
        tz_key = (timezone or config.DEFAULT_TIMEZONE).strip()
        lookup = tz_key.lower()

        if lookup in CITY_ALIASES:
            tz_key = CITY_ALIASES[lookup]

        if tz_key not in available_timezones():
            return (
                f"'{timezone}' isn't a valid timezone. "
                f"Example: 'Asia/Kolkata', 'America/New_York', 'Europe/London'"
            )

        now = datetime.now(ZoneInfo(tz_key))
        formatted = now.strftime("%A, %d %B %Y — %I:%M:%S %p (%Z)")

        return f"Current time in {tz_key}: {formatted}"

    except Exception as e:
        return f"Error fetching time: {str(e)}"


if __name__ == "__main__":
    print(get_time("Asia/Kolkata"))
