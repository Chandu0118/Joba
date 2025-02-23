import streamlit as st
from backend import process_cv_and_generate_cover_letter, analyze_feedback
import os

# Custom CSS inspired by KLIPSAN (yellow and black, bold typography)
st.markdown("""
    <style>
    .main {
        background-color: #ffffff; /* White background like KLIPSAN */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stTitle {
        color: #000000; /* Black title color */
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        font-family: 'Arial', sans-serif; /* Modern font */
        background: linear-gradient(to right, #f1c40f, #f39c12); /* Yellow gradient like KLIPSAN */
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    .stHeader {
        color: #000000; /* Black headers */
        font-size: 28px;
        font-weight: bold;
        margin-top: 20px;
    }
    .stTextInput, .stSelectbox, .stFileUploader {
        background-color: #ffffff; /* White inputs */
        border: 2px solid #f1c40f; /* Yellow border */
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stButton {
        background-color: #f1c40f; /* Yellow button */
        color: #000000;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton:hover {
        background-color: #f39c12; /* Darker yellow on hover */
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }
    .stSuccess {
        background-color: #2ecc71; /* Green for success */
        color: white;
        padding: 10px;
        border-radius: 8px;
        font-size: 16px;
    }
    .stError {
        background-color: #e74c3c; /* Red for errors */
        color: white;
        padding: 10px;
        border-radius: 8px;
        font-size: 16px;
    }
    .section {
        margin-bottom: 20px;
        padding: 15px;
        background-color: #f9f9f9; /* Light gray background for sections */
        border-radius: 8px;
        border: 1px solid #f1c40f;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description (English UI)
st.markdown('<div class="main"><h1 class="stTitle">Automated CV & Cover Letter Generator</h1>', unsafe_allow_html=True)
st.write("Upload your CV, provide a job description, and let us tailor your application with Grok.")

# Use containers for structured layout
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="stHeader">Upload Your CV</h2>', unsafe_allow_html=True)
    cv_file = st.file_uploader("Upload your CV (.docx)", type=["docx"], help="Drag and drop or browse files. Limit 200MB per .docx file")
    if cv_file:
        # Save uploaded CV to local directory
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        cv_path = os.path.join("uploads", cv_file.name)
        with open(cv_path, "wb") as f:
            f.write(cv_file.getbuffer())
        st.success(f"CV uploaded successfully: {cv_file.name}")
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="stHeader">Select LLM</h2>', unsafe_allow_html=True)
    selected_llm = st.selectbox("Select LLM:", ["Grok"], help="Currently only Grok is supported")
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="stHeader">Enter Job Details</h2>', unsafe_allow_html=True)
    job_description = st.text_area("Enter Job Description:", help="Paste the job description here")
    job_url = st.text_input("Or provide a URL:", help="Enter a URL for the job description")
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="stHeader">Select Output Language</h2>', unsafe_allow_html=True)
    output_language = st.selectbox("Select Output Language:", ["German", "English"], help="Choose the language for the output")
    st.markdown('</div>', unsafe_allow_html=True)

# Generate Button
if st.button("Generate", help="Generate updated CV and cover letter using Grok"):
    try:
        if not cv_file or not (job_description or job_url):
            st.error("Please upload a CV and provide a job description or URL.")
        else:
            st.success("Processing with Grok...")
            updated_cv_path, cover_letter_path = process_cv_and_generate_cover_letter(
                cv_path, job_description or job_url, selected_llm, output_language
            )
            st.download_button(
                label="Download Updated CV",
                data=open(updated_cv_path, "rb").read(),
                file_name="updated_cv.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                help="Download your tailored CV as a .docx file"
            )
            st.download_button(
                label="Download Cover Letter",
                data=open(cover_letter_path, "rb").read(),
                file_name="cover_letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                help="Download your tailored cover letter as a .docx file"
            )
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Feedback Loop
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="stHeader">Provide Feedback</h2>', unsafe_allow_html=True)
    reuploaded_cv = st.file_uploader("Re-upload your modified CV for feedback:", type=["docx"], help="Drag and drop or browse files. Limit 200MB per .docx file")
    if reuploaded_cv:
        # Save re-uploaded CV to local directory
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        reuploaded_cv_path = os.path.join("uploads", reuploaded_cv.name)
        with open(reuploaded_cv_path, "wb") as f:
            f.write(reuploaded_cv.getbuffer())
        st.success("Modified CV uploaded successfully.")
        differences = analyze_feedback(cv_path, reuploaded_cv_path)
        st.write(f"Changes detected: {differences}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
