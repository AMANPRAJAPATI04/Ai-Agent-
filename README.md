# AI Agent — Powered by Groq (5 Tools)

A tool-using AI agent built with Python and the **Groq API** (LLaMA 3.3 70B).
It understands natural language requests and automatically calls the right
tool to answer them.

Comes in two flavors:
- **CLI version** (`agent.py`) — runs in your terminal
- **Web version** (`app.py`) — a browser-based chat interface built with
  Streamlit, deployable for free

## 📁 Project Structure

```
ai_agent/
├── agent.py                  # CLI version — run this in the terminal
├── app.py                      # Web version (Streamlit) — use this to deploy
├── config.py                    # ⭐ All settings live here (API key, model, etc.)
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example    # Copy this to secrets.toml for deployment
└── tools/
    ├── __init__.py            # All tools are registered here
    ├── weather_tool.py          # Tool 1: Weather
    ├── time_tool.py               # Tool 2: Time
    ├── calculator_tool.py          # Tool 3: Calculator
    ├── currency_tool.py             # Tool 4: Currency Converter
    └── wiki_tool.py                  # Tool 5: Wikipedia Search
```

## 🔧 What the 5 Tools Do

| Tool | What it does |
|------|--------------|
| `get_weather` | Gets the current weather for any city (Open-Meteo API — free) |
| `get_time` | Gets the current time for any timezone/city |
| `calculate` | Safely evaluates math expressions |
| `convert_currency` | Converts between currencies (free API) |
| `search_wikipedia` | Fetches a Wikipedia summary for any topic |

## ⚙️ config.py — All Settings in One Place

Everything (API key, model name, timeout, defaults) is centralized here:

```python
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")   # Comes from an environment variable
MODEL_NAME = "llama-3.3-70b-versatile"                 # Change the model here
MAX_TOKENS = 1024                                        # Max response length
TEMPERATURE = 0.7                                          # Creativity level
SYSTEM_PROMPT = "..."                                        # Agent's behaviour
REQUEST_TIMEOUT = 10                                          # Timeout for tool API calls
DEFAULT_CURRENCY = "USD"                                        # Default for currency tool
DEFAULT_TIMEZONE = "Asia/Kolkata"                                 # Default for time tool
```

If the API key isn't set, the agent will show a clear error message when it starts.

## 🖥️ Local Setup

1. Make sure you have Python 3.10+ installed (needed for `zoneinfo`)

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get a free Groq API key: https://console.groq.com/keys

4. Set your API key as an environment variable:

**Mac/Linux:**
```bash
export GROQ_API_KEY="your-api-key-here"
```

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your-api-key-here"
```

**Windows (CMD):**
```cmd
set GROQ_API_KEY=your-api-key-here
```

## ▶️ Running the CLI Version

```bash
python agent.py
```

Then just type naturally, for example:
- "What's the weather in London?"
- "What time is it in Tokyo?"
- "What's 125 * 48 + sqrt(144)?"
- "Convert 100 USD to INR"
- "Tell me about the Eiffel Tower"

Type `quit`, `exit`, or `bye` to leave.

## 🌐 Running the Web Version Locally

Instead of setting an environment variable each time, it's easier to use a
secrets file for the web app:

1. Go into the `.streamlit` folder
2. Copy `secrets.toml.example` and rename the copy to `secrets.toml`
3. Open `secrets.toml` and put your real API key in it:
   ```toml
   GROQ_API_KEY = "your-api-key-here"
   ```
4. Run:
   ```bash
   streamlit run app.py
   ```
5. It will open in your browser at `http://localhost:8501`

## 🚀 Deploying the Web App (Streamlit Cloud — FREE)

This is the easiest and free way to make your agent live on the web.

### Step 1: Push your code to GitHub

1. Create a new repository on https://github.com
2. Upload your entire project folder (all files and folders)
   - ⚠️ **Never upload `secrets.toml`** (only upload `secrets.toml.example`) — your `.gitignore` already protects against this if you use Git commands
3. Commit the changes

### Step 2: Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **"Create app"** / **"New app"**
4. Fill in:
   - **Repository:** your repo
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Advanced settings"** and add your secret:
   ```toml
   GROQ_API_KEY = "your-real-groq-api-key"
   ```
6. Click **"Deploy"**

In 2-3 minutes your agent will be live at a public URL like:
```
https://your-app-name.streamlit.app
```

Share this link with anyone — they'll be able to use your AI agent directly
in their browser.

## ➕ Adding a New Tool

1. Create a new file in `tools/` (e.g. `my_tool.py`)
2. Write a function and a `TOOL_SCHEMA` dictionary (follow the pattern of the existing tools)
3. Register it in `tools/__init__.py`:
   - Add the schema to the `ALL_SCHEMAS` list
   - Add the function to the `TOOL_FUNCTIONS` dict

That's it — the agent will automatically learn to use the new tool.

## 💡 Notes

- Weather, Currency, and Wikipedia tools use free public APIs (no API key
  needed for those — only Groq needs a key).
- The calculator is safe — it never uses `eval()`, so there's no security risk.
- If a tool fails (e.g. no internet), it returns an error message and the
  agent will let you know.
- Groq is very fast (runs on custom LPU hardware) and its free tier has
  generous rate limits — great for testing and personal projects.
