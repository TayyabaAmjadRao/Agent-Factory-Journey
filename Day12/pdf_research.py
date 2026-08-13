import streamlit as st
from groq import Groq
from ddgs import DDGS
from dotenv import load_dotenv
import os
import pypdf

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="PDF + Research Assistant", page_icon="📚")
st.title("📚 PDF + Research Assistant")
st.write("Upload a PDF or search the web — AI will analyze it!")

# Tabs
tab1, tab2 = st.tabs(["📄 PDF Analyzer", "🔍 Web Research"])

# Tab 1 — PDF
with tab1:
    st.subheader("Upload your PDF")
    pdf_file = st.file_uploader("Choose a PDF file", type="pdf")
    question = st.text_input("Ask a question about the PDF...")

    if pdf_file and question:
        # Read PDF
        pdf_reader = pypdf.PdfReader(pdf_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()

        if pdf_text:
            with st.spinner("AI is reading the PDF..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant. Answer questions based on the provided PDF content only."},
                        {"role": "user", "content": f"PDF Content:\n{pdf_text}\n\nQuestion: {question}"}
                    ]
                )
            st.success("Done!")
            st.markdown("### 📊 Answer")
            st.write(response.choices[0].message.content)
        else:
            st.error("Could not read PDF! Please try another file.")

# Tab 2 — Web Research
with tab2:
    st.subheader("Search the Web")
    query = st.text_input("What do you want to research?")

    if st.button("🔍 Search"):
        if query:
            with st.spinner("Searching..."):
                results = DDGS().text(query, max_results=5)
                search_data = ""
                for r in results:
                    search_data += f"Title: {r['title']}\nInfo: {r['body']}\n\n"

            with st.spinner("AI analyzing..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a research assistant. Give structured summary with Key Findings and Conclusion."},
                        {"role": "user", "content": f"Topic: {query}\n\nResults:\n{search_data}"}
                    ]
                )

            st.success("Research Complete!")
            st.write(response.choices[0].message.content)

            st.markdown("### 🔗 Sources")
            for r in results:
                st.write(f"• [{r['title']}]({r['href']})")