
def do_cert_demo():
    import streamlit as st
    from google.cloud import vision
    from google.oauth2 import service_account
    import google.generativeai as genai
    from dotenv import load_dotenv
    import os
    import io
    import json

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
    print("A")
    st.set_page_config(page_title="Certification Card Reader", layout="centered")
    print("B")
    st.title("📇 Certification Card Text Extractor")
    print("C")

    uploaded_file = st.file_uploader("Upload a certification image", type=["jpg", "jpeg", "png"])

    print("D")

    if uploaded_file is not None:
        print("File loaded")
        print("Uploaded file:", uploaded_file.name)
        st.image(uploaded_file, caption="Uploaded image", use_container_width=True)

        with st.spinner("Running OCR..."):
            ocr_text = extract_text_from_image(uploaded_file)
            st.subheader("🔍 Extracted OCR Text")
            st.text_area("Raw OCR Output", ocr_text, height=200)

        with st.spinner("Asking Gemini to extract fields..."):
            result = extract_fields_with_gemini(ocr_text)

        st.subheader("📋 Structured Output")
        st.json(result)
