from dotenv import load_dotenv
import os

load_dotenv()
from groq import Groq  

client = Groq(api_key=os.getenv("GROQ_API_KEY"))  

message = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    max_tokens=1024,
    messages=[
        # {"role":"user", "content":"Tell me about agents in 5 points"}
        # {"role":"user", "content":"You are my teacher, teach me the basic or agents in 5 points"}
        # {"role":"user", "content":"You are teacher,  Teach me About agent,  I am intermediate level, In 5 points that are in maximum 2 lines and easy to undrestand, Output must be a intermediate-friendly"}
        {"role":"user", "content":"You are an AI Teacher.I already know basic Python and have heard about AI agents.Teach me what AI Agents are in 5 points.Each point max 2 lines.Use simple English.Give one real-life example in each point.Output: Numbered list with bold headings.Success: I should understand without googling anything."}
    ]
)

print(message.choices[0].message.content)

