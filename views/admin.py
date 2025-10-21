# views/admin.py

import streamlit as st
from core import match_service

def render():
    # --- 1. Bloco de Proteção DUPLA ---
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("🔒 Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    if st.session_state['role'] != 'admin':
        st.error("🔒 Acesso negado. Esta área é restrita para administradores.")
        st.stop()
        
    # --- 2. Conteúdo da Página ---
    st.title("⚙️ Painel de Administração")
    st.write("Bem-vindo, Administrador!")

    tab_matches, tab_teams, tab_modalities = st.tabs([
        "Gerenciar Partidas", 
        "Gerenciar Times", 
        "Gerenciar Modalidades"
    ])

    with tab_matches:
        st.subheader("Criar Nova Partida")
        # O formulário para criar partidas ficará aqui
    
    with tab_teams:
        st.subheader("Adicionar Novo Time")
        # O formulário para criar times ficará aqui

    with tab_modalities:
        st.subheader("Adicionar Nova Modalidade")
        # O formulário para criar modalidades ficará aqui