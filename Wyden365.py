import streamlit as st
from streamlit_option_menu import option_menu

from core.db import init_supabase_client

from views import apostar, carteira, minhasApostas, admin, login_page, baccarat 

from styles.betting import load_betting_styles
from styles.sidebar import load_sidebar_styles, render_sidebar_header, render_user_area

st.set_page_config(
    page_title="InterBet 365",
    page_icon="🐯",
    layout="wide",
    initial_sidebar_state="expanded",
)

custom_style = """
<style>
/* Esconde o rodapé */
footer {visibility: hidden;}

/* Esconde o botão de Deploy */
button[kind="header"] {display: none !important;}

/* Esconde título, logo e toolbar */
header [data-testid="stHeader"] {display: none !important;}
div[data-testid="stToolbar"] {background: transparent !important;}
}

/* Deixa só o botão de menu hambúrguer visível */
button[title="Main menu"] {
    visibility: visible !important;
    position: fixed !important;
    top: 10px !important;
    left: 10px !important;
    z-index: 9999 !important;
    opacity: 0.8 !important;
}

/* Remove sombra e bordas da barra superior */
header {
    background: transparent !important;
    box-shadow: none !important;
}
</style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

# --- 2. CSS Customizado ---
hide_streamlit_style = """
<style>
footer {visibility: hidden;}
section[data-testid="stSidebar"] {
    padding-top: 0rem;
}
.block-container {
    padding-top: 0rem;
    padding-bottom: 5rem;
}

/* Se quiser remover novamente a sidebar ou deploy no futuro, basta descomentar:
div[data-testid="stToolbar"] { display: none; }
.stDeployButton { display: none; }
*/
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 3. Inicialização do Cliente Supabase ---
@st.cache_resource
def get_supabase_client():
    return init_supabase_client()
supabase = get_supabase_client()
if not supabase:
    st.error("Falha ao conectar com o banco de dados."); st.stop()

# --- 4. Gerenciamento de Estado da View ---
is_logged_in = 'authenticated' in st.session_state and st.session_state['authenticated']

if not is_logged_in and 'view' not in st.session_state:
    st.session_state['view'] = 'browse'

# --- 5. SIDEBAR (APARECE EM TODAS AS TELAS EXCETO LOGIN) ---
def render_sidebar():
    """Renderiza a sidebar para todas as páginas exceto login"""
    
    # Carrega os estilos da sidebar
    load_sidebar_styles()
    
    with st.sidebar:
        # Header da sidebar
        render_sidebar_header()
        
        if is_logged_in:
            # Menu de navegação para usuários logados
            menu_options = ["Apostar", "Baccarat", "Minhas Apostas", "Carteira"]
            if st.session_state.get('role') == 'admin':
                menu_options.append("Admin")
            
            selected = option_menu(
                menu_title="",  # Título vazio
                options=menu_options,
                icons=["🏆", "🎲", "🎟️", "💵", "⚙️"] if st.session_state.get('role') == 'admin' else ["🏆", "🎲", "🎟️", "💵"],
                menu_icon="",
                default_index=0,
                styles={
                    "container": {
                        "padding": "0!important", 
                        "background-color": "linear-gradient(180deg, hsl(250, 15%, 8%), hsl(250, 15%, 5%))",
                        "border-radius": "1px",
                        "margin": "0!important"
                    },
                    "icon": {"color": "#FF462C", "font-size": "14px"}, 
                    "nav-link": {
                        "font-size": "14px", 
                        "text-align": "left", 
                        "border-radius": "8px",
                        "color": "rgba(255, 255, 255, 0.7)",
                        "padding": "0.6rem 1rem",
                        "width": "100%",
                        "background": "transparent",
                        "box-shadow": "none"
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(135deg, #FF462C, #A0153E)",
                        "color": "white",
                        "box-shadow": "0 4px 15px rgba(255, 70, 44, 0.3)"
                    },
                }
            )
            
            # Atualiza a página selecionada no session_state
            st.session_state['selected_page'] = selected
            
            # Área do usuário no final da sidebar
            st.markdown("<div style='height: 213px;'></div>", unsafe_allow_html=True)
            render_user_area(st.session_state['username'], st.session_state['email'])
            
            if st.button("Sair", use_container_width=True, key="sidebar_logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                try:
                    supabase.auth.sign_out()
                except:
                    pass
                st.session_state['view'] = 'browse'
                st.rerun()
        
        else:
            # Menu para usuários não logados
            st.info("Faça login para acessar todas as funcionalidades.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login", use_container_width=True, key="sidebar_login"):
                    st.session_state['view'] = 'login'
                    st.rerun()
            with col2:
                if st.button("Registrar", use_container_width=True, key="sidebar_register"):
                    st.session_state['view'] = 'login'
                    st.rerun()

# --- 6. ROTEAMENTO PRINCIPAL ---

# --- ESTADO 1: USUÁRIO ESTÁ LOGADO ---
if is_logged_in:
    # Renderiza a sidebar PRIMEIRO
    render_sidebar()
    
    # Carrega estilos
    load_betting_styles()
    
    # Determina a página selecionada
    selected_page = st.session_state.get('selected_page', 'Apostar')
    
    # Roteador de Páginas (Logado)
    if selected_page == "Apostar":
        apostar.render()
    elif selected_page == "Baccarat":
        baccarat.render()
    elif selected_page == "Minhas Apostas":
        minhasApostas.render()
    elif selected_page == "Carteira":
        carteira.render()
    elif selected_page == "Admin":
        admin.render()

# --- ESTADO 2: CONVIDADO QUER FAZER LOGIN ---
elif st.session_state.get('view') == 'login':
    # Página de login - SEM SIDEBAR
    login_page.render()

# --- ESTADO 3: CONVIDADO ESTÁ NAVEGANDO (DEFAULT) ---
else:
    # Visitante - COM SIDEBAR
    render_sidebar()
    load_betting_styles()
    
    # Pode apenas ver as apostas
    apostar.render()
    
    # Mensagem para convidados
    st.markdown("---")
    st.info("Faça login para poder fazer apostas e acessar todas as funcionalidades!")