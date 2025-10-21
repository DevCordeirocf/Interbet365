# views/login_page.py

import streamlit as st
from core.db import init_supabase_client
from core import user_service
from styles import load_auth_styles, render_brand, render_footer

# Inicializa o cliente Supabase para ser usado nesta view
@st.cache_resource
def get_supabase_client():
    return init_supabase_client()
supabase = get_supabase_client()

def render():
    """Renderiza a tela de login/registro centralizada e em tela cheia."""
    
    # Carrega os estilos de autenticação
    load_auth_styles()
    
    # Renderiza a marca
    render_brand(subtitle="Apostas Universitárias")
    
    # Centraliza o conteúdo
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        login_tab, register_tab = st.tabs(["Login", "Registrar-se"])
        
        # --- Aba de Login ---
        with login_tab:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="seu@email.com")
                password = st.text_input("Senha", type="password", placeholder="••••••••")
                login_button = st.form_submit_button("Entrar")
                
                if login_button:
                    try:
                        session = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        user = session.user
                        profile = user_service.get_profile(user.id)
                        
                        if profile:
                            st.session_state['authenticated'] = True
                            st.session_state['user_id'] = user.id
                            st.session_state['email'] = user.email
                            st.session_state['username'] = profile['username']
                            st.session_state['role'] = profile['role']
                            st.rerun() # Recarrega para o Wyden365.py mostrar o app
                        else:
                            st.error("Login bem-sucedido, mas não foi possível encontrar seu perfil.")
                    except Exception as e:
                        st.error(f"Erro no login: Usuário ou senha inválidos.")

        # --- Aba de Registro ---
        with register_tab:
            with st.form("register_form"):
                username = st.text_input("Nome de Usuário", placeholder="Escolha um nome único")
                email = st.text_input("Email", placeholder="seu@email.com")
                password = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres")
                register_button = st.form_submit_button("Criar conta")
                
                if register_button:
                    # ... (Lógica de registro com verificação de username) ...
                    try:
                        session = supabase.auth.sign_up({
                            "email": email,
                            "password": password,
                            "options": {"data": {"username": username}}
                        })
                        st.success("Registro realizado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro no registro: {e}")
        
    # Renderiza o rodapé
    render_footer()