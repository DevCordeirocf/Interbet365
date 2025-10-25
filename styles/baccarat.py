import streamlit as st

def load_baccarat_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }

    /* ==============================
       FUNDO E LAYOUT PRINCIPAL
    ============================== */
    .stApp {
        background: linear-gradient(180deg, hsl(250, 15%, 8%), hsl(250, 15%, 5%));
        min-height: 100vh;
        padding: 2rem 0;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* ==============================
       TÍTULOS E HEADERS
    ============================== */
    h1 {
        color: hsl(0, 0%, 100%) !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        margin-bottom: 0.5rem !important;
        text-align: center !important;
        letter-spacing: -0.02em !important;
    }

    h2 {
        color: hsl(0, 0%, 100%) !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        text-align: center !important;
    }

    h3 {
        color: hsl(0, 0%, 100%) !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-align: center !important;
    }

    h4 {
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        text-align: left !important;
        margin-bottom: 1rem !important;
    }

    /* ==============================
       HEADER COM ÍCONE
    ============================== */
    .icon-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    /* ==============================
       ÁREAS DO JOGADOR E BANCO
    ============================== */
    .player-area h4 {
        margin-bottom: 1rem !important; 
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        text-align: center !important;
        color: #3498db !important; /* Azul Jogador */
    }
    
    .banker-area h4 {
        margin-bottom: 1rem !important; 
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        text-align: center !important;
        color: #e74c3c !important; /* Vermelho Banco */
    }

    /* ==============================
       CONTAINER PARA UMA CARTA
    ============================== */
    .card-container {
        display: flex; 
        justify-content: center;
        align-items: center;
        min-height: 180px; 
    }

    /* ==============================
       SLOT VAZIO (Quando não há carta)
    ============================== */
    .card-slot-empty {
        width: 100px;
        height: 145px;
        border-radius: 8px;
        background-color: rgba(0, 0, 0, 0.2);
        border: 1px dashed rgba(255, 255, 255, 0.15);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* ==============================
       ROTAÇÃO DA TERCEIRA CARTA
    ============================== */
    .third-card-rotated {
        transform: rotate(90deg);
    }

    /* ==============================
       VALORES DE BACCARAT
    ============================== */
    .baccarat-values {
        text-align: center;
        margin-top: 10px; 
        padding: 5px 0;
    }
    
    .value-label {
        font-weight: 700;
        font-size: 1.125rem;
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        color: white;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .player-value .value-label { 
        background: linear-gradient(135deg, #3498db, #2980b9);
    }
    
    .banker-value .value-label { 
        background: linear-gradient(135deg, #e74c3c, #c0392b);
    }

    /* ==============================
       HISTÓRICO (Big Road)
    ============================== */
    .baccarat-grid table { 
        border-collapse: collapse; 
        margin: 10px auto; 
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        overflow: hidden;
    }
    
    .baccarat-grid th, .baccarat-grid td { 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        padding: 2px; 
        text-align: center; 
        min-width: 30px; 
        height: 30px; 
        font-size: 16px; 
    }
    
    .baccarat-grid th {
        background: rgba(255, 255, 255, 0.08);
        color: white;
        font-weight: 700;
    }
    
    .baccarat-grid td { 
        background-color: rgba(255, 255, 255, 0.02);
    }

    /* ==============================
       ESPAÇAMENTO ENTRE CARTAS
    ============================== */
    .player-area div[data-testid="stHorizontalBlock"] > div,
    .banker-area div[data-testid="stHorizontalBlock"] > div {
        padding-left: 0.25rem !important;
        padding-right: 0.25rem !important;
    }

    /* ==============================
       BOTÕES
    ============================== */
    .stButton > button {
        background: linear-gradient(135deg, hsl(11, 100%, 60%), hsl(318, 100%, 28%)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        min-height: 3rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 70, 44, 0.3) !important;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 70, 44, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ==============================
       ALERTAS
    ============================== */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15) !important;
        color: rgb(167, 243, 208) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        color: rgb(254, 202, 202) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    .stWarning {
        background: rgba(245, 158, 11, 0.15) !important;
        color: rgb(253, 230, 138) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        color: rgb(191, 219, 254) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    /* ==============================
       DIVIDER
    ============================== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
        margin: 2rem 0 !important;
    }

    /* ==============================
       REMOVER ELEMENTOS STREAMLIT
    ============================== */
    #MainMenu, footer, .stDeployButton {
        visibility: hidden !important;
        display: none !important;
    }

    /* ==============================
       SCROLLBAR CUSTOMIZADA
    ============================== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(255, 70, 44, 0.5);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 70, 44, 0.7);
    }

    /* ==============================
       RESPONSIVO
    ============================== */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }

        h4 {
            font-size: 1.1rem !important;
        }

        .card-container {
            min-height: 150px;
        }

        .card-slot-empty {
            width: 80px;
            height: 115px;
        }
    }
    </style>
    """, unsafe_allow_html=True)