# views/minhas_apostas.py

import streamlit as st
from core import bet_service
def render():
    # --- 1. Bloco de Proteção ---
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("🔒 Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    # --- 2. Conteúdo da Página ---
    st.title("🎟️ Minhas Apostas")
    st.write("Aqui ficará o histórico de todas as suas apostas (pendentes, ganhas e perdidas).")
    
    # user_id = st.session_state['user_id']
    # supabase = database.init_supabase_client()
    # if supabase:
    #     bets = supabase.table('bets').select('*').eq('user_id', user_id).execute()
    #     if bets.data:
    #         st.dataframe(bets.data)
    #     else:
    #         st.info("Você ainda não fez nenhuma aposta.")