import datetime
import streamlit as st
from streamlit_option_menu import option_menu
#import pandas as pd
#import plotly.express as px
#import pickle
#import plotly.graph_objects as go
from streamlit_phone_number import st_phone_number
from Photo import take_photo


# https://github.com/ikatyang/emoji-cheat-sheet

st.set_page_config(
    page_title="Buffalo Bills Stadium",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/jacklingwood/',
        'Report a bug': "https://github.com/JackLingwood",
        'About': "## A 'Construction Worker Jobsite Enrollment Form' by Jack Lingwood"
    },
)

def init(key, default_value):
    if key not in st.session_state:
        st.session_state[key] = default_value   

LAST_NAME = "last_name"
FIRST_NAME = "first_name"
EMAIL = "email"
DOB = "dob"
MOBILE = "mobile"
SELECTED_INDEX = "selected_index"

# Initialize session state variables
init("setup_complete", False)
init("user_message_count", 0)
init("feedback_shown", False)   
init("chat_complete", False)
init("messages", [])

init(SELECTED_INDEX, 0)
init(FIRST_NAME, "")
init(LAST_NAME, "")
init(EMAIL, "")
init(DOB, datetime.date.today())
init(MOBILE, "")

MENU_OPTIONS = [
    "Worker Registration", "Take a Photo", "Personal Information", "Contact Information",
    "Trades", "Certifications", "Consent Form", "Project Courses", "Chat"
]

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
        st.title('Worker Registration :construction_worker:')
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
    col1a, col2a = st.columns([2, 1])
    with col1a:
        take_photo()  # Call the function to take a photo


        # xxx



        # st.title('Take a photo 📸')
        # if "captured_photo" not in st.session_state:
        #     st.session_state["captured_photo"] = None
        # if "latest_frame" not in st.session_state:
        #     st.session_state["latest_frame"] = None

        # class VideoProcessor(VideoTransformerBase):
        #     def transform(self, frame):
        #         img = frame.to_ndarray(format="bgr24")
        #         st.session_state["latest_frame"] = img.copy()
        #         return img

        # webrtc_streamer(key="example", video_processor_factory=VideoProcessor)

        # if st.button("📷 Capture Photo"):
        #     if st.session_state["latest_frame"] is not None:
        #         st.session_state["captured_photo"] = st.session_state["latest_frame"]
        #         st.image(st.session_state["captured_photo"], channels="BGR", caption="Captured Photo")
        #     else:
        #         st.warning("No frame captured yet.")

        # # Always show the last captured photo if it exists
        # if st.session_state["captured_photo"] is not None:
        #     st.image(st.session_state["captured_photo"], channels="BGR", caption="Last Captured Photo")
        # else:
        #     st.warning("No photo captured yet. Please capture a photo first.")
