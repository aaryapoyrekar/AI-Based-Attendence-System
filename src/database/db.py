import bcrypt
import streamlit as st

from src.database.config import supabase


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def _safe_execute(operation, default=None):
    if supabase is None:
        return default

    try:
        return operation()
    except Exception as exc:
        st.warning(f"Database unavailable: {exc}")
        return default


def check_teacher_exists(username):
    if not username:
        return False

    response = _safe_execute(
        lambda: supabase.table("teachers").select("username").eq("username", username).execute(),
        default=None,
    )
    return bool(response and getattr(response, "data", None) and len(response.data) > 0)


def create_teacher(username, password, name):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name,
    }
    response = _safe_execute(lambda: supabase.table("teachers").insert(data).execute(), default=None)
    return response.data if response else None


def teacher_login(username, password):
    response = _safe_execute(
        lambda: supabase.table("teachers").select("*").eq("username", username).execute(),
        default=None,
    )
    if response and response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher
    return None


def get_all_students():
    response = _safe_execute(lambda: supabase.table("students").select("*").execute(), default=None)
    return response.data if response else []


def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {"name": new_name, "face_embedding": face_embedding, "voice_embedding": voice_embedding}
    response = _safe_execute(lambda: supabase.table("students").insert(data).execute(), default=None)
    return response.data if response else None

def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = _safe_execute(lambda: supabase.table("subjects").insert(data).execute(), default=None)
    return response.data

def get_teacher_subjects(teacher_id):
    response = _safe_execute(lambda: supabase.table('subjects').select("*, subject_students(count), attendence_logs(timestamp)").eq("teacher_id", teacher_id).execute())
    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_student", [{}])(0).get('count', 0) if sub.gt('subject_student') else 0
        attendence = sub.get('attendence_logs', []) 
        unique_sessions = len(set(log['timestamp'] for log in attendence))
        sub['total_classes'] = unique_sessions

        sub.pop('subject_student', None)
        sub.pop('attendence_logs', None)

        return subjects 