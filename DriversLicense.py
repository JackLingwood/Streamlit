import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np
from Common import *
from ContactInfo import get_state_name

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
            stripped = match.group(1).strip()
            if stripped =="09021975":
                stripped = "09021904"

            parsed[label] = stripped

    return parsed

def get_drivers_license_info():
    st.write("Upload Rear of Driver's License Image")
    from PIL import Image

    
    

    #from pdf417decoder import decode
    # from PIL import Image

    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "pdf"], key="certificate_image_uploader")
    if uploaded_file is not None:        
        print("Analyzing barcode from uploaded file...")
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
                print("ATTEMPTING TO USE DRIVER LICENSE DATA")   
                if "confirmed" not in st.session_state or st.session_state["confirmed"]:
                    st.session_state[FIRST_NAME] = parsed_data.get("First Name", "")
                    st.session_state[LAST_NAME] = parsed_data.get("Last Name", "")
                    st.session_state[ADDRESS_LINE_1] = parsed_data.get("Street Address", "")
                    st.session_state[CITY] = parsed_data.get("City", "")

                    state_abbr = parsed_data.get("State", "")                    
                    state_name = get_state_name(state_abbr)
                    st.session_state[STATE] = state_name

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



