import streamlit as st
import PyPDF2
import docx
import google.generativeai as genai
import os
from dotenv import load_dotenv  


load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text


def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def analyze_resume_with_gemini(resume_text, target_company, interview_type):
    # Define the prompt for Gemini
    prompt = f"""
    Analyze the following resume for a candidate targeting {target_company} for a {interview_type} interview.
    Provide the following:
    1. An overall score out of 10.
    2. Scores out of 10 for key parameters like clarity, relevance, skills, experience, and formatting.
    3. Specific suggestions for improvement.

    Resume:
    {resume_text}
    """

    # Use Gemini to generate a response
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text


st.title("Resume Rater and Improver")


uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])


target_company = st.text_input("Target Company")
interview_type = st.selectbox("Type of Interview", ["Technical", "Behavioral", "Mixed"])

if uploaded_file is not None:
    
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(uploaded_file)

    
    st.subheader("Extracted Text from Resume")
    st.text(text)

    
    if st.button("Analyze Resume"):
        st.write("Analyzing your resume...")
        analysis_result = analyze_resume_with_gemini(text, target_company, interview_type)

       
        st.subheader("Analysis Results")
        st.write(analysis_result)
