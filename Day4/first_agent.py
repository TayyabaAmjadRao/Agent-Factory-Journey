from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Tool definition 
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
    }
]

# Actual tool function
def calculate(expression):
    result = eval(expression)
    return str(result)

# Agent
messages = [
    {"role": "system", "content": "You are a helpful assistant with calculator ability."}
]

user_input = input("Ask me anything: ")
messages.append({"role": "user", "content": user_input})

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=tools
)

# Check if agent wants to use tool
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    expression = json.loads(tool_call.function.arguments)["expression"]
    result = calculate(expression)
    print(f"Agent calculated: {expression} = {result}")
else:
    print(f"Agent: {response.choices[0].message.content}")