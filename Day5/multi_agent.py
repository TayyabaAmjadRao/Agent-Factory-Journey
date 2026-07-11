from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Tools definition
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
                        "type": "string",
                        "description": "Math expression like 2+2 or 10*5"
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
                    "unit": {"type": "string", "description": "C or F"}
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
    if unit == "C":
        result = (value * 9/5) + 32
        return f"{value}°C = {result}°F"
    else:
        result = (value - 32) * 5/9
        return f"{value}°F = {result}°C"

def count_words(text):
    count = len(text.split())
    return f"Word count: {count}"

# Agent
messages = [
    {"role": "system", "content": "You are a helpful assistant with calculator, temperature converter and word counter tools."}
]

user_input = input("Ask me anything: ")
messages.append({"role": "user", "content": user_input})

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=tools
)

# Check tool calls
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

    print(f"Agent used {tool_name}: {result}")
else:
    print(f"Agent: {response.choices[0].message.content}")