"""
AI Agent - CLI Version (Groq Powered)
=====================================
This agent uses the Groq API (LLaMA models) to chat with the user, and
calls one of 5 tools whenever needed:

1. get_weather        -> tools/weather_tool.py
2. get_time            -> tools/time_tool.py
3. calculate            -> tools/calculator_tool.py
4. convert_currency     -> tools/currency_tool.py
5. search_wikipedia     -> tools/wiki_tool.py

All settings (API key, model, etc.) live in config.py.

Before running:
    pip install -r requirements.txt
    export GROQ_API_KEY="your-groq-api-key-here"      (Mac/Linux)
    $env:GROQ_API_KEY="your-groq-api-key-here"          (Windows PowerShell)

To run:
    python agent.py
"""

import json
from groq import Groq

import config
from tools import GROQ_SCHEMAS, TOOL_FUNCTIONS

# Validate config before starting (raises a clear error if the API key is missing)
config.validate_config()

client = Groq(api_key=config.GROQ_API_KEY)


def run_tool(tool_name: str, tool_input: dict) -> str:
    """Calls the correct tool function based on the tool name."""
    if tool_name not in TOOL_FUNCTIONS:
        return f"Unknown tool: {tool_name}"

    func = TOOL_FUNCTIONS[tool_name]
    try:
        return func(**tool_input)
    except Exception as e:
        return f"Error running tool '{tool_name}': {str(e)}"


def chat_with_agent(messages: list) -> list:
    """
    Processes a user message. If Groq wants to call a tool, runs the tool
    and sends the result back, looping until a final text answer is produced.
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

            # Groq's model can sometimes generate a malformed tool call.
            # Instead of crashing, try once more without tools to get a
            # plain text answer.
            if "tool_use_failed" in error_text or "Failed to call a function" in error_text:
                try:
                    fallback_response = client.chat.completions.create(
                        model=config.MODEL_NAME,
                        messages=messages,
                        max_tokens=config.MAX_TOKENS,
                        temperature=config.TEMPERATURE,
                    )
                    final_text = fallback_response.choices[0].message.content or (
                        "Sorry, I had trouble understanding that question. "
                        "Could you try rephrasing it?"
                    )
                except Exception:
                    final_text = (
                        "Sorry, I ran into an issue processing that request. "
                        "Please try asking again in a simpler way."
                    )
                messages.append({"role": "assistant", "content": final_text})
                return messages

            raise

        choice = response.choices[0]
        msg = choice.message

        # If the model wants to call a tool
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
                    print(f"  [Running tool: {tool_name}({tool_input})]")
                    result = run_tool(tool_name, tool_input)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

            continue  # Keep looping until a final answer is produced

        # Got the final text answer
        final_text = msg.content or ""
        messages.append({"role": "assistant", "content": final_text})
        return messages

    # If we hit max iterations without a final answer
    messages.append({
        "role": "assistant",
        "content": "Sorry, this request needed too many tool calls to process. Please try again."
    })
    return messages


def main():
    print("=" * 50)
    print("  AI Agent - Groq Powered")
    print("  5 Tools: Weather, Time, Calculator,")
    print("  Currency Converter, Wikipedia Search")
    print(f"  Model: {config.MODEL_NAME}")
    print("  Type 'quit' to exit")
    print("=" * 50)

    conversation = [
        {"role": "system", "content": config.SYSTEM_PROMPT}
    ]

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("quit", "exit", "bye"):
            print("Agent: Goodbye! 👋")
            break

        conversation.append({"role": "user", "content": user_input})
        conversation = chat_with_agent(conversation)

        last_msg = conversation[-1]
        if last_msg["role"] == "assistant" and last_msg.get("content"):
            print(f"\nAgent: {last_msg['content']}")


if __name__ == "__main__":
    main()
