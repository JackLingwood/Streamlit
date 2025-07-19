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

def clearConsole():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_aamva_barcode(raw_data):
    """
    Parses AAMVA barcode string from a U.S. driver's license.
    Returns a dictionary of known fields.
    """
    # Convert bytes to string if needed
    if isinstance(raw_data, bytes):
        raw_data = raw_data.decode("utf-8", errors="ignore")
    
    # Define known AAMVA field codes
    field_map = {
        "DAQ": "License Number",
        "DCS": "Last Name",
        "DAC": "First Name",
        "DAD": "Middle Name",
        "DBB": "Date of Birth",
        "DBA": "Expiration Date",
        "DBD": "Issue Date",
        "DBC": "Gender",
        "DAY": "Eye Color",
        "DAU": "Height",
        "DAG": "Street Address",
        "DAI": "City",
        "DAJ": "State",
        "DAK": "Postal Code",
        "DCF": "Document Discriminator",
        "DCG": "Country",
        "DCK": "Inventory Control Number",
        "DDB": "Issue Timestamp",
        "DAW": "Weight",
    }

    parsed = {}

    # Look for each field using regex
    for code, label in field_map.items():
        match = re.search(rf"{code}([^\n\r]*)", raw_data)
        if match:
            parsed[label] = match.group(1).strip()

    return parsed


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

        st.write("Upload Certificate Image")


        
        from PIL import Image

        clearConsole()
        print("Analyzing barcode from uploaded file...")

        #from pdf417decoder import decode
        # from PIL import Image

        uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "pdf"], key="certificate_image_uploader")
        if uploaded_file is not None:
            st.session_state[DRIVER_LICENSE] = uploaded_file
            st.image(uploaded_file, caption="Uploaded Drivers License", use_container_width=True)
            # Load your image
            #image_path = "drivers_license_back.png"
            #image = Image.open(image_path)

            # Decode PDF417 barcodes in the image
            image = Image.open(uploaded_file)

            image.save("temp_image.png")  # Save the image temporarily for debugging

            from pyzxing import BarCodeReader
            reader = BarCodeReader()
            results = reader.decode("temp_image.png")

            print(results)
            if results:
                raw = results[0]['raw']
                parsed_data = parse_aamva_barcode(raw)

                st.write("Results:")
                for key, value in parsed_data.items():
                    st.write(f"{key}: {value}")


                @st.dialog("Use driver license data to populate form?")
                def confirm_action(parsed):
                    st.write("Do you want to proceed with this action?")

                    st.write("Parsed Data:")
                    for key, value in parsed.items():
                        st.write(f"{key}: {value}")


                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Yes"):
                            st.session_state["confirmed"] = True
                            st.rerun()
                    with col2:
                        if st.button("No"):
                            st.session_state["confirmed"] = False
                            st.rerun()


                if st.button("Use Driver License Data"):    
                    if "confirmed" not in st.session_state or st.session_state["confirmed"]:
                        st.session_state[FIRST_NAME] = parsed_data.get("First Name", "")
                        st.session_state[LAST_NAME] = parsed_data.get("Last Name", "")
                        st.session_state[ADDRESS_LINE_1] = parsed_data.get("Street Address", "")
                        st.session_state[CITY] = parsed_data.get("City", "")
                        st.session_state[STATE] = parsed_data.get("State", "")
                        st.session_state[ZIP_CODE] = parsed_data.get("Postal Code", "")
                        st.session_state[COUNTRY] = parsed_data.get("Country", "")

                        dob_str = parsed_data.get("Date of Birth", "")
                        dob = datetime.datetime.strptime(dob_str, "%m%d%Y").date()
                        
                        st.session_state[DOB] = dob
                        st.session_state[MOBILE] = parsed_data.get("Mobile", "")
                        st.session_state[EMAIL] = parsed_data.get("Email", "")
                        st.write("Form populated with driver license data.")
                        st.rerun()
                    else:
                        confirm_action(parsed=parsed_data)                




            





            
              # Print the results for debugging
            #print(results[0].raw)  # Print the raw data of the first result
            #t.write("Raw barcode data:")
            #st.write(results[0].raw)  # Display the raw data in Streamlit
            print("++++++++++++++") 









            #results = decode(image)

            # Display the result
            # for result in results:
            #     st.write("Raw barcode data:")
            #     st.write(result.data.decode('utf-8'))




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

# st.write("### Navigation")  
# st.write("Selected: ", selected)
# st.write("Index: ", st.session_state[SELECTED_INDEX])
# st.write("Max Index: ", len(MENU_OPTIONS) - 1)

col_left, col_right = st.columns([3, 1])
with col_right:
    if st.button("Next"):
        if st.session_state[SELECTED_INDEX] < len(MENU_OPTIONS) - 1:
            st.session_state[SELECTED_INDEX] += 1
            st.rerun()

with col_left:
    if st.button("Previous"):
        if st.session_state[SELECTED_INDEX] > 0:
            st.session_state[SELECTED_INDEX] -= 1
            st.rerun()            

