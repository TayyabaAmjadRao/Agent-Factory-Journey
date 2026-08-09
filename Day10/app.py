import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🤖 AI Study Assistant")
st.write("Learn any topic — Your personal AI Teacher!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

topic = st.chat_input("Type any topic to learn...")

if topic:
    st.session_state.messages.append({"role": "user" , "content": topic})

    with st.chat_message("user"):
        st.write(topic)

    response= client.chat.completions.create(
         model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert teacher. Explain topics clearly with examples. Give 5 key points, 2 real life examples, and 3 practice questions."}
        ] + st.session_state.messages
    )    
    reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply })

    with st.chat_message("assistant"):
        st.write(reply)
