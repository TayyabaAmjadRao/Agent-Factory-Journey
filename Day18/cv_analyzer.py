import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import pypdf

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="CV Analyzer Agent", page_icon="📄")
st.title("📄 CV Analyzer Agent")
st.write("Match candidates to job requirements automatically!")

# Job Requirements Input
st.subheader("1️⃣ Job Requirements")
job_requirements = st.text_area(
    "Paste job requirements here...",
    placeholder="e.g. Looking for a Python developer with 2+ years experience, knowledge of AI/ML, good communication skills..."
)

# CV Upload
st.subheader("2️⃣ Upload Candidate CV")
cv_file = st.file_uploader("Choose CV (PDF)", type="pdf")

if st.button("🔍 Analyze CV"):
    if job_requirements and cv_file:
        # Extract PDF text
        pdf_reader = pypdf.PdfReader(cv_file)
        cv_text = ""
        for page in pdf_reader.pages:
            cv_text += page.extract_text()

        with st.spinner("AI is analyzing the CV..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": """You are an expert HR recruiter and CV analyzer.
                    Analyze the CV against job requirements and provide:
                    
                    1. MATCH SCORE (0-100%)
                    2. STRENGTHS (matching skills/experience)
                    3. MISSING REQUIREMENTS (what candidate lacks)
                    4. RECOMMENDATION (Strong Match / Good Match / Weak Match / Not Suitable)
                    5. SUMMARY (2-3 lines about the candidate)
                    
                    Be objective and specific."""},
                    {"role": "user", "content": f"""
Job Requirements:
{job_requirements}

Candidate CV:
{cv_text}

Analyze this candidate against the job requirements."""}
                ]
            )

        st.success("Analysis Complete!")
        st.markdown("### 📊 Analysis Report")
        st.write(response.choices[0].message.content)

    else:
        st.warning("Please provide both job requirements and CV!")

st.sidebar.title("💼 How to Use")
st.sidebar.write("1. Paste job requirements")
st.sidebar.write("2. Upload candidate CV")
st.sidebar.write("3. Click Analyze")
st.sidebar.write("4. Get instant match score!")