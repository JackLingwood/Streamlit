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
        st.session_state[FIRST_NAME] = st.text_input(label="a",value=st.session_state[FIRST_NAME], placeholder="First Name", max_chars=20, label_visibility="collapsed")
        st.session_state[DOB] = st.date_input(label="b",value=st.session_state[DOB], min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today(), label_visibility="collapsed")
        st.session_state[IS_VETERAN] = st.selectbox(label="c",options=["Are you a veteran?", "Yes", "No"], index=0, label_visibility="collapsed")

    with col2:
        st.session_state[MIDDLE_NAME] = st.text_input(label="d",value=st.session_state[MIDDLE_NAME], placeholder="Middle Name", max_chars=20, label_visibility="collapsed")
        st.session_state[ETHNICITY] = st.selectbox(label="e",options=ethnicities, index=0,label_visibility="collapsed")
        st.session_state[ALLERGIES] = st.text_input(label="f",value=st.session_state[ALLERGIES], placeholder="Allergies", max_chars=100, label_visibility="collapsed")        

        
    with col3:
        st.session_state[LAST_NAME] = st.text_input(label="g",value=st.session_state[LAST_NAME], placeholder="Last Name", max_chars=20, label_visibility="collapsed")
        st.session_state[PRIMARY_LANGUAGE] = st.selectbox(label="h",options=languages, index=0, label_visibility="collapsed")
        st.session_state[LAST_4_SSN] = st.text_input(label="i",value=st.session_state[LAST_4_SSN], placeholder="Last 4 digits of SSN", max_chars=4, type="password", label_visibility="collapsed")
    
    st.write("Gender")
    st.session_state[GENDER] = st.selectbox(
        label="Select your gender",
        options=["Select", "Male", "    Female", "Non-binary", "Prefer not to say"],
        index=0
    )   

    st.subheader("Government Issued ID")
    cola, colb, colc = st.columns(3, gap="small")
    with cola:
        st.session_state[GOVERNMENT_ID_TYPE] = st.selectbox(label="j",options=["ID Type", "Driver's License", "Passport", "State ID"], index=0, label_visibility="collapsed")
    with colb:
        st.session_state[GOVERNMENT_ID_ISSUED_BY] = st.selectbox(label="k",options=["Issued By", "State", "Federal", "Other"], index=0, label_visibility="collapsed")

    with colc:
        st.session_state[GOVERNMENT_ID_NUMBER] = st.text_input(label="l",value=st.session_state[GOVERNMENT_ID_NUMBER], placeholder="ID Number", max_chars=20, label_visibility="collapsed")




        


