import streamlit as st
import numpy as np
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.pipelines.face_pipeline import predict_attendence

def student_screen():
    style_background_dashboard()
    style_base_layout()
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home", type="secondary", key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type']= None
            st.rerun()
    st.header("Login using faceID", text_alignment ="center")
    st.space()
    st.space()

    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner('AI is scanning...'):
            detected,all_ids, num_faces = predict_attendence(img)

            if num_faces == 0:
                st.warning('Face not found!')
            


    footer_dashboard()