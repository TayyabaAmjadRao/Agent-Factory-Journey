import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Agent class — SDK style
class Agent:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

    def run(self, user_input, history=[]):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": self.instructions}
            ] + history + [
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content

# Define Agents — SDK style
research_agent = Agent(
    name="Research Assistant",
    instructions="""You are a professional research assistant.
    Help users find information, analyze topics, and provide clear summaries.
    Always be accurate, helpful, and professional."""
)

st.set_page_config(page_title="Professional AI Agent", page_icon="🤖")
st.title("🤖 Professional AI Agent")
st.write("Built with Agent SDK Style — Powered by Groq!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Agent is thinking..."):
        reply = research_agent.run(user_input, st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)