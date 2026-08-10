import streamlit as st
from groq import Groq
from ddgs import DDGS
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Page Setup
st.set_page_config(page_title="Live Research Assistant", page_icon="🔍")
st.title("🔍 Live Research Assistant")
st.write("Search anything — Get AI-powered research results!")

# Search History Memory
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# Search Input
query = st.text_input("What do you want to research?", placeholder="e.g. Latest AI trends 2026")

if st.button("🔍 Search"):
    if query:
        # Check Duplicate
        if query in st.session_state.search_history:
            st.warning("You already searched this! Try a different topic.")
        else:
            st.session_state.search_history.append(query)

            with st.spinner("Searching the web..."):
                # Web Search
                results = DDGS().text(query, max_results=5)
                search_data = ""
                for r in results:
                    search_data += f"Title: {r['title']}\n"
                    search_data += f"Info: {r['body']}\n\n"

            with st.spinner("AI is analyzing results..."):
                # AI Analysis
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a research assistant. Analyze search results and give a clear, structured summary. Include: Key Findings, Important Facts, and Conclusion."},
                        {"role": "user", "content": f"Research topic: {query}\n\nSearch Results:\n{search_data}"}
                    ]
                )

            reply = response.choices[0].message.content

            # Display Results
            st.success("Research Complete!")
            st.markdown("### 📊 Research Report")
            st.write(reply)

            # Sources
            st.markdown("### 🔗 Sources")
            for r in results:
                st.write(f"• [{r['title']}]({r['href']})")

# Search History Sidebar
st.sidebar.title("📚 Search History")
if st.session_state.search_history:
    for h in st.session_state.search_history:
        st.sidebar.write(f"• {h}")
else:
    st.sidebar.write("No searches yet!")