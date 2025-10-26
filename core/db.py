# core/db.py

import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

def init_supabase_client() -> Client | None:
    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        
        return create_client(url, key)
    except KeyError:
        st.error("Erro: Credenciais do Supabase (SUPABASE_URL ou SUPABASE_SERVICE_KEY) não encontradas no .env.")
        return None
    except Exception as e:
        st.error(f"Erro ao inicializar o cliente Supabase: {e}")
        return None