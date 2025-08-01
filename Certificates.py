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




    processing_certificate = st.session_state.get(PROCESSING_CERTIFICATE, False)
    cancelling_certificate = st.session_state.get(CANCEL_NEW_CERTIFICATE, False)

    print("Processing Certificate:", processing_certificate)
    print("Cancelling Certificate:", cancelling_certificate)

    if "cert_file_key" not in st.session_state:
        st.session_state.cert_file_key = "cert_file_1"


    st.title("Certificate Information 📜")


    certs = st.session_state.get(CERTIFICATIONS, [])
    if certs:
        st.subheader("Your Certificates")        

        for cert in certs:
            col1,col2,col3 = st.columns([0.3, 0.15, 0.55])
            with col1:
                st.write(f"**Type:** {cert.type}")
                st.write(f"**ID:** {cert.id}")
                st.write(f"**Description:** {cert.description}")
                st.write(f"**Issue Date:** {cert.issue_date}")
                st.write(f"**Expiry Date:** {cert.expiry_date}")
            with col2:
                if cert.image:
                    st.image(cert.image, caption="Certificate Image", use_container_width=True)
                else:
                    st.write("No image uploaded")
        
        st.markdown("---")

    st.write("Enter your certificate details")
    st.subheader("Certificate Details")

    col1, col2 = st.columns(2)
    with col1:
        put_selectbox(CERTIFICATION_TYPE, "Certification Type", CERTIFICATION_TYPES, index=0)
        put_text_input(CERTIFICATE_ID, "Certificate Id", "Enter the certificate id number")
        put_text_input(CERTIFICATE_DESCRIPTION, "Certificate Description", "Enter a brief description of the certificate")

    with col2:
        put_date_input(CERTIFICATE_ISSUE_DATE, "Issue Date", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        put_date_input(CERTIFICATE_EXPIRY_DATE, "Expiry Date", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        if st.button("Add Certificate"): 
            print("Adding certificate with type:", st.session_state[CERTIFICATION_TYPE])
            if st.session_state[CERTIFICATION_TYPE] == "Select Type":
                st.error("Please select a valid certification type.")
            else:
                certs = st.session_state.get(CERTIFICATIONS, [])
                new_cert = CertificateData(
                    type=st.session_state[CERTIFICATION_TYPE],
                    id=st.session_state[CERTIFICATE_ID],
                    description=st.session_state[CERTIFICATE_DESCRIPTION],
                    issue_date=st.session_state[CERTIFICATE_ISSUE_DATE],
                    expiry_date=st.session_state[CERTIFICATE_EXPIRY_DATE],
                    issued_by=st.session_state.get(CERTIFICATE_ISSUED_BY, ""),
                    image=None
                )
                certs.append(new_cert)
                st.session_state[CERTIFICATIONS] = certs
                st.success("Certificate added successfully!")
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

    uploaded_file = st.file_uploader("Upload a certification image", type=["jpg", "jpeg", "png"], key=st.session_state.cert_file_key)

    if uploaded_file is not None and session_not(CANCEL_NEW_CERTIFICATE):
        print("File loaded")
        print("Uploaded file:", uploaded_file.name)

        cola, colb, colc = st.columns([0.3, 0.4, 0.3])

        with cola:
            st.image(uploaded_file, caption="Uploaded image", use_container_width=True)

        with colb:
            if session_not(PROCESSING_CERTIFICATE):
                with st.spinner("Running OCR..."):
                    ocr_text = extract_text_from_image(uploaded_file)
                    st.subheader("🔍 Extracted OCR Text")
                    st.text_area("Raw OCR Output", ocr_text, height=200)
                    st.session_state.raw_ocr_certificate_text = ocr_text

                with st.spinner("Asking Gemini to extract fields..."):
                    result = extract_fields_with_gemini(ocr_text)
                    st.session_state.certification_extracted_fields = result

                st.subheader("📋 Structured Output")
                st.json(result)

                st.session_state[PROCESSING_CERTIFICATE] = True
            else:
                ocr_text = st.session_state.raw_ocr_certificate_text
                st.subheader("🔍 Extracted OCR Text")
                st.text_area("Raw OCR Output", ocr_text, height=200)
                st.session_state.raw_ocr_certificate_text = ocr_text
                result = st.session_state.certification_extracted_fields
                st.subheader("📋 Structured Output")
                st.json(result)

            colAlpha, colBeta = st.columns(2)

            with colAlpha:

                if st.button("Use Certificate Data"): 
                
                    print("Attempting to use certification data")

                    certName = result.get("certification_name", "")
                    certDescription = result.get("certification_description", "")
                    certType = "Other"
                    
                    if "SAFETY" in certName.upper() or "SAFETY" in certDescription.upper():
                        certType = "Safety Certification"

                    object_name = CertificateData(
                        type=certType,
                        id=result.get("certification_id", ""),
                        description=certName,
                        issue_date=result.get("issue_date", ""),
                        expiry_date=result.get("expiry_date", ""),
                        issued_by=result.get("issued_by", ""),
                        image=uploaded_file
                    )

                    print("Object created:", object_name)

                    # Print the object to debug
                    print("Certificate Object:", object_name.to_dict())

                    certs = st.session_state.get(CERTIFICATIONS, [])
                    certs.append(object_name)
                    st.session_state[CERTIFICATIONS] = certs

                    print("Certificate added to session state:", st.session_state[CERTIFICATIONS])

                    # Pretty print entire class object
                    #st.write("Certificate Object:")
                    #st.json(object_name.to_dict())

                    st.session_state[PROCESSING_CERTIFICATE] = False
                    st.session_state[CANCEL_NEW_CERTIFICATE] = False
                    uploaded_file = None
                    st.session_state.raw_ocr_certificate_text = ""
                    st.session_state.certification_extracted_fields = {}
                    current_key = st.session_state.cert_file_key
                    st.session_state.cert_file_key = current_key + "_new"

                    st.rerun()

            
            with colBeta:
                if st.button("Clear Certificate Data"):
                    
                    print("Clearing certificate data")
                    st.session_state[PROCESSING_CERTIFICATE] = False
                    st.session_state[CANCEL_NEW_CERTIFICATE] = True
                    st.session_state.cert_file = None

                    current_key = st.session_state.cert_file_key
                    st.session_state.cert_file_key = current_key + "_new"
                    uploaded_file = None
                    st.session_state.raw_ocr_certificate_text = ""
                    st.session_state.certification_extracted_fields = {}
                    st.rerun()

                    print("MAGICAL CLEARING OF CERTIFICATE DATA")

                    # st.session_state[PROCESSING_CERTIFICATE] = False
                    # st.session_state.raw_ocr_certificate_text = ""
                    # st.session_state.certification_extracted_fields = {}
                    # st.session_state[CERTIFICATION_TYPE] = "Select Type"
                    # st.session_state[CERTIFICATE_ID] = ""
                    # st.session_state[CERTIFICATE_DESCRIPTION] = ""
                    # st.session_state[CERTIFICATE_ISSUE_DATE] = datetime.date.today()
                    # st.session_state[CERTIFICATE_EXPIRY_DATE] = datetime.date.today()
                    #st.session_state[CERTIFICATE_ISSUED_BY] = ""
                

                # if "confirmed" not in st.session_state or st.session_state["confirmed"]:
                #     st.session_state[FIRST_NAME] = parsed_data.get("First Name", "")
                #     st.session_state[LAST_NAME] = parsed_data.get("Last Name", "")
                #     st.session_state[ADDRESS_LINE_1] = parsed_data.get("Street Address", "")
                #     st.session_state[CITY] = parsed_data.get("City", "")

                #     state_abbr = parsed_data.get("State", "")                    
                #     state_name = get_state_name(state_abbr)
                #     st.session_state[STATE] = state_name

                #     st.session_state[ZIP_CODE] = parsed_data.get("Postal Code", "")
                #     st.session_state[COUNTRY] = parsed_data.get("Country", "")

                #     dob_str = parsed_data.get("Date of Birth", "")
                #     dob = datetime.datetime.strptime(dob_str, "%m%d%Y").date()
                    
                #     st.session_state[DOB] = dob
                #     st.session_state[MOBILE] = parsed_data.get("Mobile", "")
                #     st.session_state[EMAIL] = parsed_data.get("Email", "")
                #     st.write("Form populated with driver license data.")
                #     st.rerun()
                # else:
                #     confirm_action(parsed=parsed_data)                



        # Save the uploaded file to session state


        #st.session_state[CERTIFICATE_IMAGE] = uploaded_file
        #st.image(uploaded_file, caption="Uploaded Certificate Image", use_column_width=True)


    if cancelling_certificate and not processing_certificate:
        print("Resetting certificate processing state")        
        #st.session_state[PROCESSING_CERTIFICATE] = False
        st.session_state[CANCEL_NEW_CERTIFICATE] = False
