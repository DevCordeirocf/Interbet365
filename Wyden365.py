# Wyden365.py
# Ponto de entrada principal e roteador da aplicação.

import streamlit as st
from streamlit_option_menu import option_menu

# Importa o CONECTOR REAL do banco de dados
from core import database

# Importa as 'views' (páginas) da nossa aplicação
from views import apostar, carteira, minhasApostas, admin

# --- 1. Configuração da Página ---
# Configura o layout da página para ser 'wide' (largo) e o menu lateral recolhido
st.set_page_config(
    page_title="Wyden365",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- 2. CSS Customizado ---
# Esconde o menu 'hambúrguer' padrão do Streamlit e o rodapé
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# --- 3. Inicialização do Cliente Supabase ---
# Inicializa o cliente uma vez e o armazena no cache do Streamlit
@st.cache_resource
def get_supabase_client():
    return database.init_supabase_client()

supabase = get_supabase_client()
if not supabase:
    st.error("Falha fatal ao conectar com o banco de dados.")
    st.stop()


# --- 4. Lógica Principal: Autenticação vs. Navegação ---

# Verifica se o usuário já está logado na sessão do Streamlit
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    
    # --- SE NÃO ESTIVER LOGADO: Mostrar telas de Login / Registro ---
    st.title("Bem-vindo ao Wyden365 🏆")
    
    login_tab, register_tab = st.tabs(["Login", "Registrar-se"])
    
    # --- Aba de Login ---
    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            login_button = st.form_submit_button("Entrar")
            
            if login_button:
                try:
                    # Tenta fazer o login com o Supabase
                    session = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })
                    user = session.user
                    
                    # Se o login deu certo, busca o perfil (saldo, role)
                    profile = database.get_profile(user.id)
                    
                    if profile:
                        # Salva tudo na sessão do Streamlit
                        st.session_state['authenticated'] = True
                        st.session_state['user_id'] = user.id
                        st.session_state['email'] = user.email
                        st.session_state['username'] = profile['username']
                        st.session_state['role'] = profile['role']
                        st.success("Login bem-sucedido!")
                        st.rerun() # Recarrega a página para o estado "logado"
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
                    try:
                        # Tenta criar o usuário no Supabase
                        # (O Trigger no BD vai criar o Perfil automaticamente)
                        session = supabase.auth.sign_up({
                            "email": email,
                            "password": password,
                            "options": {
                                # Passa o username para o Trigger que criamos
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
        # O menu principal
        selected_page = option_menu(
            menu_title=None,
            options=["Apostar", "Minhas Apostas", "Carteira", "Admin"],
            icons=["🏆", "🎟️", "💵", "⚙️"],
            orientation="horizontal",
        )
    
    with col2:
        # Mostra o nome do usuário e o botão de Sair
        st.write(f"Olá, **{st.session_state['username']}**!")
        if st.button("Sair"):
            # Limpa a sessão do Streamlit
            for key in st.session_state.keys():
                del st.session_state[key]
            supabase.auth.sign_out() # Desloga do Supabase
            st.rerun() # Recarrega para a tela de login

    # --- 6. Roteador de Páginas ---
    # Renderiza a view selecionada
    
    if selected_page == "Apostar":
        apostar.render()
        
    elif selected_page == "Minhas Apostas":
        minhasApostas.render()
        
    elif selected_page == "Carteira":
        carteira.render()
        
    elif selected_page == "Admin":
        # Proteção extra: só renderiza a página Admin se o 'role' for 'admin'
        if st.session_state['role'] == 'admin':
            admin.render()
        else:
            st.error("🔒 Acesso negado. Esta área é restrita para administradores.")