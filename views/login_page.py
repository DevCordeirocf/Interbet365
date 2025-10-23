import streamlit as st
from core.db import init_supabase_client
from core import user_service
from styles import load_auth_styles, render_brand, render_footer

@st.cache_resource
def get_supabase_client():
    return init_supabase_client()
supabase = get_supabase_client()

def render():
    
    load_auth_styles()
    
    render_brand(subtitle="Apostas Universitárias")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            
            login_tab, register_tab = st.tabs(["Login", "Registrar-se"])
            
            with login_tab:
                
                with st.form("login_form"):
                    email = st.text_input(
                        "Email", 
                        placeholder="seu@email.com",
                        key="login_email"
                    )
                    password = st.text_input(
                        "Senha", 
                        type="password", 
                        placeholder="••••••••",
                        key="login_password"
                    )
                    login_button = st.form_submit_button("Entrar", use_container_width=True)
                    
                    if login_button:
                        if not email or not password:
                            st.error("Por favor, preencha todos os campos.")
                        else:
                            try:
                                session = supabase.auth.sign_in_with_password({
                                    "email": email,
                                    "password": password
                                })
                                user = session.user
                                # Tenta buscar o perfil do usuário
                                profile = user_service.get_profile(user.id)
                                
                                if profile:
                                    st.session_state['authenticated'] = True
                                    st.session_state['user_id'] = user.id
                                    st.session_state['email'] = user.email
                                    st.session_state['username'] = profile['username']
                                    st.session_state['role'] = profile['role']
                                    st.success("Login realizado com sucesso!")
                                    st.rerun() # Redireciona para a página principal
                                else:
                                    # Se o login foi ok mas não achou perfil, ainda é erro
                                    st.error("Usuário ou senha inválidos.")
                            except Exception as e:
                                # Captura erros de senha errada ou usuário não existe
                                st.error(f"Erro no login: Usuário ou senha inválidos.")

            with register_tab:
                
                with st.form("register_form"):
                    username = st.text_input(
                        "Nome de Usuário", 
                        placeholder="Escolha um nome único",
                        key="register_username"
                    )
                    email = st.text_input(
                        "Email", 
                        placeholder="seu@email.com",
                        key="register_email"
                    )
                    password = st.text_input(
                        "Senha", 
                        type="password", 
                        placeholder="Mínimo 6 caracteres",
                        key="register_password"
                    )
                    register_button = st.form_submit_button("Criar conta", use_container_width=True)
                    
                    if register_button:
                        if not username or not email or not password:
                            st.error("Por favor, preencha todos os campos.")
                        elif len(password) < 6:
                            st.error("A senha deve ter pelo menos 6 caracteres.")
                        else:
                            try:
                                # --- CORREÇÃO APLICADA AQUI ---
                                # Verifica se o username já existe usando a função correta
                                existing_user = user_service.get_user_by_username(username) 
                                # -----------------------------
                                
                                if existing_user:
                                    st.error("Este nome de usuário já está em uso.")
                                else:
                                    # Tenta criar o usuário no Supabase Auth
                                    session = supabase.auth.sign_up({
                                        "email": email,
                                        "password": password,
                                        # Passa o username nos metadados para o trigger usar
                                        "options": {"data": {"username": username}} 
                                    })
                                    st.success("Registro realizado com sucesso! Verifique seu email para confirmar a conta.")
                                    # Você pode querer limpar o formulário ou redirecionar aqui
                            except Exception as e:
                                # Tenta dar uma mensagem de erro mais útil
                                error_message = str(e)
                                if "User already registered" in error_message:
                                     st.error("Este e-mail já está em uso.")
                                elif "check constraint" in error_message or "duplicate key" in error_message:
                                     st.error("Erro ao salvar perfil. Tente outro nome de usuário.")
                                else:
                                     st.error(f"Erro no registro: {error_message}")
            
        
    render_footer()
