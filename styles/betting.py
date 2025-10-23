

import streamlit as st

COLOR_PRIMARY = "#FF462C"
COLOR_SECONDARY = "#88005B"

def load_betting_styles():

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    /* Estilos dos ícones */
    .feature-icon {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.5rem;
    }}
    
    .feature-icon svg {{
        width: 24px;
        height: 24px;
        stroke: {COLOR_PRIMARY};
        transition: transform 0.2s ease;
    }}

    .bet-button-container {{
        position: relative;
        cursor: pointer;
        transition: all 0.2s ease;
    }}

    .bet-button-container:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }}

    .bet-button-container:hover .feature-icon svg {{
        transform: scale(1.1);
    }}

    /* ==============================
       VARIÁVEIS DO TEMA ESCURO
    ============================== */
    :root {{
        --background: 220 20% 8%;
        --foreground: 0 0% 98%;
        --card: 220 18% 12%;
        --primary: 9 100% 59%;
        --secondary: 320 100% 27%;
        --muted: 220 15% 20%;
        --border: 220 15% 18%;
        --radius: 0.75rem;
    }}

    /* ==============================
       LAYOUT GERAL - TEMA ESCURO
    ============================== */
    .main .block-container {{
        padding: 2rem 1rem !important;
        max-width: 1400px !important;
        background-color: hsl(var(--background)) !important;
        font-family: 'Inter', sans-serif !important;
    }}

    .stApp {{
        background-color: hsl(var(--background)) !important;
        color: hsl(var(--foreground)) !important;
    }}

    /* ==============================
       TÍTULOS
    ============================== */
    h1, h2, h3 {{
        font-family: 'Inter', sans-serif !important;
        color: hsl(var(--foreground)) !important;
        font-weight: 700 !important;
    }}

    h1 {{
        background: linear-gradient(135deg, hsl(9 100% 59%), hsl(320 100% 27%)) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
    }}

    /* ==============================
       CARDS DE PARTIDA
    ============================== */
    .match-card {{
        background: linear-gradient(180deg, hsl(220 18% 14%) 0%, hsl(220 18% 10%) 100%) !important;
        border: 1px solid hsl(var(--border)) !important;
        border-radius: var(--radius) !important;
        padding: 2rem !important;
        margin: 1.5rem 0 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    .match-modality {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.5rem !important;
        margin-bottom: 1rem !important;
        color: hsl(var(--primary)) !important;
        font-weight: 600 !important;
    }}
    
    .modality-icon {{
        font-size: 1.25rem !important;
    }}
    
    .modality-name {{
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}

    .match-card:hover {{
        border-color: hsl(var(--primary)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 70, 44, 0.15) !important;
    }}

    .match-header {{
        text-align: center !important;
        margin-bottom: 1.5rem !important;
    }}

    .match-teams {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 1rem !important;
        margin-bottom: 1rem !important;
    }}

    .team-name {{
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: hsl(var(--foreground)) !important;
    }}

    .match-vs {{
        color: hsl(var(--primary)) !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
    }}

    .match-meta {{
        color: hsl(220 10% 60%) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }}

    /* ==============================
       CONTAINER DOS BOTÕES DE APOSTA
    ============================== */
    .bet-button-container {{
        background: hsl(var(--muted)) !important;
        border: 2px solid hsl(var(--border)) !important;
        border-radius: var(--radius) !important;
        padding: 1.5rem 1rem !important;
        text-align: center !important;
        margin-bottom: 0.75rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    .bet-button-container:hover {{
        border-color: hsl(var(--primary)) !important;
        background: hsl(var(--primary) / 0.05) !important;
        transform: translateY(-2px) !important;
    }}

    .odds-label {{
        font-size: 0.85rem !important;
        color: hsl(220 10% 60%) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }}

    .odds-display {{
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: hsl(var(--primary)) !important;
        text-shadow: 0 2px 8px hsl(9 100% 59% / 0.3) !important;
    }}

    /* ==============================
       BOTÕES DE APOSTA - CORRIGIDO
    ============================== */
    .stButton > button {{
        width: 100% !important;
        height: 3rem !important;
        border-radius: calc(var(--radius) - 4px) !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: 2px solid hsl(var(--primary)) !important;
        background: hsl(var(--primary)) !important;
        color: white !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
    }}

    .stButton > button:hover {{
        background: hsl(var(--secondary)) !important;
        border-color: hsl(var(--secondary)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px hsl(9 100% 59% / 0.3) !important;
    }}

    /* Efeito de brilho ao hover - CORRIGIDO */
    .stButton > button::before {{
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
        transition: left 0.5s !important;
        z-index: 1 !important;
    }}

    .stButton > button:hover::before {{
        left: 100% !important;
    }}

    .stButton > button span {{
        position: relative !important;
        z-index: 2 !important;
    }}

    /* ==============================
       FORMULÁRIO DE CONFIRMAÇÃO
    ============================== */
    .bet-confirmation {{
        background: hsl(var(--card)) !important;
        border: 2px solid hsl(var(--primary)) !important;
        border-radius: var(--radius) !important;
        padding: 2rem !important;
        margin: 2rem 0 !important;
        box-shadow: 0 10px 40px hsl(9 100% 59% / 0.15) !important;
        animation: slideDown 0.4s ease !important;
    }}

    @keyframes slideDown {{
        from {{
            opacity: 0;
            transform: translateY(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .confirmation-title {{
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        color: hsl(var(--foreground)) !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
    }}

    .confirmation-info {{
        background: hsl(var(--muted)) !important;
        border-radius: calc(var(--radius) - 4px) !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        border-left: 4px solid hsl(var(--primary)) !important;
    }}

    .info-row {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 0.75rem 0 !important;
        border-bottom: 1px solid hsl(var(--border)) !important;
    }}

    .info-row:last-child {{
        border-bottom: none !important;
    }}

    .info-label {{
        color: hsl(220 10% 60%) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }}

    .info-value {{
        color: hsl(var(--foreground)) !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }}

    .balance-value {{
        color: hsl(142 76% 45%) !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
    }}

    /* ==============================
       CAIXA DE GANHO POTENCIAL
    ============================== */
    .potential-win-box {{
        background: linear-gradient(135deg, hsl(142 76% 15%) 0%, hsl(142 76% 10%) 100%) !important;
        border: 2px solid hsl(142 76% 35%) !important;
        border-radius: var(--radius) !important;
        padding: 1.5rem !important;
        margin: 1.5rem 0 !important;
    }}

    .potential-row {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 0.5rem 0 !important;
    }}

    .potential-label {{
        color: hsl(142 76% 65%) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }}

    .potential-value {{
        font-weight: 800 !important;
        font-size: 1.3rem !important;
    }}

    .potential-value.win {{
        color: hsl(142 76% 55%) !important;
    }}

    .potential-value.profit {{
        color: hsl(142 76% 45%) !important;
    }}

    /* ==============================
       INPUT DE VALOR
    ============================== */
    .stNumberInput label {{
        color: hsl(var(--foreground)) !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }}

    .stNumberInput input {{
        height: 3.5rem !important;
        border: 2px solid hsl(var(--border)) !important;
        border-radius: calc(var(--radius) - 4px) !important;
        padding: 0 1rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        background: hsl(var(--muted)) !important;
        color: hsl(var(--foreground)) !important;
        transition: all 0.3s ease !important;
    }}

    .stNumberInput input:focus {{
        border-color: hsl(var(--primary)) !important;
        box-shadow: 0 0 0 3px hsl(9 100% 59% / 0.1) !important;
        outline: none !important;
        background: hsl(220 18% 14%) !important;
    }}

    /* ==============================
       ALERTAS PERSONALIZADOS
    ============================== */
    .stAlert {{
        border-radius: calc(var(--radius) - 4px) !important;
        border: none !important;
        margin: 1rem 0 !important;
        font-weight: 600 !important;
        background: hsl(var(--muted)) !important;
        color: hsl(var(--foreground)) !important;
    }}

    .stSuccess {{
        border-left: 4px solid hsl(142 76% 45%) !important;
        background: hsl(142 76% 15%) !important;
    }}

    .stError {{
        border-left: 4px solid hsl(0 84% 60%) !important;
        background: hsl(0 84% 15%) !important;
    }}

    .stWarning {{
        border-left: 4px solid hsl(38 92% 50%) !important;
        background: hsl(38 92% 15%) !important;
    }}

    .stInfo {{
        border-left: 4px solid hsl(221 83% 53%) !important;
        background: hsl(221 83% 15%) !important;
    }}

    /* ==============================
       DIVIDER
    ============================== */
    hr {{
        margin: 2rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: hsl(var(--border)) !important;
    }}

    /* ==============================
       CAPTIONS
    ============================== */
    .stCaption {{
        color: hsl(220 10% 60%) !important;
    }}

    /* ==============================
       RESPONSIVIDADE
    ============================== */
    @media (max-width: 768px) {{
        .match-card {{
            padding: 1.5rem !important;
        }}

        .team-name {{
            font-size: 1.2rem !important;
        }}

        .odds-display {{
            font-size: 1.5rem !important;
        }}

        .bet-button-container {{
            padding: 1rem 0.75rem !important;
        }}

        .potential-value {{
            font-size: 1.1rem !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)


def get_modality_icon(modality_name):
    """Retorna o ícone apropriado para cada modalidade."""
    icons = {
        'Futsal': '⚽',
        'Basquete': '🏀',
        'Vôlei': '🏐',
        'Handball': '🤾',
    }
    return icons.get(modality_name, '🎮')  # retorna 🎮 se a modalidade não estiver mapeada

def render_match_card(team_a_name, team_b_name, match_datetime, modality=None, formatted_dt=None):
    """
    Renderiza um card de partida no estilo React com modalidade e data formatada
    """
    modality_icon = get_modality_icon(modality)
    
    st.markdown(f"""
        <div class="match-card">
            <div class="match-header">
                <div class="match-modality">
                    <span class="modality-icon">{modality_icon}</span>
                    <span class="modality-name">{modality or "Esporte"}</span>
                </div>
                <div class="match-teams">
                    <span class="team-name">{team_a_name}</span>
                    <span class="match-vs">VS</span>
                    <span class="team-name">{team_b_name}</span>
                </div>
                <div class="match-meta">
                    {formatted_dt or match_datetime}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_confirmation_box(label, odds, balance):
    """
    Renderiza a caixa de confirmação de aposta
    """
    st.markdown(f"""
        <div class="bet-confirmation">
            <div class="confirmation-title"> Confirmar Aposta</div>
            <div class="confirmation-info">
                <div class="info-row">
                    <span class="info-label">Sua Escolha:</span>
                    <span class="info-value">{label}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Odds:</span>
                    <span class="info-value">{odds:.2f}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Saldo Disponível:</span>
                    <span class="balance-value">R$ {balance:.2f}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)