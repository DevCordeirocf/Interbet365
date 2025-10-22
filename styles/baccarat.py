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
        .player-area h4, .banker-area h4 {
             margin-bottom: 10px; /* Espaço abaixo do título */
             font-weight: bold;
             font-size: 1.3rem;
             text-align: center;
        }

        /* --- Container para UMA carta (st.image já cuida do tamanho) --- */
        .card-container {
            display: flex; /* Para centralizar o slot */
            justify-content: center;
            align-items: center;
            min-height: 180px; /* Altura para carta normal ou rotacionada */
            padding: 5px; /* Pequeno espaçamento interno */
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

         /* --- Classe para rotacionar a TERCEIRA CARTA (container ou imagem) --- */
        .third-card-rotated {
            transform: rotate(90deg);
            /* Ajuste fino da posição se necessário após rotação */
            /* margin-top: 20px; */
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
    </style>
    """, unsafe_allow_html=True)

