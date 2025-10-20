# core/database.py

import streamlit as st
from supabase import create_client, Client

def init_supabase_client() -> Client | None:
    """
    Inicializa e retorna o cliente Supabase.
    Lê as credenciais do arquivo secrets.toml do Streamlit.
    """
    try:
        url = st.secrets["supabase_url"]
        key = st.secrets["supabase_key"]
        return create_client(url, key)
    except KeyError:
        st.error("Erro: Credenciais do Supabase (url ou key) não encontradas em secrets.toml.")
        return None
    except Exception as e:
        st.error(f"Erro ao inicializar o cliente Supabase: {e}")
        return None

def get_profile(user_id: str) -> dict | None:
    """
    Busca o perfil de um usuário (username, role, balance) na tabela Profiles
    usando o ID de usuário do Supabase.
    """
    supabase = init_supabase_client()
    if supabase:
        try:
            # Seleciona todas as colunas (*) da tabela 'Profiles'
            # Onde a coluna 'id' for igual ao user_id fornecido
            # .single() garante que esperamos apenas um resultado
            response = supabase.table('Profiles').select('*').eq('id', user_id).single().execute()
            
            if response.data:
                return response.data
            else:
                st.warning(f"Nenhum perfil encontrado para o usuário {user_id}.")
                return None
        except Exception as e:
            st.error(f"Erro ao buscar perfil: {e}")
            return None
    return None

def get_user_balance(user_id: str) -> float | None:
    """
    Busca especificamente o saldo do usuário.
    """
    profile = get_profile(user_id)
    if profile:
        return profile.get('balance', 0.0)
    return None

def update_user_balance(user_id: str, amount: float) -> bool:
    """
    Atualiza o saldo de um usuário.
    Esta função usa 'rpc' para chamar uma função no banco de dados
    para uma atualização segura.
    (Isto requer a criação de uma função 'update_balance' no Supabase)
    
    Abordagem Simples (menos segura, mas funciona):
    """
    supabase = init_supabase_client()
    if supabase:
        try:
            current_balance = get_user_balance(user_id)
            if current_balance is None:
                return False
                
            new_balance = current_balance + amount
            
            response = supabase.table('Profiles').update({'balance': new_balance}).eq('id', user_id).execute()
            
            if response.data:
                print(f"Saldo de {user_id} atualizado para {new_balance}")
                return True
            return False
        except Exception as e:
            st.error(f"Erro ao atualizar saldo: {e}")
            return False
    return False

# 
# AQUI VOCÊ ADICIONARÁ TODAS AS OUTRAS FUNÇÕES DE BANCO DE DADOS:
#
# def get_open_matches(): ...
# def create_bet(...): ...
# def get_all_modalities(): ...
# ... etc ...
#