from groq import Groq
from dotenv import load_dotenv
from ddgs import DDGS
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Tool
tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for latest information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "search query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# Tool function
def web_search(query):
    results = DDGS().text(query, max_results=3)
    output = ""
    for r in results:
        output += f"Title: {r['title']}\n"
        output += f"Info: {r['body']}\n\n"
    return output

# Agent
messages = [
    {"role": "system", "content": "You are a helpful assistant. When user asks something, FIRST use web_search tool to find information. After getting search results, ALWAYS summarize the results and give a clear answer to the user. Never say 'Done searching' — always give the actual answer."}
]

print("Web Search Agent Ready!")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    max_iterations = 3
    iteration = 0
    final_reply = ""

    while True:
        iteration += 1
        if iteration > max_iterations:
            if final_reply:
                print(f"Agent: {final_reply}\n")
            else:
                print("Agent: I searched but could not find a clear answer!\n")
            break

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            result = ""
            if tool_name == "web_search":
                result = web_search(args["query"])

            print(f"  [Searching: {args['query']}...]")

            messages.append({"role": "assistant", "content": None, "tool_calls": [tool_call]})
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

        else:
            final_reply = response.choices[0].message.content
            print(f"Agent: {final_reply}\n")
            messages.append({"role": "assistant", "content": final_reply})
            break