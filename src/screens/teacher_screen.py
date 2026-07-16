import streamlit as st

from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout
from src.ui.base_layout import style_background_dashboard
from src.components.footer import footer_dashboard

from src.database.db import check_teacher_exists, create_teacher, teacher_login

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "Login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "Register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    st.header(f""" Welcome, {teacher_data['name']}!""")

def login_teacher(username, password):
    if not username or not password:
        return False
    
    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    
    return False

def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home", type="secondary", key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type']= None
            st.rerun()

    st.header("Login using password", text_alignment ="center")
    st.space()
    st.space()

    teacher_username = st.text_input("Username", placeholder="Enter your username")
    teacher_password = st.text_input("Password", placeholder="Enter your password", type="password")

    st.divider()

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("Login", icon=":material/passkey:", shortcut="control+enter", width="stretch"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Login successful!", icon="✅")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

    with btnc2:
        if st.button("Register Instead",type="primary", icon=":material/person_add:",  width="stretch"):
            st.session_state.teacher_login_type = "Register"
            
    footer_dashboard()

def register_teacher(teacher_username, teacher_pass, teacher_pass_confirm, teacher_name):
    if not teacher_username or not teacher_pass or not teacher_pass_confirm or not teacher_name:
        return False, "Please fill in all fields."
    
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."
    
    if check_teacher_exists(teacher_username):
        return False, "Username already exists."
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Teacher registered successfully! Login now."
    except Exception as e:
        return False, f"Error creating teacher: {str(e)}"
        

def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home", type="secondary", key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type']= None
            st.rerun()
    
    st.header("Register using teacher profile",text_alignment ="center")
    st.space()
    st.space()

    teacher_username = st.text_input("Username", placeholder="Enter your username")
    teacher_name = st.text_input("Name", placeholder="Enter your name")

    teacher_pass = st.text_input("Password", placeholder="Enter your password", type="password")
    teacher_pass_confirm = st.text_input("Confirm Password", placeholder="Enter your password again", type="password")


    st.divider()

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("Register now", icon=":material/passkey:", shortcut="control+enter", width="stretch"):
            success, message = register_teacher(teacher_username, teacher_pass, teacher_pass_confirm, teacher_name)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "Login"
                st.rerun()
            else:
                st.error(message)
    with btnc2:
        if st.button("Login Instead",type="primary", icon=":material/person_add:",  width="stretch"):
            st.session_state.teacher_login_type = "Login"
            
    footer_dashboard()

