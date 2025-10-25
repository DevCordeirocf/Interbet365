
import streamlit as st

def load_sidebar_styles():

    st.markdown("""
    <style>
    /* ==============================
       SIDEBAR PRINCIPAL
    ============================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, hsl(250, 15%, 8%), hsl(250, 15%, 5%)) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        /* Usa flexbox para permitir posicionar a user-area no final */
        display: flex !important;
        flex-direction: column !important;
        height: 100vh !important;
        box-sizing: border-box !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #FF462C, #A0153E) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        height: 2.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 70, 44, 0.3) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #A0153E, #FF462C) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(255, 70, 44, 0.4) !important;
    }
    
    /* ==============================
       HEADER DA SIDEBAR
    ============================== */
    .sidebar-header {
        text-align: left !important;
        margin-bottom: 2rem !important;
        padding: 0 0.5rem !important;
    }
    
    .sidebar-title {
        font-size: 2rem;
        font-weight: 900;
        background: #FF462C;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 25px rgba(255, 70, 44, 0.25);
        letter-spacing: -0.02em;
        user-select: none;
    }
    
    .sidebar-subtitle {
        color: #666 !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }
    
    /* ==============================
       MENU DE NAVEGAÇÃO
    ============================== */
    .st-emotion-cache-16txtl3 {
        padding: 1rem 0.5rem !important;
    }
    
    /* Remove o título*/
    [data-testid="stSidebarNav"] .css-1r6slb0 {
        display: none !important;
    }
    
    /* Container do menu */
    [data-testid="stSidebar"] [data-baseweb="menu"] {
        background: transparent !important;
        padding: 0 !important;
    }
    
    /* Itens do menu */
    [data-testid="stSidebar"] [data-baseweb="tab"] {
        padding: 0.75rem 1rem !important;
        margin: 0.25rem 0 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        background: transparent !important; /* mantém a mesma cor da navbar */
        border: none !important;
        color: rgba(255, 255, 255, 0.7) !important;
        transition: all 0.3s ease !important;
        justify-content: flex-start !important;
        text-align: left !important;
    }
    
    /* Item selecionado */
    [data-testid="stSidebar"] [aria-selected="true"] {
        background: linear-gradient(135deg, #FF462C, #A0153E) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(255, 70, 44, 0.3) !important;
    }
    
    /* Hover nos itens */
    [data-testid="stSidebar"] [data-baseweb="tab"]:hover {
        background: rgba(255, 70, 44, 0.06) !important; /* leve destaque no hover */
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* ==============================
       ÁREA DO USUÁRIO (FINAL)
    ============================== */
    /* Garante que a user-area fique ancorada ao rodapé da sidebar */
    .user-area {
        margin-top: auto !important; /* empurra para o final do container flex */
        left: 1rem !important;
        right: 1rem !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        /* Espaço extra acima para separar do botão Sair */
        margin-bottom: 1.5rem !important;
    }

    /* Separador visual acima da área do usuário */
    .user-area::before {
        content: "";
        display: block;
        height: 8px;
        width: 100%;
    }
    
    .user-name {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin: 0 0 0.25rem 0 !important;
    }
    
    .user-email {
        color: #888 !important;
        font-size: 0.75rem !important;
        margin: 0 0 0.75rem 0 !important;
    }
    
    /* ==============================
       INFO BOX PARA CONVIDADOS
    ============================== */
    [data-testid="stSidebar"] .stAlert {
        background: rgba(255, 70, 44, 0.1) !important;
        border: 1px solid rgba(255, 70, 44, 0.3) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }
    
    [data-testid="stSidebar"] .stAlert [data-testid="stMarkdownContainer"] {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 0.85rem !important;
    }
    
    /* ==============================
       BOTÕES DE LOGIN/REGISTRO
    ============================== */
    .login-buttons {
        display: flex !important;
        gap: 0.5rem !important;
        margin-top: 1rem !important;
    }
    
    /* ==============================
       SCROLLBAR DA SIDEBAR
    ============================== */
    /* Remove a barra de rolagem visível na sidebar */
    [data-testid="stSidebar"] {
        overflow: hidden !important;
    }

    /* Esconde scrollbars para WebKit (Chrome, Edge, Safari) */
    [data-testid="stSidebar"] ::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* Esconde scrollbars para Firefox */
    [data-testid="stSidebar"] {
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }

    /* Mantém area interna rolável se necessário em elementos específicos (menu) */
    [data-testid="stSidebar"] [data-baseweb="menu"] {
        overflow: auto !important;
        -webkit-overflow-scrolling: touch !important;
        max-height: calc(100vh - 220px) !important; /* evita overflow da user-area */
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar_header():
    """Renderiza o header da sidebar"""
    st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-title">InterBet 365</div>
            <div class="sidebar-subtitle">Apostas em jogos universitários</div>
        </div>
    """, unsafe_allow_html=True)


def render_user_area(username, email):
    """Renderiza a área do usuário no final da sidebar"""
    st.markdown(f"""
        <div class="user-area">
            <p class="user-name">{username}</p>
            <p class="user-email">{email}</p>
    """, unsafe_allow_html=True)