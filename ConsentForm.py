from httpx import options
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np
from Common import *

def get_consent_form():    

    st.title("Consent Form 🖋️")
    st.write("Enter your consent information")

    job_titles = ["Supervisor", "Project Manager", "Site Manager", "Foreman", "Other"]
    project_trade = ["Trade", "Electrical", "Plumbing", "Carpentry", "Masonry", "Other"]
    trade_status = ["Trade Status", "Active", "Inactive", "Pending"]

    col1, col2 = st.columns(2)
    with col1:
        put_selectbox(CONSENT_FORM_JOB_TITLE, "Job Title", job_titles, index=0)
        put_selectbox(CONSENT_FORM_PROJECT_TRADE, "Project Trade", project_trade, index=0)
        put_selectbox(CONSENT_FORM_TRADE_STATUS, "Trade Status", trade_status, index=0)

    with col2:
        put_text_input(CONSENT_FORM_SUPERVISOR_NAME, "Supervisor Name", "Enter the name of your supervisor")
        put_text_input(CONSENT_FORM_SUPERVISOR_PHONE, "Supervisor Phone", "Enter the phone number of your supervisor")
        put_text_input(LAST_4_SSN, "Last 4 SSN", "Enter the last 4 digits of your Social Security Number")