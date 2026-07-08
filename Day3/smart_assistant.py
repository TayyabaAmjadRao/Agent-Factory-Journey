from dotenv import load_dotenv
import os
load_dotenv()
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_history = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    chat_history.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful teacher."}
        ] + chat_history
    )

    reply = response.choices[0].message.content

    chat_history.append({
        "role": "assistant",
        "content": reply
    })

    print(f"AI: {reply}\n")