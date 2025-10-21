# views/apostar.py

import streamlit as st
from core import match_service
from core import bet_service
from core import user_service 

def render():
    # --- 1. Bloco de Proteção ---
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("🔒 Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    # --- 2. Conteúdo da Página ---
    st.title("🏆 Apostar")
    st.write("Aqui ficarão listadas todas as partidas disponíveis.")
    
    # Exemplo de como você vai carregar os dados no futuro:
    # supabase = database.init_supabase_client()
    # if supabase:
    #     matches = supabase.table('matches').select('*').eq('status', 'Agendado').execute()
    #     if matches.data:
    #         st.dataframe(matches.data)
    #     else:
    #         st.info("Nenhuma partida agendada no momento.")