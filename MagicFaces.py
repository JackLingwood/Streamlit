import streamlit as st
import cv2
import numpy as np
import tempfile
from PIL import Image
import mediapipe as mp
import face_recognition

import torch


def get_blue_monkeys():
    st.title("🛂 Passport Photo Validator – Face Visibility Check")

    uploaded_file = st.file_uploader("Upload your passport-style photo", type=["jpg", "jpeg", "png"])

    def mediapipe_face_detect(image_np):
        mp_face = mp.solutions.face_detection
        with mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
            results = detector.process(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
            print(f"MediaPipe detected {len(results.detections) if results.detections else 0} face(s).")
            print("Detection results:")
            print(results)
            st.write("Face probability:", results.detections[0].score[0] if results.detections else "No face detected")
            return results.detections
        

    def face_recognition_detect(image_np):
        rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        st.write(f"face_recognition detected {len(boxes)} face(s).")
        st.write("Face locations:")
        st.write(boxes)


        return boxes




    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        


        # Convert to OpenCV image
        image_np = np.array(image)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        st.write("Second opinion on face visibility...")
        boxes = face_recognition_detect(image_np)



        # Step 1: Try MediaPipe
        detections = mediapipe_face_detect(image_np)

        if detections:
            print(f"Detected {len(detections)} face(s) using MediaPipe.")
            print(detections)
            for detection in detections:
                bboxC = detection.location_data.relative_bounding_box
                h, w, _ = image_np.shape
                x, y, width, height = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                cv2.rectangle(image_np, (x, y), (x + width, y + height), (0, 255, 0), 2)


            st.success("✅ Face detected using MediaPipe!")
            st.write("Photo is likely acceptable.")
        else:
            st.warning("⚠️ No face detected with MediaPipe. Trying fallback...")

            boxes = face_recognition_detect(image_np)

            if boxes:
                print(f"Detected {len(boxes)} face(s) using face_recognition.")
                print(boxes)


                st.info("✅ Face detected using face_recognition (fallback)")
                st.write("Warning: Image quality may be marginal or face may be partially obstructed.")
            else:
                st.error("❌ No face detected. Photo may be obstructed or invalid.")
                st.markdown("""
                **Possible reasons:**
                - Face is covered (mask, sunglasses, hand, hair)
                - Poor lighting or shadows
                - Face too small or out of frame
                - Low resolution or blur
                """)

