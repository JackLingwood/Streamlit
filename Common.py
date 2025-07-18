import datetime
import streamlit as st

MENU_OPTIONS = [
    "Worker Registration", "Take a Photo", "Personal Information", "Contact Information",
    "Trades", "Certifications", "Consent Form", "Project Courses", "Chat"
]

SELECTED_INDEX = "selected_index"
LAST_NAME = "last_name"
FIRST_NAME = "first_name"
MIDDLE_NAME = "middle_name"
EMAIL = "email"
DOB = "dob"
MOBILE = "mobile"
ETHNICITY = "ethnicity"
PRIMARY_LANGUAGE = "primary_language"
IS_VETERAN = "is_veteran"
ALLERGIES = "allergies"
LAST_4_SSN = "last_4_ssn"
GENDER = "gender"
GOVERNMENT_ID_TYPE = "government_id_type"
GOVERNMENT_ID_ISSUED_BY = "government_id_issued_by"
GOVERNMENT_ID_NUMBER = "government_id_number"
GOVERNMENT_ID_IMAGE = "government_id_image"

def init_session_variables():
    init(SELECTED_INDEX, 0)
    init(FIRST_NAME, "")
    init(MIDDLE_NAME, "")
    init(LAST_NAME, "")
    init(EMAIL, "")
    init(DOB, datetime.date.today())
    init(MOBILE, "")
    
    init(ETHNICITY, "")
    init(PRIMARY_LANGUAGE, "")
    init(IS_VETERAN, "")
    init(ALLERGIES, "")
    init(LAST_4_SSN, "")
    init(GENDER, "")
    init(GOVERNMENT_ID_TYPE, "")
    init(GOVERNMENT_ID_ISSUED_BY, "")
    init(GOVERNMENT_ID_NUMBER, "")
    init(GOVERNMENT_ID_IMAGE, None)







def init(key, default_value):
    if key not in st.session_state:
        st.session_state[key] = default_value


def get_session(key):
    return st.session_state.get(key, None)  
