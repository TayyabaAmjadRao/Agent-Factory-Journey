import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Customer Memory Agent", page_icon="🧠")
st.title("🧠 Customer Memory Agent")
st.write("I remember everything about you!")

# Customer memory store
if "customer_memory" not in st.session_state:
    st.session_state.customer_memory = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar — Customer Profile
st.sidebar.title("👤 Customer Profile")
customer_name = st.sidebar.text_input("Your Name")

if customer_name:
    if customer_name not in st.session_state.customer_memory:
        st.session_state.customer_memory[customer_name] = {
            "name": customer_name,
            "preferences": [],
            "history": [],
            "address": "",
            "phone": ""
        }

    # Show profile
    profile = st.session_state.customer_memory[customer_name]
    st.sidebar.write(f"**Name:** {profile['name']}")
    st.sidebar.write(f"**Phone:** {profile['phone'] or 'Not provided'}")
    st.sidebar.write(f"**Address:** {profile['address'] or 'Not provided'}")
    st.sidebar.write(f"**Preferences:** {', '.join(profile['preferences']) or 'None yet'}")
    st.sidebar.write(f"**Total Orders:** {len(profile['history'])}")

    # Chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Chat with your personal assistant...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Build memory context
        memory_context = f"""
Customer Profile:
- Name: {profile['name']}
- Phone: {profile['phone']}
- Address: {profile['address']}
- Preferences: {profile['preferences']}
- Order History: {profile['history']}

You are a personal shopping assistant. 
Remember and update customer information when they share it.
Be personalized and helpful based on their history.
If customer shares phone/address/preference, acknowledge it.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": memory_context}
            ] + st.session_state.messages
        )

        reply = response.choices[0].message.content

        # Update memory based on conversation
        if "phone" in user_input.lower() or any(char.isdigit() for char in user_input):
            digits = ''.join(filter(str.isdigit, user_input))
            if len(digits) > 7:
                st.session_state.customer_memory[customer_name]["phone"] = digits

        if "address" in user_input.lower() or "live" in user_input.lower():
            st.session_state.customer_memory[customer_name]["address"] = user_input

        if "like" in user_input.lower() or "prefer" in user_input.lower() or "love" in user_input.lower():
            st.session_state.customer_memory[customer_name]["preferences"].append(user_input)

        if "order" in user_input.lower() or "buy" in user_input.lower() or "purchase" in user_input.lower():
            st.session_state.customer_memory[customer_name]["history"].append(user_input)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

else:
    st.info("👈 Please enter your name in the sidebar to start!")