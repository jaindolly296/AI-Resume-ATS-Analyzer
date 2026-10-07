import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Page configuration
st.set_page_config(
    page_title="AI Resume ATS Analyzer",
    page_icon="📄",
    layout="centered"
)


# Title
st.title("📄 AI Resume ATS Analyzer")
st.write(
    "By Dolly Jain"
)

st.write(
    "Upload Resume + Job Description and get ATS score using AI."
)


# Check API key

if GROQ_API_KEY is None:

    st.error(
        "❌ GROQ_API_KEY not found. Add it in Render Environment Variables."
    )

    st.stop()



# Groq client

client = Groq(
    api_key=GROQ_API_KEY
)



# Upload Resume

resume_file = st.file_uploader(
    "📄 Upload Resume PDF",
    type=["pdf"]
)



# Job Description

job_description = st.text_area(
    "📝 Paste Job Description"
)



# Extract PDF text

def extract_text(pdf_file):

    text = ""

    reader = PdfReader(pdf_file)


    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"


    return text




# Main logic

if resume_file is not None:


    with st.spinner(
        "Reading Resume..."
    ):

        resume_text = extract_text(
            resume_file
        )


    st.success(
        "✅ Resume Uploaded Successfully"
    )


    st.info(
        f"Resume characters: {len(resume_text)}"
    )



    if st.button(
        "🚀 Analyze Resume"
    ):


        if job_description.strip() == "":


            st.warning(
                "⚠️ Please paste Job Description"
            )


        else:


            try:


                prompt = f"""

You are an expert ATS Resume Analyzer.

Analyze the resume against the job description.

Resume:

{resume_text}


Job Description:

{job_description}


Provide:

1. ATS Match Score out of 100

2. Missing Keywords

3. Resume Strengths

4. Resume Weaknesses

5. Improvement Suggestions

6. Final Verdict

"""


                with st.spinner(
                    "Analyzing with AI..."
                ):


                    response = client.chat.completions.create(

                        model="llama-3.1-8b-instant",

                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],

                        temperature=0.2

                    )


                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )


                st.subheader(
                    "📊 ATS Analysis Result"
                )


                st.write(answer)



            except Exception as e:


                st.error(
                    f"Error from Groq API: {e}"
                )
