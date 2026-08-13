import streamlit as st
from groq import Groq
from ddgs import DDGS
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Multi-Agent System", page_icon="🤖")
st.title("🤖 Multi-Agent System")
st.write("Manager assigns tasks to specialized AI Workers!")

# Agent definitions
AGENTS = {
    "Research Agent": "You are a Research Agent. Your ONLY job is to search and find information. Give factual, structured research findings.",
    "Analyzer Agent": "You are an Analyzer Agent. Your ONLY job is to analyze data and find patterns, insights, and conclusions.",
    "Writer Agent": "You are a Writer Agent. Your ONLY job is to write clear, professional, engaging content based on provided information."
}

MANAGER_PROMPT = """You are a Manager Agent. 
Your job is to read the user request and decide which agent should handle it.
Reply with ONLY one of these exact words:
- Research Agent
- Analyzer Agent  
- Writer Agent

User request: """

def run_manager(user_input):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": MANAGER_PROMPT + user_input}
        ]
    )
    return response.choices[0].message.content.strip()

def run_worker(agent_name, user_input):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": AGENTS[agent_name]},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# UI
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Type your request...")

if user_input:
    with st.spinner("Manager is deciding..."):
        assigned_agent = run_manager(user_input)
        
        # Clean up response
        for agent in AGENTS.keys():
            if agent.lower() in assigned_agent.lower():
                assigned_agent = agent
                break

    st.info(f"📋 Manager assigned to: **{assigned_agent}**")

    with st.spinner(f"{assigned_agent} is working..."):
        result = run_worker(assigned_agent, user_input)

    st.session_state.history.append({
        "user": user_input,
        "agent": assigned_agent,
        "result": result
    })

# Show history
for item in st.session_state.history:
    with st.chat_message("user"):
        st.write(item["user"])
    with st.chat_message("assistant"):
        st.write(f"**[{item['agent']}]**")
        st.write(item["result"])