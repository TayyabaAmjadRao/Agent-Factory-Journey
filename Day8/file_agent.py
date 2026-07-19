
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
            "name": "read_file",
            "description": "Read content from a text file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of file to read"
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a text file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string"
                    },
                    "content": {
                        "type": "string"
                    }
                },
                "required": ["filename", "content"]
            }
        }
    }
]

# Tool functions
def read_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except:
        return f"Error: {filename} not found!"

def write_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)
    return f"File '{filename}' saved successfully!"

# Agent
messages = [
    {"role": "system", "content": "You are a helpful file assistant. Read and write files when needed."}
]

print("File Agent Ready!")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=tools
        )

        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if tool_name == "read_file":
                result = read_file(args["filename"])
            elif tool_name == "write_file":
                result = write_file(args["filename"], args["content"])

            print(f"  [Tool: {tool_name} → {result}]")

            messages.append({"role": "assistant", "content": None, "tool_calls": [tool_call]})
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

        else:
            reply = response.choices[0].message.content
            print(f"Agent: {reply}\n")
            messages.append({"role": "assistant", "content": reply})
            break