"""
Currency Converter Tool
-----------------------
Converts an amount from one currency to another.
Uses a free exchange rate API - no API key required.
"""

import requests
import config

TOOL_SCHEMA = {
    "name": "convert_currency",
    "description": "Converts an amount from one currency to another, e.g. USD to INR.",
    "input_schema": {
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "description": "The amount to convert, e.g. 100"
            },
            "from_currency": {
                "type": "string",
                "description": "Source currency code, e.g. 'USD', 'INR', 'EUR'"
            },
            "to_currency": {
                "type": "string",
                "description": "Target currency code, e.g. 'INR', 'USD', 'EUR'"
            }
        },
        "required": ["amount", "from_currency", "to_currency"]
    }
}


def convert_currency(amount: float, from_currency: str = None, to_currency: str = None) -> str:
    try:
        from_curr = (from_currency or config.DEFAULT_CURRENCY).strip().upper()
        to_curr = (to_currency or config.DEFAULT_CURRENCY).strip().upper()

        url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
        resp = requests.get(url, timeout=config.REQUEST_TIMEOUT)
        data = resp.json()

        if "rates" not in data:
            return f"'{from_curr}' doesn't look like a valid currency code."

        rates = data["rates"]
        if to_curr not in rates:
            return f"'{to_curr}' doesn't look like a valid currency code."

        rate = rates[to_curr]
        converted = amount * rate

        return f"{amount} {from_curr} = {round(converted, 2)} {to_curr} (rate: 1 {from_curr} = {rate} {to_curr})"

    except Exception as e:
        return f"Error converting currency: {str(e)}"


if __name__ == "__main__":
    print(convert_currency(100, "USD", "INR"))
