# Wyden365.py
# Ponto de entrada principal e roteador da aplicação.

import streamlit as st
from streamlit_option_menu import option_menu

# Importa o CONECTOR REAL do banco de dados e os SERVIÇOS
from core.db import init_supabase_client
from core import user_service 
# Importa as 'views' (páginas) da nossa aplicação
from views import apostar, carteira, minhasApostas, admin # Mantive seu nome 'minhasApostas'

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


# --- 4. Lógica Principal: Autenticação vs. Navegação ---

if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    
    st.title("Bem-vindo ao Wyden365 ")
    
    login_tab, register_tab = st.tabs(["Login", "Registrar-se"])
    
    # --- Aba de Login ---
    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            login_button = st.form_submit_button("Entrar")
            
            if login_button:
                
                try:
                    session = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    user = session.user
                    
                    # =========================================================
                    # MUDANÇA AQUI: Trocado 'database' por 'user_service'
                    # =========================================================
                    profile = user_service.get_profile(user.id)
                    
                    if profile:
                        st.session_state['authenticated'] = True
                        st.session_state['user_id'] = user.id
                        st.session_state['email'] = user.email
                        st.session_state['username'] = profile['username']
                        st.session_state['role'] = profile['role']
                        st.success("Login bem-sucedido!")
                        st.rerun()
                    else:
                        st.error("Login bem-sucedido, mas não foi possível encontrar seu perfil.")
                        
                except Exception as e:
                    st.error(f"Erro no login: Usuário ou senha inválidos.")

    # --- Aba de Registro ---
    with register_tab:
        with st.form("register_form"):
            username = st.text_input("Nome de Usuário (único)")
            email = st.text_input("Email de Registro")
            password = st.text_input("Senha de Registro", type="password")
            register_button = st.form_submit_button("Criar Conta")
            
            if register_button:
                if not username:
                    st.warning("Nome de usuário é obrigatório.")
                else:
                    # =========================================================
                    # MUDANÇA AQUI: Lógica de negócio movida para o 'user_service'
                    # =========================================================
                    username_exists = user_service.does_username_exist(username)

                    if username_exists:
                        st.error("Este nome de usuário já está em uso. Escolha outro.")
                    else:
                        try:
                            session = supabase.auth.sign_up({
                                "email": email,
                                "password": password,
                                "options": {
                                    "data": {"username": username} 
                                }
                            })
                            st.success("Registro realizado com sucesso! Verifique seu e-mail para confirmar a conta.")
                        except Exception as e:
                            st.error(f"Erro no registro: {e}")

else:
    # --- SE ESTIVER LOGADO: Mostrar o Header de Navegação e as Páginas ---
    
    # --- 5. Header de Navegação ---
    col1, col2 = st.columns([0.8, 0.2])

    with col1:
        selected_page = option_menu(
            menu_title=None,
            options=["Apostar", "Minhas Apostas", "Carteira", "Admin"],
            icons=["🏆", "🎟️", "💵", "⚙️"],
            orientation="horizontal",
        )
    
    with col2:
        st.write(f"Olá, **{st.session_state['username']}**!")
        if st.button("Sair"):
            for key in st.session_state.keys():
                del st.session_state[key]
            supabase.auth.sign_out()
            st.rerun()

    # --- 6. Roteador de Páginas ---
    
    if selected_page == "Apostar":
        apostar.render()
        
    elif selected_page == "Minhas Apostas":
        minhasApostas.render() # <-- Mantendo sua nomenclatura
        
    elif selected_page == "Carteira":
        carteira.render()
        
    elif selected_page == "Admin":
        if st.session_state['role'] == 'admin':
            admin.render()
        else:
            st.error("🔒 Acesso negado. Esta área é restrita para administradores.")