import streamlit as st
from core.db import init_supabase_client 

def get_profile(user_id: str) -> dict | None:
    supabase = init_supabase_client()
    if not supabase:
        st.error("Falha crítica: Não foi possível conectar ao banco de dados em get_profile.")
        return None
    try:
        response = supabase.table('profiles').select('*').eq('id', user_id).single().execute()
        if response.data:
            return response.data
        else:
            print(f"Perfil não encontrado para user_id: {user_id}")
            return None
    except Exception as e:
        error_message = str(e) if e else "Erro desconhecido na busca de perfil por ID"
        st.error(f"Erro ao buscar perfil por ID: {error_message}")
        return None


def get_user_by_username(username: str) -> dict | None:
    supabase = init_supabase_client()
    if not supabase:
        st.error("Falha crítica: Não foi possível conectar ao banco de dados em get_user_by_username.")
        return None
    try:
        response = supabase.table('profiles').select('id, username').eq('username', username).maybe_single().execute()
        print(f"Resposta da busca por username '{username}': {response}")
        if response.data:
            return response.data 
        else:
            return None 
            
    except Exception as e:
        error_message = str(e) if e else "Erro desconhecido na busca por username"
        return None


def get_user_balance(user_id: str) -> float | None:
    profile = get_profile(user_id)
    if profile:
        return profile.get('balance', 0.0) if profile.get('balance') is not None else 0.0
    print(f"Não foi possível obter saldo para user_id {user_id} pois o perfil não foi encontrado.")
    return None

def update_user_balance(user_id: str, amount: float) -> bool:
    supabase = init_supabase_client()
    if not supabase:
        st.error("Falha crítica: Não foi possível conectar ao banco de dados em update_user_balance.")
        return False
    try:
        current_balance = get_user_balance(user_id)
        if current_balance is None:
            return False
            
        new_balance = (current_balance or 0.0) + amount
        
        print(f"Tentando atualizar saldo de {user_id}: {current_balance} + {amount} -> {new_balance}")    
        response = supabase.table('profiles').update({'balance': new_balance}).eq('id', user_id).execute()
        
        if response.data:
            print(f"Saldo de {user_id} atualizado com sucesso para {new_balance}")
            return True
        else:
            print(f"Falha ao atualizar saldo para user_id {user_id}. Resposta Supabase: {response}")
            st.error("Não foi possível atualizar o saldo no banco de dados.")
            return False
    except Exception as e:
        error_message = str(e) if e else "Erro desconhecido na atualização de saldo"
        st.error(f"Erro ao atualizar saldo: {error_message}")
        return False

