"""
Estilos para a página do Baccarat - TEMA ESCURO (Layout Cassino com Rotação)
"""

import streamlit as st

def load_baccarat_styles():
    """
    Carrega os estilos CSS específicos para a página do Baccarat.
    """
    st.markdown("""
    <style>
        /* --- Áreas do Jogador e Banco --- */
        .player-area h4 {
             margin-bottom: 10px; 
             font-weight: bold;
             font-size: 1.3rem;
             text-align: center;
             color: #3498db; /* Azul Jogador */
        }
        
        .banker-area h4 {
             margin-bottom: 10px; 
             font-weight: bold;
             font-size: 1.3rem;
             text-align: center;
             color: #e74c3c; /* Vermelho Banco */
        }

        /* --- Container para UMA carta --- */
        .card-container {
            display: flex; 
            justify-content: center;
            align-items: center;
            min-height: 180px; 
        }

        /* --- Slot VAZIO (Quando não há carta) --- */
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

         /* --- Classe para rotacionar a TERCEIRA CARTA --- */
        .third-card-rotated {
            transform: rotate(90deg);
        }

        /* --- Valores de Baccarat --- */
        .baccarat-values {
            text-align: center;
            margin-top: 10px; 
            padding: 5px 0;
        }
        .value-label {
            font-weight: bold;
            font-size: 18px;
            padding: 6px 18px;
            border-radius: 5px;
            color: white;
            display: inline-block;
        }
        .player-value .value-label { background-color: #3498db; }
        .banker-value .value-label { background-color: #e74c3c; }

        /* --- Histórico (Big Road - sem mudanças) --- */
        .baccarat-grid table { border-collapse: collapse; margin: 10px auto; }
        .baccarat-grid th, .baccarat-grid td { border: 1px solid #555; padding: 2px; text-align: center; min-width: 30px; height: 30px; font-size: 16px; }
        .baccarat-grid td { background-color: #333; }

        /* --- CORREÇÃO: Diminui o espaço entre as colunas das cartas --- */
        /* Streamlit gera divs com classes como esta dentro de st.columns */
        /* O seletor [data-testid="stVerticalBlock"]>div pode ser necessário se a classe mudar */
        .player-area div[data-testid="stHorizontalBlock"] > div,
        .banker-area div[data-testid="stHorizontalBlock"] > div {
            padding-left: 0.25rem !important;  /* Diminui o padding esquerdo */
            padding-right: 0.25rem !important; /* Diminui o padding direito */
        }
        /* ----------------------------------------------------------------- */

    </style>
    """, unsafe_allow_html=True)

