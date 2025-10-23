# core/db.py

import streamlit as st
from supabase import create_client, Client

def init_supabase_client() -> Client | None:
    try:
        url = st.secrets["supabase_url"]
        key = st.secrets["supabase_service_key"]
        
        return create_client(url, key)
    except KeyError:
        st.error("Erro: Credenciais do Supabase (url ou service_key) não encontradas em secrets.toml.")
        return None
    except Exception as e:
        st.error(f"Erro ao inicializar o cliente Supabase: {e}")
        return None