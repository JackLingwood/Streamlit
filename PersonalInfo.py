import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np
from Common import *

def initialize_session_variables():
    init(FIRST_NAME, "")
    init(LAST_NAME, "")
    init(DOB, datetime.date.today())
    init(MOBILE, "")
    init(MIDDLE_NAME, "")
    
ethnicities = ["Ethnicity", "Hispanic or Latino", "Not Hispanic or Latino"]
languages = ["Primary Language", "English", "Spanish", "Other"]

def get_personal_info():
    initialize_session_variables()

    st.title("Personal Information 🧑‍🏭")
    st.write("Enter your personal details below")

    st.subheader("Personal Information")

    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        put_text_input(FIRST_NAME, "First Name", "Enter your first name")
        put_date_input(DOB, "Date of birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        put_selectbox(IS_VETERAN, "Are you a veteran?", ["Yes", "No"], index=0)


    with col2:
        
        put_text_input(MIDDLE_NAME, "Middle Name", "Enter your middle name")
        put_selectbox(ETHNICITY, "Ethnicity", ethnicities, index=0)
        put_text_input(ALLERGIES, "Allergies", "Enter any allergies", max_chars=100)

    with col3:
        put_text_input(LAST_NAME, "Last Name", "Enter your last name")
        put_selectbox(PRIMARY_LANGUAGE, "Primary Language", languages, index=0)
        put_text_input(LAST_4_SSN, "Last 4 digits of SSN", "Enter the last 4 digits of your SSN", max_chars=4, type="password")        
        
    
    st.write("Gender")

    st.session_state[GENDER] = st.selectbox(
        label="Select your gender",
        options=["Select", "Male", "Female", "Non-binary", "Prefer not to say"],
        index=0
    )   

    st.subheader("Government Issued ID")
    cola, colb, colc = st.columns(3, gap="small")
    with cola:
        put_selectbox(GOVERNMENT_ID_TYPE, "ID Type", ["Driver's License", "Passport", "State ID"], index=0)

        
    with colb:
        put_selectbox(GOVERNMENT_ID_ISSUED_BY, "Issued By", ["State", "Federal", "Other"], index=0)        

    with colc:
        put_text_input(GOVERNMENT_ID_NUMBER, "ID Number", "Enter your government ID number", max_chars=20)
        