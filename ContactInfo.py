import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np
from Common import *


    
ethnicities = ["Ethnicity", "Hispanic or Latino", "Not Hispanic or Latino"]
languages = ["Primary Language", "English", "Spanish", "Other"]
us_states_and_territories = [
    # 50 States
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
    "Wisconsin", "Wyoming",

    # 5 Major Territories
    "American Samoa", "Guam", "Northern Mariana Islands", "Puerto Rico", "U.S. Virgin Islands",

    # Minor Outlying Islands (optional, often omitted)
    "Baker Island", "Howland Island", "Jarvis Island", "Johnston Atoll", "Kingman Reef",
    "Midway Islands", "Navassa Island", "Palmyra Atoll", "Wake Island"
]

def get_index_of_state(): 
    state_name =  st.session_state[STATE]
    print(f"State name: {state_name}")

    try:
        return us_states_and_territories.index(state_name)+1
    except ValueError:
        return 0


us_states_and_territories_with_abbreviation = [
    # 50 States
    { "abbreviation": "AL", "name": "Alabama" },
    { "abbreviation": "AK", "name": "Alaska" },
    { "abbreviation": "AZ", "name": "Arizona" },
    { "abbreviation": "AR", "name": "Arkansas" },
    { "abbreviation": "CA", "name": "California" },
    { "abbreviation": "CO", "name": "Colorado" },
    { "abbreviation": "CT", "name": "Connecticut" },
    { "abbreviation": "DE", "name": "Delaware" },
    { "abbreviation": "FL", "name": "Florida" },
    { "abbreviation": "GA", "name": "Georgia" },
    { "abbreviation": "HI", "name": "Hawaii" },
    { "abbreviation": "ID", "name": "Idaho" },
    { "abbreviation": "IL", "name": "Illinois" },
    { "abbreviation": "IN", "name": "Indiana" },
    { "abbreviation": "IA", "name": "Iowa" },
    { "abbreviation": "KS", "name": "Kansas" },
    { "abbreviation": "KY", "name": "Kentucky" },
    { "abbreviation": "LA", "name": "Louisiana" },
    { "abbreviation": "ME", "name": "Maine" },
    { "abbreviation": "MD", "name": "Maryland" },
    { "abbreviation": "MA", "name": "Massachusetts" },
    { "abbreviation": "MI", "name": "Michigan" },
    { "abbreviation": "MN", "name": "Minnesota" },
    { "abbreviation": "MS", "name": "Mississippi" },
    { "abbreviation": "MO", "name": "Missouri" },
    { "abbreviation": "MT", "name": "Montana" },
    { "abbreviation": "NE", "name": "Nebraska" },
    { "abbreviation": "NV", "name": "Nevada" },
    { "abbreviation": "NH", "name": "New Hampshire" },
    { "abbreviation": "NJ", "name": "New Jersey" },
    { "abbreviation": "NM", "name": "New Mexico" },
    { "abbreviation": "NY", "name": "New York" },
    { "abbreviation": "NC", "name": "North Carolina" },
    { "abbreviation": "ND", "name": "North Dakota" },
    { "abbreviation": "OH", "name": "Ohio" },
    { "abbreviation": "OK", "name": "Oklahoma" },
    { "abbreviation": "OR", "name": "Oregon" },
    { "abbreviation": "PA", "name": "Pennsylvania" },
    { "abbreviation": "RI", "name": "Rhode Island" },
    { "abbreviation": "SC", "name": "South Carolina" },
    { "abbreviation": "SD", "name": "South Dakota" },
    { "abbreviation": "TN", "name": "Tennessee" },
    { "abbreviation": "TX", "name": "Texas" },
    { "abbreviation": "UT", "name": "Utah" },
    { "abbreviation": "VT", "name": "Vermont" },
    { "abbreviation": "VA", "name": "Virginia" },
    { "abbreviation": "WA", "name": "Washington" },
    { "abbreviation": "WV", "name": "West Virginia" },
    { "abbreviation": "WI", "name": "Wisconsin" },
    { "abbreviation": "WY", "name": "Wyoming" },

    # 5 Major Territories
    { "abbreviation": "AS", "name": "American Samoa" },
    { "abbreviation": "GU", "name": "Guam" },
    { "abbreviation": "MP", "name": "Northern Mariana Islands" },
    { "abbreviation": "PR", "name": "Puerto Rico" },
    { "abbreviation": "VI", "name": "U.S. Virgin Islands" },

    # Minor Outlying Islands (ISO alpha-2 codes used where available)
    { "abbreviation": "UM-81", "name": "Baker Island" },
    { "abbreviation": "UM-84", "name": "Howland Island" },
    { "abbreviation": "UM-86", "name": "Jarvis Island" },
    { "abbreviation": "UM-67", "name": "Johnston Atoll" },
    { "abbreviation": "UM-89", "name": "Kingman Reef" },
    { "abbreviation": "UM-71", "name": "Midway Islands" },
    { "abbreviation": "UM-76", "name": "Navassa Island" },
    { "abbreviation": "UM-95", "name": "Palmyra Atoll" },
    { "abbreviation": "UM-79", "name": "Wake Island" }
]

def get_state_name(state_abbr):
    for state in us_states_and_territories_with_abbreviation:
        if state["abbreviation"] == state_abbr:
            return state["name"]
    return "Unknown State"



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


   # Give me array with all US states and territories
   
    

    # how do I append one array to another in python


    with cold:
        put_selectbox(STATE, "State", ["Select State"] + us_states_and_territories, index=get_index_of_state()) 
        put_text_input(ZIP_CODE, "Zip Code", "Enter your zip code")
        put_text_input(COUNTRY, "Country", "Enter your country")
        

    st.subheader("Emergency Contact")
    cole, colf = st.columns(2)

    with cole:
        put_text_input(EMERGENCY_CONTACT_NAME, "Emergency Contact Name", "Enter the name of your emergency contact")
        put_selectbox(EMERGENCY_CONTACT_RELATIONSHIP, "Relationship", ["Select Relationship", "Parent", "Sibling", "Friend", "Other"], index=0)

    with colf:
        put_text_input(EMERGENCY_CONTACT_PHONE, "Emergency Contact Phone", "Enter the phone number of your emergency contact")






        


