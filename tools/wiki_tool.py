"""
Wikipedia Search Tool
---------------------
Fetches a short summary of any topic from Wikipedia.
Uses the Wikipedia REST API - no API key required.
"""

import requests
import config

TOOL_SCHEMA = {
    "name": "search_wikipedia",
    "description": "Fetches a short summary from Wikipedia about any topic, person, or thing.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The topic to look up, e.g. 'Albert Einstein', 'Eiffel Tower'"
            }
        },
        "required": ["query"]
    }
}


def search_wikipedia(query: str) -> str:
    try:
        formatted_query = query.strip().replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_query}"
        resp = requests.get(url, timeout=config.REQUEST_TIMEOUT)

        if resp.status_code == 404:
            return f"Couldn't find anything on Wikipedia about '{query}'."

        data = resp.json()
        title = data.get("title", query)
        extract = data.get("extract", "No summary available.")

        return f"{title}:\n{extract}"

    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"


if __name__ == "__main__":
    print(search_wikipedia("Eiffel Tower"))
