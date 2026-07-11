from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a math expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_temperature",
            "description": "Convert temperature between Celsius and Fahrenheit",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "number"},
                    "unit": {"type": "string"}
                },
                "required": ["value", "unit"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_words",
            "description": "Count words in a text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"}
                },
                "required": ["text"]
            }
        }
    }
]

# Tool functions
def calculate(expression):
    return str(eval(expression))

def convert_temperature(value, unit):
    if unit.upper() in ["C", "CELSIUS"]:
        result = (value * 9/5) + 32
        return f"{value}°C = {result}°F"
    else:
        result = (value - 32) * 5/9
        return f"{value}°F = {result}°C"

def count_words(text):
    return f"Word count: {len(text.split())}"

# Memory
chat_history = [
    {"role": "system", "content": """You are Aria, a personal AI assistant.
You are helpful, smart and friendly.
Use tools when needed.
Remember the conversation history."""}
]

print("Aria: Hello! I am Aria, your personal AI assistant. How can I help you?")
print("(Type 'exit' to quit)\n")

# Main loop
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Aria: Goodbye! Have a great day!")
        break

    chat_history.append({"role": "user", "content": user_input})

    # Agentic loop
    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_history,
            tools=tools
        )

        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if tool_name == "calculate":
                result = calculate(args["expression"])
            elif tool_name == "convert_temperature":
                result = convert_temperature(args["value"], args["unit"])
            elif tool_name == "count_words":
                result = count_words(args["text"])

            print(f"  [Tool: {tool_name} → {result}]")

            chat_history.append({"role": "assistant", "content": None, "tool_calls": [tool_call]})
            chat_history.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

        else:
            reply = response.choices[0].message.content
            print(f"Aria: {reply}\n")
            chat_history.append({"role": "assistant", "content": reply})
            break