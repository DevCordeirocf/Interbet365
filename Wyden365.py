# Wyden365.py
# Ponto de entrada principal e roteador da aplicação.

import streamlit as st
from streamlit_option_menu import option_menu

# Importa o CONECTOR REAL do banco de dados e os SERVIÇOS
from core.db import init_supabase_client
from core import user_service 

# Importa as 'views' (páginas) da nossa aplicação
from views import apostar, carteira, minhasApostas, admin

# Importa os estilos
from styles import load_auth_styles, render_brand, render_footer

# --- 1. Configuração da Página ---
st.set_page_config(
    page_title="Wyden365",
    page_icon="🐯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- 2. CSS Customizado ---
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 3. Inicialização do Cliente Supabase ---
@st.cache_resource
def get_supabase_client():
    return init_supabase_client()

supabase = get_supabase_client()
if not supabase:
    st.error("Falha fatal ao conectar com o banco de dados.")
    st.stop()

# --- 4. Lógica Principal: Navegação ---

# Renderiza a marca
render_brand(subtitle="Apostas Universitárias")

# Menu de navegação principal
selected = option_menu(
    menu_title=None,
    options=["Apostar", "Carteira", "Minhas Apostas", "Login"],
    icons=["currency-exchange", "wallet", "list-check", "person"],
    orientation="horizontal",
    default_index=0
)

# Roteamento das páginas
if selected == "Apostar":
    apostar.render()
elif selected == "Carteira":
    if 'authenticated' in st.session_state and st.session_state['authenticated']:
        carteira.render()
    else:
        st.warning("🔒 Você precisa fazer login para acessar sua carteira.")
elif selected == "Minhas Apostas":
    if 'authenticated' in st.session_state and st.session_state['authenticated']:
        minhasApostas.render()
    else:
        st.warning("🔒 Você precisa fazer login para ver suas apostas.")
elif selected == "Login":
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        # Carrega os estilos de autenticação
        load_auth_styles()
        
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
                        if email and password:
                            # Tenta fazer login
                            success, user = user_service.login_user(supabase, email, password)
                            
                            if success:
                                st.success("✅ Login realizado com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Email ou senha inválidos.")
                        else:
                            st.error("Por favor, preencha todos os campos.")
            
            # --- Aba de Registro ---
            with register_tab:
                with st.form("register_form"):
                    new_username = st.text_input("Nome de Usuário")
                    new_email = st.text_input("Email", placeholder="seu@email.com")
                    new_password = st.text_input("Senha", type="password", placeholder="••••••••")
                    confirm_password = st.text_input("Confirme a Senha", type="password", placeholder="••••••••")
                    register_button = st.form_submit_button("Registrar")
                    
                    if register_button:
                        if new_username and new_email and new_password and confirm_password:
                            if new_password == confirm_password:
                                # Tenta registrar o usuário
                                success = user_service.register_user(supabase, new_email, new_password, new_username)
                                
                                if success:
                                    st.success("✅ Conta criada com sucesso! Faça login para continuar.")
                                else:
                                    st.error("❌ Erro ao criar conta. Este email já está em uso.")
                            else:
                                st.error("As senhas não coincidem.")
                        else:
                            st.error("Por favor, preencha todos os campos.")
    else:
        # Se já estiver logado, mostrar informações do usuário e botão de logout
        st.write(f"Olá, **{st.session_state['username']}**!")
        if st.button("Sair"):
            for key in st.session_state.keys():
                del st.session_state[key]
            supabase.auth.sign_out()
            st.rerun()

render_footer()