from datetime import *
from dateutil.relativedelta import relativedelta
import streamlit as st
from streamlit_option_menu import option_menu
#import pandas as pd
#import plotly.express as px
#import pickle
#import plotly.graph_objects as go
from streamlit_phone_number import st_phone_number
from Photo import take_photo
#from Common import init, MENU_OPTIONS, SELECTED_INDEX
from Common import *

from PersonalInfo import get_personal_info
from ContactInfo import get_contact_info
from Trades import get_trade_info
from Certificates import get_certificate_info
from ConsentForm import get_consent_form
from DriversLicense import get_drivers_license_info


# https://github.com/ikatyang/emoji-cheat-sheet

st.set_page_config(
    page_title="ABC Construction Project",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/jacklingwood/',
        'Report a bug': "https://github.com/JackLingwood",
        'About': "## A 'Construction Worker Jobsite Enrollment Form' by Jack Lingwood"
    },
)

init_session_variables()

# Initialize session state variables
init("setup_complete", False)
init("user_message_count", 0)
init("feedback_shown", False)   
init("chat_complete", False)
init("messages", [])
init(SELECTED_INDEX, 0)

with st.sidebar:
    selected = option_menu(
        menu_title = "Worker Enrollment",
        options = MENU_OPTIONS,
        icons = ["clipboard", "person-video", "card-text", "telephone", "hammer", "award", "pencil-square", "mortarboard"],
        menu_icon= "none",        
        default_index=st.session_state[SELECTED_INDEX]
    )






def next_step():
    # if st.button("Next"):
    # if st.session_state["selected_index"] < len(MENU_OPTIONS) - 1:
    #     st.session_state["selected_index"] += 1
    #     st.experimental_rerun()
    
    st.session_state.setup_complete = True
    st.write("Setup complete. Starting interview...")

if selected == "Worker Registration":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title('Worker Registration 👷')
        st.header("Enter your basic information")
        st.divider()
        col1, col2 = st.columns([2, 2])

        with col1:
            put_text_input(FIRST_NAME, "First Name", "Enter your first name")
            put_text_input(EMAIL, "Email", "Enter your email")

            min_value = datetime.date(1900, 1, 1)
            today = date.today()
            sixteen_years_ago = today - relativedelta(years=16)
            put_date_input(DOB, "Date of birth", min_value=min_value, max_value=sixteen_years_ago)

        with col2:
            put_text_input(LAST_NAME, "Last Name", "Enter your last name")
            put_text_input(MOBILE, "Mobile", "Enter your mobile number")
    get_drivers_license_info()        


if selected == "Take a Photo":
    take_photo()    
        
if selected == "Personal Information":
    get_personal_info()

if selected == "Contact Information":
    get_contact_info()

if selected == "Trades":
    get_trade_info()    

if selected == "Certifications":    
    get_certificate_info()

if selected == "Consent Form":
    get_consent_form()  

if selected == "Project Courses":
    st.write("Project Courses will be implemented in the future.")
    

if selected == "Facial Recognition Lab":    
    import SiteSafetyCardToText

    #SiteSafetyCardToText.py

# st.write("### Navigation")  
# st.write("Selected: ", selected)
# st.write("Index: ", st.session_state[SELECTED_INDEX])
# st.write("Max Index: ", len(MENU_OPTIONS) - 1)

col_left, col_right = st.columns([3, 1])
with col_right:
    if st.button("Next", key="next_button"):
        if st.session_state[SELECTED_INDEX] < len(MENU_OPTIONS) - 1:
            st.session_state[SELECTED_INDEX] += 1
            st.rerun()

with col_left:
    if st.button("Previous", key="prev_button"):
        if st.session_state[SELECTED_INDEX] > 0:
            st.session_state[SELECTED_INDEX] -= 1
            st.rerun()            

