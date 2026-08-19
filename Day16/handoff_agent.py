import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Agent Handoff System", page_icon="🔄")
st.title("🔄 Agent Handoff System")
st.write("Agents hand off to specialists automatically!")

AGENTS = {
    "General Agent": {
        "instructions": """You are a friendly General Customer Service Agent.
        Handle general queries. 
        If user has TECHNICAL problem — say exactly: 'HANDOFF:Technical Agent'
        If user has BILLING problem — say exactly: 'HANDOFF:Billing Agent'
        If user has COMPLAINT — say exactly: 'HANDOFF:Complaint Agent'
        Otherwise handle it yourself.""",
        "icon": "👋"
    },
    "Technical Agent": {
        "instructions": """You are an expert Technical Support Agent.
        Solve technical problems professionally.
        Provide step-by-step solutions.
        If resolved, ask if they need anything else.""",
        "icon": "🔧"
    },
    "Billing Agent": {
        "instructions": """You are a Billing Specialist Agent.
        Handle payment issues, refunds, and billing queries professionally.
        Always verify before processing refunds.
        Be empathetic but follow company policy.""",
        "icon": "💳"
    },
    "Complaint Agent": {
        "instructions": """You are a Complaint Resolution Agent.
        Handle complaints with empathy and professionalism.
        Always apologize first, then solve.
        Offer compensation when appropriate.""",
        "icon": "🤝"
    }
}

def run_agent(agent_name, messages):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": AGENTS[agent_name]["instructions"]}
        ] + messages
    )
    return response.choices[0].message.content

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_agent" not in st.session_state:
    st.session_state.current_agent = "General Agent"

agent = st.session_state.current_agent
st.info(f"{AGENTS[agent]['icon']} Currently talking to: **{agent}**")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner(f"{agent} is responding..."):
        reply = run_agent(st.session_state.current_agent, st.session_state.messages)

    if "HANDOFF:" in reply:
        new_agent = reply.split("HANDOFF:")[1].strip()
        new_agent = new_agent.split("\n")[0].strip()
        if new_agent in AGENTS:
            st.session_state.current_agent = new_agent
            st.warning(f"🔄 Handoff to **{new_agent}**!")
            reply = run_agent(new_agent, st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)

if st.button("🔄 Start New Conversation"):
    st.session_state.messages = []
    st.session_state.current_agent = "General Agent"
    st.rerun()