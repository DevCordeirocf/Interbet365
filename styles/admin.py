import streamlit as st

def load_admin_styles():
    """Carrega estilos específicos para a página de administração com design moderno"""
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
            margin-bottom: 1rem !important;
        }

        h3 {
            color: hsl(0, 0%, 100%) !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }

        .stSubheader {
            color: hsl(0, 0%, 70%) !important;
            text-align: center !important;
            font-size: 1.125rem !important;
            margin-bottom: 2rem !important;
        }

        /* ==============================
           GLASS CARD EFFECT
        ============================== */
        .form-card {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px !important;
            padding: 2rem !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
            margin-bottom: 2rem !important;
        }

        /* ==============================
           TABS ESTILIZADAS
        ============================== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            padding: 0.5rem;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .stTabs [data-baseweb="tab"] {
            height: 3rem;
            border-radius: 8px;
            color: rgba(255, 255, 255, 0.7);
            font-weight: 600;
            font-size: 1rem;
            background-color: transparent;
            border: none;
            transition: all 0.3s ease;
            padding: 0 1.5rem;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, hsl(11, 100%, 60%), hsl(318, 100%, 28%)) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(255, 70, 44, 0.4) !important;
            transform: translateY(-2px);
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(255, 70, 44, 0.15);
            color: rgba(255, 255, 255, 0.9);
        }

        /* ==============================
           INPUTS E FORMS
        ============================== */
        .stTextInput > label,
        .stSelectbox > label,
        .stNumberInput > label,
        .stDateInput > label,
        .stTimeInput > label,
        .stRadio > label {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.5rem !important;
        }

        .stTextInput > div > div > input,
        .stSelectbox > div > div > div,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input,
        .stTimeInput > div > div > input {
            background: rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            font-size: 1rem !important;
            color: #ffffff !important;
            transition: all 0.3s ease !important;
            min-height: 3rem !important;
        }

        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > div:focus-within,
        .stNumberInput > div > div > input:focus,
        .stDateInput > div > div > input:focus,
        .stTimeInput > div > div > input:focus {
            box-shadow: 0 0 0 3px rgba(255, 70, 44, 0.15) !important;
            background: rgba(255, 255, 255, 0.12) !important;
        }

        /* Radio buttons */
        .stRadio > div {
            flex-direction: row !important;
            gap: 2rem !important;
        }

        .stRadio > div > label {
            background: rgba(255, 255, 255, 0.05) !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
        }

        .stRadio > div > label:hover {
            background: rgba(255, 255, 255, 0.1) !important;
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
           DATAFRAMES E TABELAS
        ============================== */
        .stDataFrame {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            overflow: hidden !important;
        }

        .stDataFrame [data-testid="stDataFrameResizable"] {
            border: none !important;
        }

        .stDataFrame table {
            color: white !important;
        }

        .stDataFrame thead tr th {
            background: rgba(255, 255, 255, 0.08) !important;
            color: white !important;
            font-weight: 700 !important;
            border: none !important;
            padding: 1rem !important;
        }

        .stDataFrame tbody tr {
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            transition: background 0.2s ease !important;
        }

        .stDataFrame tbody tr:hover {
            background: rgba(255, 255, 255, 0.05) !important;
        }

        .stDataFrame tbody tr td {
            border: none !important;
            padding: 1rem !important;
            color: rgba(255, 255, 255, 0.9) !important;
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
           ALERTAS E MENSAGENS
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
           ÍCONES E BADGES
        ============================== */
        .icon-header {
            text-align: center;
            margin-bottom: 1rem;
        }

        .badge-status {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .badge-open {
            background: rgba(255, 70, 44, 0.2);
            color: hsl(11, 100%, 60%);
        }

        .badge-closed {
            background: rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.6);
        }

        /* ==============================
           REMOVER ELEMENTOS STREAMLIT
        ============================== */
        #MainMenu, footer, header, .stDeployButton {
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

            .form-card {
                padding: 1.5rem !important;
            }

            .stTabs [data-baseweb="tab"] {
                font-size: 0.875rem;
                padding: 0 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)