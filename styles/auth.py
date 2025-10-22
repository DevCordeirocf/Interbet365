import streamlit as st
from .config import COLOR_PRIMARY, COLOR_SECONDARY

def load_auth_styles():
    """
    Carrega os estilos CSS para as páginas de autenticação (Login/Registro)
    """
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    * {{
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }}

    /* ==============================
       FUNDO E LAYOUT
    ============================== */
    .stApp {{
        background: 
            linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.7)),
            url('https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?ixlib=rb-4.1.0&auto=format&fit=crop&q=80&w=2070');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #fff;
        min-height: 100vh;
    }}

    /* Remove scroll desnecessário */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}

    /* ==============================
       EFEITOS DECORATIVOS
    ============================== */
    .stApp::before,
    .stApp::after {{
        content: '';
        position: fixed;
        width: 500px;
        height: 500px;
        filter: blur(120px);
        pointer-events: none;
        z-index: 0;
        opacity: 0.25;
    }}

    .stApp::before {{
        top: -150px;
        left: -150px;
        background: radial-gradient(circle, {COLOR_PRIMARY}, transparent 70%);
    }}

    .stApp::after {{
        bottom: -150px;
        right: -150px;
        background: radial-gradient(circle, {COLOR_SECONDARY}, transparent 70%);
    }}

    /* ==============================
       LOGO / TÍTULOS
    ============================== */
    .brand-title {{
        font-size: 5.5rem;
        font-weight: 900;
        background: {COLOR_PRIMARY};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 25px rgba(255, 70, 44, 0.25);
        letter-spacing: -0.02em;
        text-align: center;
        user-select: none;
    }}

    .brand-subtitle {{
        color: {COLOR_SECONDARY};
        font-size: 1.4rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        text-align: center;
        user-select: none;
    }}

    .form-title {{
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        color: #ffffff;
        text-shadow: 0 2px 15px rgba(0, 0, 0, 0.5);
    }}

    /* ==============================
       TABS DE AUTENTICAÇÃO
    ============================== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem;
        background-color: rgba(255, 255, 255, 0.05);
        padding: 0.8rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 2rem;
        width: 10rem;
        border-radius: 10px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 600;
        font-size: 1rem;
        background-color: transparent;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {COLOR_PRIMARY} !important;
        color: white !important;
        border-color: {COLOR_PRIMARY} !important;
        box-shadow: 0 4px 15px rgba(255, 70, 44, 0.3);
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(255, 70, 44, 0.1);
        border-color: rgba(255, 70, 44, 0.3);
    }}

    /* ==============================
       LABELS E INPUTS
    ============================== */
    .stTextInput > label,
    .stTextArea > label {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
    }}

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        height: 3rem !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        padding: 0 1rem !important;
        font-size: 0.95rem !important;
        background: rgba(255, 255, 255, 0.95) !important;
        transition: all 0.3s ease !important;
        color: #1f2937 !important;
        backdrop-filter: blur(10px);
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {COLOR_PRIMARY} !important;
        outline: none !important;
        background: white !important;
    }}

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {{
        color: #9ca3af !important;
        opacity: 1 !important;
    }}

    /* ==============================
       BOTÕES
    ============================== */
    .stButton > button {{
        height: 3rem !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border: 2px solid {COLOR_PRIMARY} !important;
        background-color: {COLOR_PRIMARY} !important;
        color: white !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        margin-top: 1rem !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 70, 44, 0.3);
    }}

    .stButton > button:hover {{
        background-color: {COLOR_SECONDARY} !important;
        border-color: {COLOR_SECONDARY} !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 70, 44, 0.4) !important;
    }}

    .stButton > button:active {{
        transform: translateY(0) !important;
    }}

    /* Botão de Submit do Form */
    .stForm button[kind="primaryFormSubmit"] {{
        height: 3rem !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        background-color: {COLOR_PRIMARY} !important;
        border: 2px solid {COLOR_PRIMARY} !important;
        color: white !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        margin-top: 1rem !important;
        box-shadow: 0 4px 15px rgba(255, 70, 44, 0.3);
    }}

    .stForm button[kind="primaryFormSubmit"]:hover {{
        background-color: {COLOR_SECONDARY} !important;
        border-color: {COLOR_SECONDARY} !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 70, 44, 0.4) !important;
    }}

    /* ==============================
       ALERTAS E MENSAGENS
    ============================== */
    .stAlert {{
        border-radius: 10px !important;
        border: none !important;
        margin: 1rem 0 !important;
        backdrop-filter: blur(10px);
        background-color: rgba(255, 255, 255, 0.95) !important;
    }}

    .stSuccess {{
        background-color: rgba(34, 197, 94, 0.15) !important;
        border-left: 4px solid #22c55e !important;
    }}

    .stError {{
        background-color: rgba(239, 68, 68, 0.15) !important;
        border-left: 4px solid #ef4444 !important;
    }}

    .stWarning {{
        background-color: rgba(251, 191, 36, 0.15) !important;
        border-left: 4px solid #fbbf24 !important;
    }}

    .stInfo {{
        background-color: rgba(59, 130, 246, 0.15) !important;
        border-left: 4px solid #3b82f6 !important;
    }}

    /* ==============================
       FOOTER
    ============================== */
    .footer {{
        text-align: center;
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.9rem;
        margin-top: 2.5rem;
        font-weight: 500;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }}

    /* ==============================
       REMOVER ELEMENTOS STREAMLIT
    ============================== */
    #MainMenu, footer, header, .stDeployButton {{
        visibility: hidden !important;
        display: none !important;
    }}

    .stApp > header {{
        display: none !important;
    }}

    /* ==============================
       CARD CONTAINER (para centralizar forms)
    ============================== */
    .auth-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }}

    /* ==============================
       RESPONSIVO
    ============================== */
    @media (max-width: 768px) {{
        .brand-title {{
            font-size: 3.5rem;
        }}
        
        .brand-subtitle {{
            font-size: 1rem;
        }}
        
        .form-title {{
            font-size: 1.5rem;
        }}
        
        .stTextInput > div > div > input {{
            height: 3.2rem !important;
        }}
        
        .stButton > button {{
            height: 3.2rem !important;
            font-size: 1rem !important;
        }}

        .auth-card {{
            padding: 1.5rem;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)
