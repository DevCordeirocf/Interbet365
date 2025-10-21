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


# --- 4. Lógica Principal: Autenticação vs. Navegação ---

if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    
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
                        
                        # Busca o perfil do usuário
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
                username = st.text_input("Nome de Usuário", placeholder="Escolha um nome único")
                email = st.text_input("Email", placeholder="seu@email.com")
                password = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres")
                register_button = st.form_submit_button("Criar conta")
                
                if register_button:
                    if not username:
                        st.warning("Nome de usuário é obrigatório.")
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
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Renderiza o rodapé
        render_footer()

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
        minhasApostas.render()
        
    elif selected_page == "Carteira":
        carteira.render()
        
    elif selected_page == "Admin":
        if st.session_state['role'] == 'admin':
            admin.render()
        else:
            st.error("🔒 Acesso negado. Esta área é restrita para administradores.")