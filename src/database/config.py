import os

import streamlit as st
from supabase import Client, create_client


def get_supabase_client() -> Client | None:
    try:
        supabase_url = st.secrets.get("supabase_url")
        supabase_key = st.secrets.get("supabase_key")
    except Exception:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        return None

    return create_client(supabase_url, supabase_key)


supabase: Client | None = get_supabase_client()