from httpx import options
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np
from Common import *



from google.cloud import vision
from google.oauth2 import service_account
import google.generativeai as genai
from dotenv import load_dotenv
import os
import io
import json


def get_certificate_info():    

    st.title("Certificate Information 📜")
    st.write("Enter your certificate details")

    st.subheader("Certificate Details")

    col1, col2 = st.columns(2)
    with col1:
        put_selectbox(CERTIFICATION_TYPE, "Certification Type", ["Select Type", "Trade Certification", "Safety Certification", "Other"], index=0)
        put_text_input(CERTIFICATE_ID, "Certificate Id", "Enter the certificate id number")
        put_text_input(CERTIFICATE_DESCRIPTION, "Certificate Description", "Enter a brief description of the certificate")
        

    with col2:
        put_date_input(CERTIFICATE_ISSUE_DATE, "Issue Date", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        put_date_input(CERTIFICATE_EXPIRY_DATE, "Expiry Date", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        #put_text_input(CERTIFICATE_ISSUED_BY, "Issued By", "Enter the organization that issued the certificate")


    st.write("Upload Certificate Image")

    # Load .env variables
    load_dotenv()

    # Setup credentials
    google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    credentials = service_account.Credentials.from_service_account_file(google_application_credentials)
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)

    print("Google Application Credentials:", google_application_credentials)
    print("Credentials loaded successfully.")

    # Initialize Vision client
    vision_client = vision.ImageAnnotatorClient(credentials=credentials)
    print("Vision client initialized.")

    # Extract text from uploaded image
    def extract_text_from_image(uploaded_file):
        content = uploaded_file.read()
        image = vision.Image(content=content)
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description if texts else ""

    # Use Gemini to extract structured fields
    def extract_fields_with_gemini(ocr_text):
        print("Extracting fields with Gemini...")
        model = genai.GenerativeModel(
            'gemini-1.5-flash-latest',
            system_instruction="You are an AI assistant. Extract structured fields from OCR text and return JSON. If a field is missing, return an empty string."
        )

        prompt = f"""
        Extract the following fields from the OCR text:
        - worker_full_name
        - certification_name
        - certification_id
        - issue_date (MM/DD/YYYY)
        - expiry_date (MM/DD/YYYY)

        Return the result as a JSON object.

        --- OCR TEXT ---
        {ocr_text}
        --- END OF TEXT ---
        """

        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )

        try:
            return json.loads(response.text)
        except Exception as e:
            return {"error": "Failed to parse Gemini response", "raw": response.text}

    # --- Streamlit UI ---
    
    #st.set_page_config(page_title="Certification Card Reader", layout="centered")
    

    uploaded_file = st.file_uploader("Upload a certification image", type=["jpg", "jpeg", "png"])

    print("D")

    if uploaded_file is not None:
        print("File loaded")
        print("Uploaded file:", uploaded_file.name)

    
        cola, colb = st.columns(2)


        with cola:
            st.image(uploaded_file, caption="Uploaded image", use_container_width=True)

        with colb:
            with st.spinner("Running OCR..."):
                ocr_text = extract_text_from_image(uploaded_file)
                st.subheader("🔍 Extracted OCR Text")
                st.text_area("Raw OCR Output", ocr_text, height=200)

            with st.spinner("Asking Gemini to extract fields..."):
                result = extract_fields_with_gemini(ocr_text)

            st.subheader("📋 Structured Output")
            st.json(result)

        #st.session_state[CERTIFICATE_IMAGE] = uploaded_file
        #st.image(uploaded_file, caption="Uploaded Certificate Image", use_column_width=True)