import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np
from Common import *


    
ethnicities = ["Ethnicity", "Hispanic or Latino", "Not Hispanic or Latino"]
languages = ["Primary Language", "English", "Spanish", "Other"]

def get_contact_info():    

    st.title("Contact Information 📞")
    st.write("Enter your contact information")

    st.subheader("Contact Information")

    cola, colb = st.columns(2)
    with cola:
        put_text_input(CONTACT_EMAIL, "Email address", "Enter your contact email")

    with colb:
        put_text_input(CONTACT_PHONE, "Mobile number", "Enter your contact mobile number")


    st.subheader("Home Address")
    colc, cold = st.columns(2)
    
    with colc:
        put_text_input(ADDRESS_LINE_1, "Address Line 1", "Enter your address line 1")
        put_text_input(ADDRESS_LINE_2, "Address Line 2", "Enter your address line 2 (optional)")
        put_text_input(CITY, "City", "Enter your city")
        

    with cold:
        put_selectbox(STATE, "State", ["Select State", "California", "Texas", "New York"], index=0) 
        put_text_input(ZIP_CODE, "Zip Code", "Enter your zip code")
        put_text_input(COUNTRY, "Country", "Enter your country")
        

    st.subheader("Emergency Contact")
    cole, colf = st.columns(2)

    with cole:
        put_text_input(EMERGENCY_CONTACT_NAME, "Emergency Contact Name", "Enter the name of your emergency contact")
        put_selectbox(EMERGENCY_CONTACT_RELATIONSHIP, "Relationship", ["Select Relationship", "Parent", "Sibling", "Friend", "Other"], index=0)

    with colf:
        put_text_input(EMERGENCY_CONTACT_PHONE, "Emergency Contact Phone", "Enter the phone number of your emergency contact")






        


