"""
Config File
===========
All settings live here — API key, model name, and other configuration.
If you ever need to change something (model, timeout, etc.), just edit
this file — no need to touch the rest of the code.
"""

import os

# ---------------------------------------------------------------------
# GROQ API SETTINGS
# ---------------------------------------------------------------------

# The API key is read from an environment variable. If it's not set,
# the default below is empty (recommended — using an environment
# variable is more secure than hardcoding a key here).
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# You *can* hardcode your key here for quick local testing, but never
# commit that to GitHub or share it with anyone:
# GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxx"

# Which Groq model to use. Options:
#   "llama-3.3-70b-versatile"  -> most capable, best for tool-use (default)
#   "llama-3.1-8b-instant"      -> faster and lighter, but tool-calling is
#                                   slightly less accurate
#   "mixtral-8x7b-32768"          -> if you need a longer context window
MODEL_NAME = "llama-3.3-70b-versatile"

# Max tokens allowed in the model's response
MAX_TOKENS = 1024

# How "creative" the model should be (0 = fully factual/deterministic, 1 = more creative)
TEMPERATURE = 0.7


# ---------------------------------------------------------------------
# AGENT BEHAVIOUR SETTINGS
# ---------------------------------------------------------------------

# System prompt — the agent's default behaviour/personality
SYSTEM_PROMPT = (
    "You are a helpful AI assistant that uses tools when needed to answer "
    "the user's questions accurately. Keep your responses clear and concise."
)

# Maximum number of tool-call iterations allowed per user message
# (prevents infinite loops)
MAX_TOOL_ITERATIONS = 10


# ---------------------------------------------------------------------
# TOOL-SPECIFIC SETTINGS
# ---------------------------------------------------------------------

# Timeout (in seconds) for every external API call (weather, currency, wiki)
REQUEST_TIMEOUT = 10

# Default base currency for the currency converter (used if the user doesn't specify one)
DEFAULT_CURRENCY = "USD"

# Default timezone for the time tool (used if the user doesn't specify one)
DEFAULT_TIMEZONE = "Asia/Kolkata"


# ---------------------------------------------------------------------
# VALIDATION — fail fast with a clear message if something required is missing
# ---------------------------------------------------------------------

def validate_config():
    """Checks required settings before the agent starts."""
    errors = []

    if not GROQ_API_KEY:
        errors.append(
            "GROQ_API_KEY is not set! Run this in your terminal:\n"
            "  PowerShell:   $env:GROQ_API_KEY=\"your-api-key-here\"\n"
            "  Mac/Linux:    export GROQ_API_KEY=\"your-api-key-here\"\n"
            "Get a free API key here: https://console.groq.com/keys"
        )

    if errors:
        raise ValueError("\n\n".join(errors))

    return True


if __name__ == "__main__":
    try:
        validate_config()
        print("✅ Config looks good, everything is set!")
        print(f"Model: {MODEL_NAME}")
        print(f"API key set: {'Yes' if GROQ_API_KEY else 'No'}")
    except ValueError as e:
        print(f"❌ Config problem:\n{e}")
