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
                    "expression": {
                        "type": "string"
                    }
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

# Agentic Loop
messages = [
    {"role": "system", "content": "You are a helpful assistant. Use tools when needed. Complete all tasks step by step."}
]

user_input = input("You: ")
messages.append({"role": "user", "content": user_input})

# Loop Start
while True:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools
    )

    # Check Tool call 
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        # Tool run
        if tool_name == "calculate":
            result = calculate(args["expression"])
        elif tool_name == "convert_temperature":
            result = convert_temperature(args["value"], args["unit"])
        elif tool_name == "count_words":
            result = count_words(args["text"])

        print(f"Tool used: {tool_name} → {result}")

        # Result add in messages
        messages.append({"role": "assistant", "content": None, "tool_calls": [tool_call]})
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

    # Not Tool — final answer
    else:
        final = response.choices[0].message.content
        print(f"Agent: {final}")
        break