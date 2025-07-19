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
        put_text_input(CERTIFICATE_NAME, "Certificate Name", "Enter the name of the certificate")
        put_date_input(CERTIFICATE_ISSUE_DATE, "Issue Date", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())

    with col2:
        put_text_input(CERTIFICATE_ISSUED_BY, "Issued By", "Enter the organization that issued the certificate")
        put_text_input(CERTIFICATE_NUMBER, "Certificate Number", "Enter the certificate number (if applicable)")

    st.subheader("Certificate Validity")
    put_date_input(CERTIFICATE_EXPIRY_DATE, "Expiry Date", min_value=datetime.date.today(), label_visibility="collapsed")

    st.markdown("---")  # Separator line