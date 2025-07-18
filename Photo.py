import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np

def init(key, default_value):
    if key not in st.session_state:
        st.session_state[key] = default_value

def get_session(key):
    return st.session_state.get(key, None)  

def in_session(key):
    return st.session_state[key]

def set_session(key, value=True):
    st.session_state[key] = value

def deactivate_session(key, value=False):
    st.session_state[key] = value

CAPTURED_IMAGE_KEY = 'captured_image'
PHOTO_SESSION = 'photo_session'
PHOTO_SESSION_1_SHOW_INSTRUCTIONS = 1
PHOTO_SESSION_2_CAMERA_ACTIVATING = 2
PHOTO_SESSION_3_CAMERA_ACTIVE = 3
PHOTO_SESSION_4_PHOTO_TAKEN = 4
PHOTO_SESSION_5_PHOTO_ACCEPTED = 5
PHOTO_SESSION_6_PHOTO_DONE = 6


def init_photo_sessions():
    init(CAPTURED_IMAGE_KEY, None)
    init(PHOTO_SESSION,PHOTO_SESSION_1_SHOW_INSTRUCTIONS)
    init(CAPTURED_IMAGE_KEY, None)


def show_photo_instructions():
    col1, col2 = st.columns([0.2, 0.8],gap="large")
    with col1:
        st.image("No Hardhat Allowed.png", width=100)

    with col2:
        st.subheader("Setup your space and remove any face coverings")
        st.write("Make sure you are in a well-lit area and your face is clearly visible.")
        st.write("Use grey or neutral background. Remove any hats, hard hats or other PPE.")


    col1a, col2a = st.columns([0.2, 0.8],gap="large")
    with col1a:
        st.image("No Face Coverings.png", width=100)

    with col2a:
        st.subheader("Remove face coverings")
        st.write("Please remove any face coverings such as masks, sunglasses, or hats to ensure a clear photo.")
        st.write("This helps us to accurately identify you in the photo.")
        st.write("Click the button below to start capturing your photo.")

def show_photo():
    if st.session_state[CAPTURED_IMAGE_KEY] is not None:
        st.image(st.session_state[CAPTURED_IMAGE_KEY], channels="BGR")


def take_photo():

    init_photo_sessions()


    st.title("Take a Photo 📸")

    if get_session(PHOTO_SESSION) == PHOTO_SESSION_6_PHOTO_DONE:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Over"):
                set_session(PHOTO_SESSION, PHOTO_SESSION_1_SHOW_INSTRUCTIONS)
                st.rerun()
        with col2:
            if st.button("Next"):
                st.write("Moving on to the next step...")
        
        show_photo()
        return

    if get_session(PHOTO_SESSION) == PHOTO_SESSION_5_PHOTO_ACCEPTED:
        st.success("Photo accepted!")
        st.balloons()
        show_photo()
        set_session(PHOTO_SESSION, PHOTO_SESSION_6_PHOTO_DONE)        
        return

    if get_session(PHOTO_SESSION) == PHOTO_SESSION_4_PHOTO_TAKEN:
        #if st.session_state[CAPTURED_IMAGE_KEY] is not None:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Accept Photo"):
                set_session(PHOTO_SESSION, PHOTO_SESSION_5_PHOTO_ACCEPTED)
                st.rerun()
                return
        with col2:
            if st.button("Reject Photo"):
                set_session(PHOTO_SESSION, PHOTO_SESSION_1_SHOW_INSTRUCTIONS)
                st.rerun()
                return

        show_photo()
        return
        # st.image(st.session_state[CAPTURED_IMAGE_KEY], channels="BGR")




    # Transformer class to show webcam feed and optionally capture frame
    class VideoTransformer(VideoTransformerBase):
        def __init__(self):
            self.frame = None
            self.capture = False
        
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            self.frame = img
            return frame  # Return the original or modified frame

    #ctx = None
    if get_session(PHOTO_SESSION) == PHOTO_SESSION_1_SHOW_INSTRUCTIONS:
        st.subheader("Capture your image")
        if st.button("Take Photo"):
            set_session(PHOTO_SESSION, PHOTO_SESSION_2_CAMERA_ACTIVATING)
        show_photo_instructions()

        
    if get_session(PHOTO_SESSION) == PHOTO_SESSION_2_CAMERA_ACTIVATING or get_session(PHOTO_SESSION) == PHOTO_SESSION_3_CAMERA_ACTIVE:
        
        if get_session(PHOTO_SESSION) == PHOTO_SESSION_3_CAMERA_ACTIVE:
            if st.button("Capture Photo"):
                ctx = get_session("CTX")
                if ctx is None:
                    st.write("Camera is active. Click 'Capture Photo' to take a photo.")
                if not ctx:
                   st.write("Camera is active. Click 'Capture Photo' to take a photo.")
                else:
                    st.write("Activating camera... Please wait.")
                    ctx = webrtc_streamer(
                        key="example",
                        video_processor_factory=VideoTransformer,
                        media_stream_constraints={"video": True, "audio": False},
                        async_processing=True,
                    )
                img = ctx.video_processor.frame
                if img is not None:
                    st.session_state[CAPTURED_IMAGE_KEY] = img
                    show_photo()
                    set_session(PHOTO_SESSION, PHOTO_SESSION_4_PHOTO_TAKEN)
                    st.rerun()
                    return
                else:
                    st.warning("No frame available yet. Try again in a moment.")

        # Launch webcam
        ctx = webrtc_streamer(
            key="example",
            video_processor_factory=VideoTransformer,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )

        if ctx.video_processor:
            init("CTX", ctx)
            set_session(PHOTO_SESSION, PHOTO_SESSION_3_CAMERA_ACTIVE)
           

    if get_session(PHOTO_SESSION) == PHOTO_SESSION_3_CAMERA_ACTIVE:
        st.write("Camera is active. Click 'Capture Photo' to take a photo.")

