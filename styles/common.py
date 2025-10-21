"""
styles/common.py
Estilos para componentes comuns (marca, rodapé, etc)
"""

import streamlit as st
from .config import COLOR_PRIMARY, COLOR_SECONDARY

def render_brand(subtitle=None):

    subtitle_html = f"<p class='brand-subtitle'>Aposte com inteligência</p>" if subtitle else ""
    
    st.markdown(f"""
        <div style="margin: 1rem 0;">
            <h1 class='brand-title'>Wyden 365</h1>
            {subtitle_html}
        </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Renderiza o rodapé"""
    st.markdown("""
        <p class='footer'>© 2025 Wyden 365. Jogue com responsabilidade. +18</p>
    """, unsafe_allow_html=True)

def load_common_styles():
    """Carrega os estilos comuns usados em todas as páginas"""
    st.markdown(f"""
    <style>
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

    /* ==============================
       RODAPÉ
    ============================== */
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem;
        background: rgba(0,0,0,0.8);
        backdrop-filter: blur(10px);
        text-align: center;
        font-size: 0.9rem;
        color: rgba(255,255,255,0.7);
    }}
    </style>
    """, unsafe_allow_html=True)