"""
Tools package - all 5 tools are imported and registered from here.
"""

from .weather_tool import get_weather, TOOL_SCHEMA as WEATHER_SCHEMA
from .time_tool import get_time, TOOL_SCHEMA as TIME_SCHEMA
from .calculator_tool import calculate, TOOL_SCHEMA as CALC_SCHEMA
from .currency_tool import convert_currency, TOOL_SCHEMA as CURRENCY_SCHEMA
from .wiki_tool import search_wikipedia, TOOL_SCHEMA as WIKI_SCHEMA

ALL_SCHEMAS = [
    WEATHER_SCHEMA,
    TIME_SCHEMA,
    CALC_SCHEMA,
    CURRENCY_SCHEMA,
    WIKI_SCHEMA,
]

TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "get_time": get_time,
    "calculate": calculate,
    "convert_currency": convert_currency,
    "search_wikipedia": search_wikipedia,
}


def _to_groq_format(schema):
    return {
        "type": "function",
        "function": {
            "name": schema["name"],
            "description": schema["description"],
            "parameters": schema["input_schema"],
        },
    }


GROQ_SCHEMAS = [_to_groq_format(schema) for schema in ALL_SCHEMAS]
