from httpx import options
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np
from Common import *


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
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "pdf"], key="certificate_image_uploader")
    if uploaded_file is not None:
        st.session_state[CERTIFICATE_IMAGE] = uploaded_file
        st.image(uploaded_file, caption="Uploaded Certificate Image", use_column_width=True)    