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


def _response_data(response, default=None):
    if response is None:
        return default
    return getattr(response, "data", default)


def check_teacher_exists(username):
    if not username:
        return False

    response = _safe_execute(
        lambda: supabase.table("teachers").select("username").eq("username", username).execute(),
        default=None,
    )
    data = _response_data(response, default=[])
    return bool(data and len(data) > 0)


def create_teacher(username, password, name):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name,
    }
    response = _safe_execute(lambda: supabase.table("teachers").insert(data).execute(), default=None)
    return _response_data(response)


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
    return _response_data(response, default=[])


def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {"name": new_name, "face_embedding": face_embedding, "voice_embedding": voice_embedding}
    response = _safe_execute(lambda: supabase.table("students").insert(data).execute(), default=None)
    return _response_data(response)

def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = _safe_execute(lambda: supabase.table("subjects").insert(data).execute(), default=None)
    return _response_data(response)

def get_teacher_subjects(teacher_id):
    response = _safe_execute(lambda: supabase.table('subjects').select("*, subject_students(count), attendence_logs(timestamp)").eq("teacher_id", teacher_id).execute(), default=None)
    subjects = _response_data(response, default=[])

    for sub in subjects:
        total_students = 0
        student_counts = sub.get("subject_students", [])
        if isinstance(student_counts, list) and student_counts:
            total_students = student_counts[0].get('count', 0)
        sub['total_students'] = total_students

        attendence = sub.get('attendence_logs', [])
        unique_sessions = len(set(log.get('timestamp') for log in attendence if isinstance(log, dict)))
        sub['total_classes'] = unique_sessions

        sub.pop('subject_students', None)
        sub.pop('attendence_logs', None)

    return subjects 

def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, 'subject_id': subject_id}
    response = _safe_execute(lambda: supabase.table('subject_students').insert(data).execute(), default=None)
    return _response_data(response)

def unenroll_student_to_subject(student_id, subject_id):
    response = _safe_execute(lambda: supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute(), default=None)
    return _response_data(response)

def get_student_subjects(student_id):
    response = _safe_execute(lambda: supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute(), default=None)
    return _response_data(response, default=[])

def get_student_attendence(student_id):
    response = _safe_execute(lambda: supabase.table('attendence_logs').select('*, subjects(*)').eq('student_id', student_id).execute(), default=None)
    return _response_data(response, default=[])