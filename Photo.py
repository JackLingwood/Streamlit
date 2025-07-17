
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
#import cv2
#import av
import numpy as np

def take_photo():
    st.title(" Webcam Photo Capture with Streamlit")

    # State to store the captured image
    if 'captured_image' not in st.session_state:
        st.session_state['captured_image'] = None

    # Transformer class to show webcam feed and optionally capture frame
    class VideoTransformer(VideoTransformerBase):
        def __init__(self):
            self.frame = None
            self.capture = False

        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")
            self.frame = img
            return img

    # Launch webcam
    ctx = webrtc_streamer(
        key="example",
        video_processor_factory=VideoTransformer,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    # Capture button
    if ctx.video_processor:
        if st.button("Capture Photo"):
            img = ctx.video_processor.frame
            if img is not None:
                st.session_state['captured_image'] = img
            else:
                st.warning("No frame available yet. Try again in a moment.")

    # Display captured image
    if st.session_state['captured_image'] is not None:
        st.subheader("Captured Image")
        st.image(st.session_state['captured_image'], channels="BGR")


take_photo()