from httpx import options
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np
from Common import *

    

def get_trade_info():    

    st.title("Trade Information 🛠️")
    st.write("Enter your trade information")

    roles = ["Role", "Supervisor", "Journeyman", "Apprentice", "Laborer"]


    col1, col2 = st.columns(2)
    with col1:
        put_selectbox(ROLE, "Role", roles, index=0)
        put_text_input(WORK_EXPERIENCE, "Work Experience", "Enter your work experience in years")

    with col2:
        put_selectbox(LABOR_UNION, "Are you a member of a labor union?", ["Labor Union","Yes", "No"], index=0)
        put_text_input(LABOR_UNION_NUMBER, "Labor Union Number", "Enter your labor union number (if applicable)")

    st.markdown("---")

    st.subheader("Select Trades")

    trades = [
    "Acoustical Treatment", "Audio Visual", "Carpenter", "Concrete", "Craftworker",
    "Demolition", "Doors & Frames", "Earthwork", "Electrical", "Elevators", "Fire & Smoke",
    "Flooring", "Furnishings", "Glazing", "HVAC", "Laborer", "Landscaping/Irrigation",
    "Masonry", "Mechanical", "Paints & Coatings", "Plumbing", "Roofing", "Solar & Wind",
    "Structural metal Framing", "Utility Services", "Waterproofing", "Water Supply & Treatment",
    "Welding", "Windows", "Test"
    ]

    st.pills(
        label="Select your trades",
        options=trades, selection_mode="multi",
        key="selected_trades",
        default=[]
    )

    st.write("Add other trades")
    st.text_input("Other Trades", key="other_trades", placeholder="Enter other trades you are skilled in")




        


