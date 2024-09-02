import streamlit as st
import requests
import fitz  # PyMuPDF for PDF files
#from docx import Document  # python-docx for Word documents

# Define the FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000/analyze"

st.title("Supplier Agreement Analysis Tool")

#st.header("Upload Supplier Agreement Document")
# Input form
st.header("Input Supplier Agreements")
#uploaded_file = st.file_uploader("Upload PDF or DOCX file", type=["pdf", "docx"])
# Agreement text input
agreement_text = st.text_area("Enter Supplier Agreement Text", height=200)


communication_text = st.text_area("Enter Communication Text for Sentiment Analysis", height=100)

# def extract_text_from_pdf(file):
#     """Extract text from a PDF file."""
#     text = ""
#     with fitz.open(stream=file.read(), filetype="pdf") as doc:
#         for page in doc:
#             text += page.get_text()
#     return text

# def extract_text_from_docx(file):
#     """Extract text from a DOCX file."""
#     doc = Document(file)
#     text = "\n".join([para.text for para in doc.paragraphs])
#     return text

# # Extract text from uploaded file
# if uploaded_file is not None:
#     file_type = uploaded_file.type
#     if file_type == "application/pdf":
#         agreement_text = extract_text_from_pdf(uploaded_file)
#     elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#         agreement_text = extract_text_from_docx(uploaded_file)
#     else:
#         st.error("Unsupported file type.")
# else:
#     agreement_text = None

if st.button("Analyze"):
    if agreement_text and communication_text:
        # Send data to FastAPI backend
        payload = {
            "text": agreement_text,
            "communication": communication_text
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()

            # Display results
            st.subheader("Analysis Results")
            st.write(result)
            # st.write(f"Supplier: {result.get('Supplier')}")
            # st.write(f"Buyer: {result.get('Buyer')}")
            # st.write(f"Effective Date: {result.get('Effective Date')}")
            # st.write(f"Payment Terms: {result.get('Payment Terms')}")
            # st.write(f"Warranty: {result.get('Warranty')}")
            # st.write(f"Pricing: {result.get('Pricing')}")
            # st.write(f"Delivery Time: {result.get('Delivery Time')}")
            # st.write(f"Governing Law: {result.get('Governing Law')}")
            # st.write(f"Sentiment Score: {result.get('Sentiment Score')}")
        else:
            st.error(f"Error: {response.status_code} - {response.json()['detail']}")
    else:
        st.warning("Please upload a file and fill out all fields before submitting.")
