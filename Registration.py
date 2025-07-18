import datetime
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


# https://github.com/ikatyang/emoji-cheat-sheet

st.set_page_config(
    page_title="ABC Construction Project",
    page_icon="🧊",
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
            st.session_state[FIRST_NAME] = st.text_input(label="First Name", value=st.session_state[FIRST_NAME], placeholder="Enter your first name", max_chars=20)
            st.session_state[EMAIL] = st.text_input(label="Email", value=st.session_state[EMAIL], placeholder="Enter your email", max_chars=20)            
            st.session_state[DOB] = st.date_input(label="Date of birth",    value=st.session_state[DOB], min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today()) 
        
        with col2:
            st.session_state[LAST_NAME] = st.text_input(label="Last Name", value=st.session_state[LAST_NAME], placeholder="Enter your last name", max_chars=20)
            #st.session_state[MOBILE] = st.text_input(label="Mobile", value=st.session_state[MOBILE], placeholder="Enter your mobile number", max_chars=20)
            st.session_state[MOBILE] = st_phone_number(label="Mobile", placeholder="Enter your mobile number",  default_country="US")


    # if st.button("Next", on_click=complete_setup):
    #     st.write("Setup complete. Starting interview...")        

    col_left, col_right = st.columns([3, 1])
    with col_right:
        if st.button("Next"):
            if st.session_state[SELECTED_INDEX] < len(MENU_OPTIONS) - 1:
                st.session_state[SELECTED_INDEX] += 1
                st.rerun()

    

if selected == "Take a Photo":
    take_photo()    
        
if selected == "Personal Information":
    get_personal_info()


  