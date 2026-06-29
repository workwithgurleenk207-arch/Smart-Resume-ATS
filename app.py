from dotenv import load_dotenv
import io
import base64
load_dotenv()
from pdf2image import convert_from_path 
import streamlit as st 
import os
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response (input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
  if uploaded_file is not None:
    images = pdf2image.convert_from_bytes(uploaded_file.read()), 
    
    first_page = images[0]
    

    # Convert to bytes
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    pdf_parts = [
             {
              "mime_type": "image/jpeg",
              "data": base64.b64encode(img_byte_arr).decode() # encode to base64
}
    ]
 
    return pdf_parts
  else:
    raise FileNotFoundError("No File Uploaded")

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ", key="input")
uploaded_file=st.file_uploader("Upload your resume (PDF)...",type=["pdf"])


if uploaded_file is not None:
  st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about my resume")
submit2 = st.button("How can I improve my resume")
submit3 = st.button("What are the keywords that are missing")
submit4 = st.button("Percentage match")

input_prompt1 = """
Review a resume against a job description.
Act like a human HR professional.
Evaluate whether the candidate is suitable.
Highlight strengths and weaknesses.
Provide professional feedback.
"""

input_prompt3 = """
Compare the resume with the job description.
Calculate an ATS match percentage.
Identify missing keywords.
Explain why the resume matches or doesn't match.
"""

if submit1:
  if uploaded_file is not None:
   pdf_content=input_pdf_setup(uploaded_file)
   response=get_gemini_response (input_prompt1, pdf_content, input_text)
   st.subheader("The Repsonse is")
   st.write(response)
  else:
   st.write("Please uplaod the resume")
   
elif submit3:
    if uploaded_file is not None:
     pdf_content=input_pdf_setup(uploaded_file)
     response=get_gemini_response(input_prompt3, pdf_content, input_text)
     st.subheader("The Repsonse is")
     st.write(response)
    else:
     st.write("Please uplaod the resume")
