import streamlit as st
from backend import process_cv_and_generate_cover_letter, analyze_feedback
import os

# Title and description (English UI)
st.title("Automated CV & Cover Letter Generator")
st.write("Upload your CV, provide a job description, and let us tailor your application with Grok.")

# Step 1: Upload CV
cv_file = st.file_uploader("Upload your CV (.docx)", type=["docx"])
if cv_file:
    # Save uploaded CV to local directory
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    cv_path = os.path.join("uploads", cv_file.name)
    with open(cv_path, "wb") as f:
        f.write(cv_file.getbuffer())
    st.success(f"CV uploaded successfully: {cv_file.name}")

# Step 2: Choose LLM (Only Grok for now)
selected_llm = st.selectbox("Select LLM:", ["Grok"])  # Restricted to Grok

# Step 3: Input Job Description
job_description = st.text_area("Enter Job Description:")
job_url = st.text_input("Or provide a URL:")

# Step 4: Language Selection
output_language = st.selectbox("Select Output Language:", ["German", "English"])

# Step 5: Generate Button
if st.button("Generate"):
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
            )
            st.download_button(
                label="Download Cover Letter",
                data=open(cover_letter_path, "rb").read(),
                file_name="cover_letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Step 6: Feedback Loop
reuploaded_cv = st.file_uploader("Re-upload your modified CV for feedback:", type=["docx"])
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
