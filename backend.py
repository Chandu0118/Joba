# backend.py

from docx import Document
import requests
from langchain.llms import OpenAI, DeepSeek, Qwen
from grok_api import GrokModel

def process_cv_and_generate_cover_letter(cv_path, job_input, selected_llm, output_language):
    # Load CV
    cv_doc = Document(cv_path)
    cv_text = "\n".join([para.text for para in cv_doc.paragraphs])

    # Process Job Description
    if job_input.startswith("http"):
        response = requests.get(job_input)
        job_description = response.text
    else:
        job_description = job_input

    # Initialize LLM
    if selected_llm == "ChatGPT":
        llm = OpenAI(model_name="gpt-3.5-turbo")
    elif selected_llm == "Grok":
        llm = GrokModel(model_name="grok-1")
    elif selected_llm == "Qwen":
        llm = Qwen()
    elif selected_llm == "DeepSeek":
        llm = DeepSeek(model_name="deepseek-coder")

    # Generate CV Updates
    prompt_cv = (
        f"Update the following CV based on the job description. "
        f"Do not carry over information from the job description unless explicitly mentioned. "
        f"Output language: {output_language}.\n\n"
        f"CV:\n{cv_text}\n\nJob Description:\n{job_description}"
    )
    updated_cv_text = llm(prompt_cv)

    # Save Updated CV
    updated_cv_doc = Document()
    updated_cv_doc.add_paragraph(updated_cv_text)
    if not os.path.exists("output"):
        os.makedirs("output")
    updated_cv_path = "output/updated_cv.docx"
    updated_cv_doc.save(updated_cv_path)

    # Generate Cover Letter
    prompt_cover = (
        f"Write a professional cover letter in {output_language} for the following job description:\n\n"
        f"{job_description}\n\nCV:\n{cv_text}"
    )
    cover_letter = llm(prompt_cover)

    return updated_cv_path, cover_letter


def analyze_feedback(original_cv_path, updated_cv_path):
    original_doc = Document(original_cv_path)
    updated_doc = Document(updated_cv_path)

    original_text = "\n".join([para.text for para in original_doc.paragraphs])
    updated_text = "\n".join([para.text for para in updated_doc.paragraphs])

    # Compare texts and log differences for learning
    differences = set(updated_text.split()) - set(original_text.split())
    return ", ".join(differences)