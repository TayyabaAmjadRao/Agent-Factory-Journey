import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Email Writer Agent", page_icon="✉️")
st.title("✉️ Business Email Writer Agent")
st.write("Automatically writes professional email replies!")

st.subheader("1️⃣ Select Email Type")
email_type = st.selectbox(
    "What type of email is this?",
    ["Complaint", "Inquiry", "Follow-up", "General/Unknown"]
)

EMAIL_INSTRUCTIONS = {
    "Complaint": "Write an empathetic, apologetic response. Acknowledge the issue, apologize sincerely, and offer a clear solution or next step.",
    "Inquiry": "Write a friendly, informative response. Answer their question clearly and offer additional help.",
    "Follow-up": "Write a professional, concise response. Be direct and provide status update or next steps.",
    "General/Unknown": "Write a polite holding response saying a human team member will respond shortly. Do not make promises or commitments."
}

st.subheader("2️⃣ Client Details")
client_name = st.text_input("Client's Name")
client_email = st.text_area("Client's email...", height=150)

st.subheader("3️⃣ Additional Context (Optional)")
context = st.text_input("Any specific details? (e.g. order number, refund amount)")

if st.button("✍️ Generate Reply"):
    if client_email and client_name:
        with st.spinner("Writing professional reply..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": f"""You are a professional business email writer.
                    
Email Type: {email_type}
Style Instructions: {EMAIL_INSTRUCTIONS[email_type]}

Write a complete, professional email reply. Include:
- Appropriate greeting using the client's name
- Body addressing their concern
- Professional closing

Keep it concise and business-appropriate."""},
                    {"role": "user", "content": f"""Client Name: {client_name}

Client's Original Email:
{client_email}

Additional Context: {context if context else 'None provided'}

Write the reply email addressing them by name."""}
                ]
            )

        st.success("Reply Generated!")
        st.markdown("### 📧 Generated Email")
        st.text_area("Copy this reply:", value=response.choices[0].message.content, height=300)

    else:
        st.warning("Please provide client's name and email!")

st.sidebar.title("📋 How to Use")
st.sidebar.write("1. Select email type")
st.sidebar.write("2. Enter client name & email")
st.sidebar.write("3. Add context if needed")
st.sidebar.write("4. Generate professional reply!")