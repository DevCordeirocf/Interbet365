# Wyden365.py
# Ponto de entrada principal e roteador da aplicação.

import streamlit as st
from streamlit_option_menu import option_menu

# Importa o CONECTOR REAL e os SERVIÇOS
from core.db import init_supabase_client
from core import user_service 

# Importa as 'views' (páginas)
from views import apostar, carteira, minhasApostas, admin, login_page

# Importa os estilos
from styles import load_auth_styles, render_brand, render_footer

# --- 1. Configuração da Página ---
st.set_page_config(
    page_title="Wyden365",
    page_icon="🏆", # Ícone original
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
    st.error("Falha fatal ao conectar com o banco de dados."); st.stop()


# --- 4. Gerenciamento de Estado da View ---
is_logged_in = 'authenticated' in st.session_state and st.session_state['authenticated']

# Define o estado de view padrão para convidados
if not is_logged_in and 'view' not in st.session_state:
    st.session_state['view'] = 'browse' # 'browse' ou 'login'


# --- 5. Roteamento de Layout Principal ---

# --- ESTADO 1: USUÁRIO ESTÁ LOGADO ---
if is_logged_in:
    # Renderiza o header de usuário logado
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        options = ["Apostar", "Minhas Apostas", "Carteira"]
        icons = ["🏆", "🎟️", "💵"]
        if st.session_state.get('role') == 'admin':
            options.append("Admin")
            icons.append("⚙️")

        selected_page = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            orientation="horizontal",
        )
    with col2:
        st.write(f"Olá, **{st.session_state['username']}**!")
        if st.button("Sair"):
            for key in st.session_state.keys():
                del st.session_state[key]
            supabase.auth.sign_out()
            st.session_state['view'] = 'browse' # Define a view padrão para convidados
            st.rerun()

    # Roteador de Páginas (Logado)
    if selected_page == "Apostar":
        apostar.render()
    elif selected_page == "Minhas Apostas":
        minhasApostas.render()
    elif selected_page == "Carteira":
        carteira.render()
    elif selected_page == "Admin":
        admin.render()

# --- ESTADO 2: CONVIDADO QUER FAZER LOGIN ---
elif st.session_state.get('view') == 'login':
    # Renderiza a página de login em tela cheia
    login_page.render()

# --- ESTADO 3: CONVIDADO ESTÁ NAVEGANDO (DEFAULT) ---
else: # (not is_logged_in and st.session_state.get('view') == 'browse')
    # Renderiza o header de convidado
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        selected_page = option_menu(
            menu_title=None,
            options=["Apostar", "Minhas Apostas", "Carteira"],
            icons=["🏆", "🎟️", "💵"],
            orientation="horizontal",
        )
    with col2:
        col_login, col_reg = st.columns(2)
        with col_login:
            if st.button("Login", use_container_width=True):
                st.session_state['view'] = 'login' # Muda o estado para o layout de login
                st.rerun()
        with col_reg:
            if st.button("Registrar-se", use_container_width=True):
                st.session_state['view'] = 'login' # Muda o estado para o layout de login
                st.rerun()

    # Roteador de Páginas (Convidado)
    if selected_page == "Apostar":
        apostar.render()
    elif selected_page == "Minhas Apostas" or selected_page == "Carteira":
        # Se clicar em uma página protegida, muda o estado para login
        st.session_state['view'] = 'login'
        st.rerun()