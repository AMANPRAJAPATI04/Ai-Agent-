"""
Streamlit Web App
==================
This app.py is the web (browser) version of our AI Agent.
Uses the same 5 tools as the CLI agent.py — just the interface is a
chat window in the browser instead of a terminal.

To run locally:
    pip install -r requirements.txt
    streamlit run app.py

For deployment instructions, see README.md (Streamlit Cloud — free).
"""

import json
import streamlit as st
from groq import Groq

import config
from tools import GROQ_SCHEMAS, TOOL_FUNCTIONS

# ---------------------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="AI Agent - Weather, Time, Calculator & More",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Agent")
st.caption("Weather • Time • Calculator • Currency Converter • Wikipedia Search")


# ---------------------------------------------------------------------
# API KEY HANDLING
# ---------------------------------------------------------------------
# On deployment, the API key comes from Streamlit Secrets.
# For local testing, it can also come from config.py / an environment variable.

def get_api_key():
    # First check Streamlit secrets (for deployment)
    try:
        return st.secrets["GROQ_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass
    # Otherwise fall back to config.py / environment variable (for local testing)
    return config.GROQ_API_KEY


api_key = get_api_key()

if not api_key:
    st.error(
        "⚠️ GROQ_API_KEY is not set!\n\n"
        "- **Locally**: set it in `config.py` or as an environment variable\n"
        "- **When deploying**: add it to Streamlit Cloud's Secrets\n\n"
        "Get a free key here: https://console.groq.com/keys"
    )
    st.stop()

client = Groq(api_key=api_key)


# ---------------------------------------------------------------------
# TOOL EXECUTION
# ---------------------------------------------------------------------

def run_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name not in TOOL_FUNCTIONS:
        return f"Unknown tool: {tool_name}"
    func = TOOL_FUNCTIONS[tool_name]
    try:
        return func(**tool_input)
    except Exception as e:
        return f"Error running tool '{tool_name}': {str(e)}"


def chat_with_agent(messages: list) -> str:
    """
    Runs the full tool-use loop and returns only the final text answer
    (to display in the Streamlit UI).
    """
    iterations = 0

    while iterations < config.MAX_TOOL_ITERATIONS:
        iterations += 1

        try:
            response = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
                tools=GROQ_SCHEMAS,
                tool_choice="auto",
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE,
            )
        except Exception as e:
            error_text = str(e)

            # Groq's model can sometimes generate a malformed tool call
            # (e.g. "<function=...>"). Instead of crashing, try once more
            # without tools to get a plain text answer.
            if "tool_use_failed" in error_text or "Failed to call a function" in error_text:
                try:
                    fallback_response = client.chat.completions.create(
                        model=config.MODEL_NAME,
                        messages=messages,
                        max_tokens=config.MAX_TOKENS,
                        temperature=config.TEMPERATURE,
                    )
                    return fallback_response.choices[0].message.content or (
                        "Sorry, I had trouble understanding that question. "
                        "Could you try rephrasing it?"
                    )
                except Exception:
                    return (
                        "Sorry, I ran into an issue processing that request. "
                        "Please try asking again in a simpler way."
                    )

            # Re-raise anything else
            raise

        choice = response.choices[0]
        msg = choice.message

        if msg.tool_calls:
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            })

            for tc in msg.tool_calls:
                tool_name = tc.function.name

                try:
                    tool_input = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    tool_input = {}
                    result = f"Couldn't parse the arguments for '{tool_name}'. Please rephrase the question more clearly."
                else:
                    result = run_tool(tool_name, tool_input)

                # Show a small status widget in the UI
                with st.status(f"🔧 Running {tool_name}...", expanded=False) as status:
                    st.write(f"Input: {tool_input}")
                    st.write(f"Result: {result}")
                    status.update(label=f"✅ {tool_name} complete", state="complete")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

            continue

        return msg.content or ""

    return "Sorry, this request needed too many tool calls to process. Please try again."


# ---------------------------------------------------------------------
# SESSION STATE (keeps chat history within the browser session)
# ---------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": config.SYSTEM_PROMPT}
    ]

# Display previous messages (skip the system message)
for msg in st.session_state.messages:
    if msg["role"] in ("user", "assistant") and msg.get("content"):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


# ---------------------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------------------

user_input = st.chat_input("Ask me anything... (e.g. 'What's the weather in London?')")

if user_input:
    # Show the user's message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get the agent's reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = chat_with_agent(st.session_state.messages)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})


# ---------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------

with st.sidebar:
    st.header("ℹ️ About This Agent")
    st.markdown(f"""
    **Model:** `{config.MODEL_NAME}`

    **5 Tools:**
    - 🌤️ Weather
    - 🕐 Time
    - 🔢 Calculator
    - 💱 Currency Converter
    - 📖 Wikipedia Search
    """)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": config.SYSTEM_PROMPT}
        ]
        st.rerun()
