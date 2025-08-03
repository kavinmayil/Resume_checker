import streamlit as st
import PyPDF2
import os
import re

ROLE_KEYWORDS = {
    "data analyst": {"python", "excel", "sql", "power bi", "statistics", "data visualization"},
    "web developer": {"html", "css", "javascript", "react", "node.js", "api"},
    "ai engineer": {"python", "tensorflow", "keras", "machine learning", "deep learning", "nlp"},
    "embedded engineer": {"c", "c++", "microcontroller", "i2c", "spi", "uart", "arduino", "raspberry pi", "pcb"},
    "cloud engineer": {"aws", "azure", "gcp", "docker", "kubernetes", "terraform", "devops", "ci/cd"},
}

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text.lower()

def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    return set(text.lower().split())

def analyze_resume(resume_text, role_keywords):
    resume_words = clean_text(resume_text)
    matched = resume_words.intersection(role_keywords)
    missing = role_keywords - resume_words
    match_percent = (len(matched) / len(role_keywords)) * 100
    return matched, missing, match_percent

st.title("🪩 Resume Analyzer")

role = st.selectbox("🎯 Select Role Applied For", list(ROLE_KEYWORDS.keys()))
resume_name = st.text_input("📄 Enter resume file name (without .pdf)")

if resume_name:
    resume_path = f"{resume_name}.pdf"
    
    if os.path.exists(resume_path):
        with open(resume_path, "rb") as file:
            resume_text = extract_text_from_pdf(file)
            matched, missing, score = analyze_resume(resume_text, ROLE_KEYWORDS[role])

            st.subheader("📊 Resume Analysis Report")
            st.markdown(f"🔹 **Match Score:** `{score:.2f}%`")

            st.markdown("✅ **Matched Skills**")
            st.write(', '.join(sorted(matched)) if matched else "None")

            st.markdown("❌ **Missing Skills**")
            st.write(', '.join(sorted(missing)) if missing else "None")

            # Check for important sections
            st.markdown("📌 **Section Check**")
            st.success("🎯 Career Objective found ✅" if "objective" in resume_text else "⚠️ Career Objective missing")
            st.success("📁 Projects section found ✅" if "project" in resume_text else "⚠️ Projects section missing")

            # Suitability conclusion
            if score >= 70:
                st.success("🟢 This resume is suitable for the selected role.")
            else:
                st.error("🔴 Resume not suitable. Add more relevant skills.")
    else:
        st.error("📂 Resume file not found. Please place it in the same directory.")
