from dotenv import load_dotenv
import os
load_dotenv()
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

topic= input("Which topic do you want to learn? ")
message = client.chat.completions.create(
    model= "llama-3.3-70b-versatile",
    messages= [
        {
            "role": "user",
            "content": f""" You are an expert teacher.
            TOPIC: {topic}
            Task 1: Explain in 5 simple points.
            Task 2: Give 3 real life examples.
            Task 3: Create 5 practice questions.
            Output: Clean and structured."""
        }
    ]
)
        
print(message.choices[0].message.content)
