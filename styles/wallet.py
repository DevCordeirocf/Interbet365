import streamlit as st

def load_wallet_styles():
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
            max-width: 1200px;
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
           CARD DE SALDO (DESTAQUE)
        ============================== */
        .balance-card {
            background: linear-gradient(135deg, hsl(11, 100%, 60%), hsl(318, 100%, 28%)) !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 20px !important;
            padding: 2.5rem !important;
            box-shadow: 0 20px 60px rgba(255, 70, 44, 0.4) !important;
            margin: 2rem 0 !important;
            text-align: center !important;
            position: relative !important;
            overflow: hidden !important;
        }

        .balance-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }

        .balance-label {
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            margin-bottom: 0.5rem !important;
        }

        .balance-value {
            color: white !important;
            font-size: 3rem !important;
            font-weight: 900 !important;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
            letter-spacing: -0.02em !important;
        }

        /* Customização do st.metric */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, hsl(11, 100%, 60%), hsl(318, 100%, 28%)) !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 20px !important;
            padding: 2.5rem !important;
            box-shadow: 0 20px 60px rgba(255, 70, 44, 0.4) !important;
            margin: 2rem 0 !important;
            text-align: center !important;
        }

        [data-testid="stMetricLabel"] {
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            justify-content: center !important;
        }

        [data-testid="stMetricValue"] {
            color: white !important;
            font-size: 3rem !important;
            font-weight: 900 !important;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
            justify-content: center !important;
        }

        /* ==============================
           FEATURE CARDS COM ÍCONES
        ============================== */
        .feature-card {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            text-align: center !important;
            transition: all 0.3s ease !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            gap: 1rem !important;
        }

        .feature-card:hover {
            transform: translateY(-4px) !important;
            background: rgba(255, 255, 255, 0.05) !important;
            border-color: hsl(11, 100%, 60%) !important;
        }

        .feature-icon {
            width: 48px !important;
            height: 48px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: linear-gradient(135deg, hsl(11, 100%, 60%), hsl(318, 100%, 28%)) !important;
            border-radius: 12px !important;
            margin-bottom: 0.5rem !important;
        }

        .feature-icon svg {
            width: 24px !important;
            height: 24px !important;
            stroke: white !important;
        }

        .feature-title {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            color: white !important;
            margin: 0.5rem 0 !important;
        }

        .feature-desc {
            font-size: 0.9rem !important;
            color: hsl(220 10% 60%) !important;
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
           INPUTS E FORMS
        ============================== */
        .stTextInput > label,
        .stNumberInput > label {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.5rem !important;
        }

        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            font-size: 1.1rem !important;
            color: #ffffff !important;
            transition: all 0.3s ease !important;
            min-height: 3.5rem !important;
            font-weight: 600 !important;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: hsl(11, 100%, 60%) !important;
            box-shadow: 0 0 0 3px rgba(255, 70, 44, 0.15) !important;
            background: rgba(255, 255, 255, 0.12) !important;
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
            min-height: 3.5rem !important;
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

        /* Botão de link especial */
        .stButton > a {
            background: linear-gradient(135deg, #10b981, #059669) !important;
            color: white !important;
            text-decoration: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            min-height: 3.5rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
        }

        .stButton > a:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4) !important;
        }

        /* ==============================
           ÍCONES NOS HEADERS
        ============================== */
        .icon-header {
            text-align: center;
            margin-bottom: 1rem;
        }

        .section-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
        }

        .section-icon {
            background: rgba(255, 70, 44, 0.15);
            border-radius: 10px;
            padding: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: center;
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
           DIVIDER
        ============================== */
        hr {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
            margin: 2rem 0 !important;
        }

        /* ==============================
           FEATURE CARDS
        ============================== */
        .feature-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }

        .feature-card:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 70, 44, 0.3);
            transform: translateY(-2px);
        }

        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .feature-title {
            color: white;
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.25rem;
        }

        .feature-desc {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.875rem;
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

            .balance-value {
                font-size: 2rem !important;
            }

            [data-testid="stMetricValue"] {
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