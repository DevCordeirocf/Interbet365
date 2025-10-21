# core/user_service.py

import streamlit as st
from core.db import init_supabase_client # Importa o conector

def get_profile(user_id: str) -> dict | None:
    """
    Busca o perfil de um usuário (username, role, balance) na tabela Profiles.
    """
    supabase = init_supabase_client()
    if supabase:
        try:
            response = supabase.table('profiles').select('*').eq('id', user_id).single().execute()
            if response.data:
                return response.data
            else:
                return None
        except Exception as e:
            st.error(f"Erro ao buscar perfil: {e}")
            return None
    return None

def get_user_balance(user_id: str) -> float | None:
    """Busca especificamente o saldo do usuário."""
    profile = get_profile(user_id)
    if profile:
        return profile.get('balance', 0.0)
    return None

def update_user_balance(user_id: str, amount: float) -> bool:
    """
    Atualiza o saldo de um usuário (pode ser valor positivo ou negativo).
    """
    supabase = init_supabase_client()
    if supabase:
        try:
            current_balance = get_user_balance(user_id)
            if current_balance is None:
                return False
                
            new_balance = current_balance + amount
            
            response = supabase.table('profiles').update({'balance': new_balance}).eq('id', user_id).execute()
            
            if response.data:
                print(f"Saldo de {user_id} atualizado para {new_balance}")
                return True
            return False
        except Exception as e:
            st.error(f"Erro ao atualizar saldo: {e}")
            return False
    return False