import streamlit as st

def load_mybets_styles():
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
        }

        h3 {
            color: hsl(0, 0%, 100%) !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }

        /* ==============================
           HEADER COM ÍCONE
        ============================== */
        .icon-header {
            text-align: center;
            margin-bottom: 1.5rem;
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
            margin: 2rem 0;
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
           EXPANDER CUSTOMIZADO
        ============================== */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            padding: 1rem 1.5rem !important;
        }

        .streamlit-expanderHeader:hover {
            background: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(255, 70, 44, 0.3) !important;
            transform: translateX(4px) !important;
        }

        .streamlit-expanderContent {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-top: none !important;
            border-radius: 0 0 12px 12px !important;
            padding: 1.5rem !important;
            color: rgba(255, 255, 255, 0.9) !important;
        }

        /* Textos dentro do expander */
        .streamlit-expanderContent p,
        .streamlit-expanderContent strong {
            color: rgba(255, 255, 255, 0.9) !important;
        }

        /* ==============================
           DATAFRAME CUSTOMIZADO
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
            text-transform: uppercase !important;
            font-size: 0.75rem !important;
            letter-spacing: 0.05em !important;
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
           EMPTY STATE
        ============================== */
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            border: 1px dashed rgba(255, 255, 255, 0.1);
            margin: 2rem 0;
        }

        .empty-state-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }

        .empty-state-title {
            color: white;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .empty-state-desc {
            color: rgba(255, 255, 255, 0.6);
            font-size: 1rem;
        }

        /* ==============================
           TEXTO GENÉRICO
        ============================== */
        p, span, div {
            color: rgba(255, 255, 255, 0.9);
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

            .streamlit-expanderHeader {
                font-size: 0.9rem !important;
                padding: 0.75rem 1rem !important;
            }

            .stTabs [data-baseweb="tab"] {
                font-size: 0.875rem;
                padding: 0 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)