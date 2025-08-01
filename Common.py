from streamlit_phone_number import st_phone_number
import datetime
import streamlit as st
import re

MENU_OPTIONS = [
    "Worker Registration", "Take a Photo", "Personal Information", "Contact Information",
    "Trades", "Certifications", "Consent Form", "Project Courses", "Chat", "Facial Recognition Lab"
]

DRIVER_LICENSE = "driver_license"

CERTIFICATION_TYPES = [
    "Select Type", "Trade Certification", "Safety Certification", "Other"
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

CONTACT_EMAIL = "contact_email"
CONTACT_PHONE = "contact_phone"
ADDRESS_LINE_1 = "address_line_1"
ADDRESS_LINE_2 = "address_line_2"
CITY = "city"
STATE = "state"
ZIP_CODE = "zip_code"
COUNTRY = "country"
EMERGENCY_CONTACT_NAME = "emergency_contact_name"
EMERGENCY_CONTACT_RELATIONSHIP = "emergency_contact_relationship"
EMERGENCY_CONTACT_PHONE = "emergency_contact_phone"

ROLE = "role"
WORK_EXPERIENCE = "work_experience"
LABOR_UNION = "labor_union"
LABOR_UNION_NUMBER = "labor_union_number"
SELECTED_TRADES = "selected_trades"

CERTIFICATIONS = "certifications"
PROCESSING_CERTIFICATE = "processing_certificate"
CANCEL_NEW_CERTIFICATE = "cancel_new_certificate"

CERTIFICATION_TYPE = "certification_type"
CERTIFICATE_ID = "certificate_id"
CERTIFICATE_DESCRIPTION= "certificate_description"
CERTIFICATE_ISSUE_DATE = "certificate_issue_date"
CERTIFICATE_EXPIRY_DATE = "certificate_expiry_date"
CERTIFICATE_ISSUED_BY = "certificate_issued_by"
CERTIFICATE_IMAGE = "certificate_image"

CONSENT_FORM_JOB_TITLE = "consent_form_job_title"
CONSENT_FORM_TRADE_STATUS = "consent_form_trade_status"
CONSENT_FORM_SUPERVISOR_NAME = "consent_form_supervisor_name"
CONSENT_FORM_SUPERVISOR_PHONE = "consent_form_supervisor_phone"
CONSENT_FORM_PROJECT_TRADE = "consent_form_project_trade"
CONSENT_FORM_SUPERVISOR_NAME = "consent_form_supervisor_name"

CONSENT_FORM_SIGNATURE_DATE = "consent_form_signature_date"
CONSENT_FORM_SIGNATURE = "consent_form_signature"

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

    init(CONTACT_EMAIL, "")
    init(CONTACT_PHONE, "")
    init(ADDRESS_LINE_1, "")
    init(ADDRESS_LINE_2, "")
    init(CITY, "")
    init(STATE, "")
    init(ZIP_CODE, "")
    init(COUNTRY, "")
    init(EMERGENCY_CONTACT_NAME, "")
    init(EMERGENCY_CONTACT_RELATIONSHIP, "")
    init(EMERGENCY_CONTACT_PHONE, "")

    init(ROLE, "")
    init(WORK_EXPERIENCE, "")
    init(LABOR_UNION, "")
    init(LABOR_UNION_NUMBER, "")
    init(SELECTED_TRADES, [])

    init(CERTIFICATION_TYPE, "")
    init(CERTIFICATE_ID, "")
    init(CERTIFICATE_DESCRIPTION, "")
    init(CERTIFICATE_ISSUE_DATE, datetime.date.today())
    init(CERTIFICATE_EXPIRY_DATE, datetime.date.today())
    init(CERTIFICATE_ISSUED_BY, "")
    init(CERTIFICATE_IMAGE, None)
    init(CONSENT_FORM_SUPERVISOR_PHONE, "")
    init(CERTIFICATIONS, [])
    init(PROCESSING_CERTIFICATE, False)
    init(CANCEL_NEW_CERTIFICATE, False)



    init(CONSENT_FORM_JOB_TITLE, "")
    init(CONSENT_FORM_TRADE_STATUS, "")
    init(CONSENT_FORM_SUPERVISOR_NAME, "")
    init(CONSENT_FORM_PROJECT_TRADE, "")
    init(CONSENT_FORM_SIGNATURE_DATE, datetime.date.today())
    init(CONSENT_FORM_SIGNATURE, None)


def init(key, default_value):
    if key not in st.session_state:
        st.session_state[key] = default_value

def get_session(key):
    return st.session_state.get(key, None)

def session_not(key):
    value = get_session(key)
    if value is None:
        return True
    if isinstance(value, bool):
        return not value
    
def session_is(key):
    value = get_session(key)
    if value is None:
        return False

    if isinstance(value, bool):
        return value
    

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(pattern, email) is not None

def put_phone(session_key, label="", placeholder="", default_country="US"):
    st_phone_number(label=label, placeholder=placeholder,  default_country=default_country, key=session_key)

def put_text_input(session_key, label, placeholder="", type="default", max_chars=20, label_visibility="collapsed"):
    st.session_state[session_key] = st.text_input(label=label, value=st.session_state[session_key], placeholder=placeholder, type=type, max_chars=max_chars, label_visibility=label_visibility)



def put_selectbox(session_key, label, options, index=0):
    st.selectbox(label=label, options=options, index=index, key=session_key, label_visibility="collapsed")

#def place_date_input(session_key, label, min_value=None, max_value=None):
 #   st.session_state[session_key] = st.date_input(label=label,value=st.session_state[session_key], min_value=min_value if min_value else datetime.date(1900, 1, 1), max_value=max_value if max_value else datetime.date.today())


def put_date_input(session_key, label, min_value=None, max_value=None, label_visibility="collapsed"):
    min_value = min_value or datetime.date(1900, 1, 1)
    max_value = max_value or datetime.date.today()

    # Get existing value or set to max_value by default
    existing_value = st.session_state.get(session_key, max_value)

    # Clamp the existing value to be within range
    if existing_value < min_value:
        existing_value = min_value
    elif existing_value > max_value:
        existing_value = max_value

    st.session_state[session_key] = st.date_input(
        label=label,
        value=existing_value,
        min_value=min_value,
        max_value=max_value,
        label_visibility=label_visibility
    )

def clearConsole():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')    


# Create a class for storing certificate data
class CertificateData:
    def __init__(self):
        self.type = ""
        self.id = ""
        self.description = ""
        self.issue_date = datetime.date.today()
        self.expiry_date = datetime.date.today()
        self.issued_by = ""
        self.image = None

    def __init__(self, type="", id="", description="", issue_date=None, expiry_date=None, issued_by="", image=None):
        self.type = type
        self.id = id
        self.description = description
        self.issue_date = issue_date or datetime.date.today()
        self.expiry_date = expiry_date or datetime.date.today()
        self.issued_by = issued_by
        self.image = image

    def to_dict(self):
        def safe_isoformat(date_value):
            if hasattr(date_value, "isoformat"):
                return date_value.isoformat()
            try:
                # Try to parse string to date
                return datetime.strptime(date_value, "%m/%d/%Y").date().isoformat()
            except Exception:
                return str(date_value)
        return {
            "type": self.type,
            "id": self.id,
            "description": self.description,
            "issue_date": safe_isoformat(self.issue_date),
            "expiry_date": safe_isoformat(self.expiry_date),
            "issued_by": self.issued_by,
            "image": self.image
        }
    
# Create a class for storing multiple certificates
class CertificateCollection:
    def __init__(self):
        self.certificates = []

    def add_certificate(self, certificate: CertificateData):
        self.certificates.append(certificate)

    def to_dict(self):
        return [cert.to_dict() for cert in self.certificates]
    