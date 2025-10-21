# views/minhasApostas.py

import streamlit as st
from core import bet_service

def render():
    # Bloco de proteção (embora Wyden365 já verifique, é uma boa prática)
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("🔒 Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    st.title("🎟️ Minhas Apostas")
    
    user_id = st.session_state['user_id']
    all_bets = bet_service.get_bets_by_user(user_id)
    
    if not all_bets:
        st.info("Você ainda não fez nenhuma aposta.")
        st.stop()
        
    # Separa as apostas em abas
    tab_pending, tab_finished = st.tabs(["Apostas Pendentes", "Apostas Finalizadas"])
    
    with tab_pending:
        st.subheader("Aguardando Resultado")
        pending_bets = [bet for bet in all_bets if bet['status'] == 'Pendente']
        if not pending_bets:
            st.write("Nenhuma aposta pendente.")
        
        for bet in pending_bets:
            # Pega os nomes dos times (o JOIN já foi feito no bet_service)
            match_info = bet.get('match', {})
            team_a = match_info.get('team_a', {}).get('name', 'Time A')
            team_b = match_info.get('team_b', {}).get('name', 'Time B')
            
            with st.expander(f"Aposta de R$ {bet['bet_amount']:.2f} em {team_a} vs {team_b}"):
                st.write(f"**Partida:** {team_a} vs {team_b}")
                st.write(f"**Sua Previsão:** {bet['prediction']}")
                st.write(f"**Valor:** R$ {bet['bet_amount']:.2f}")
                st.write(f"**Status:** {bet['status']}")

    with tab_finished:
        st.subheader("Histórico de Apostas")
        finished_bets = [bet for bet in all_bets if bet['status'] != 'Pendente']
        
        if not finished_bets:
            st.write("Nenhuma aposta finalizada.")
            
        # O frontender pode usar st.dataframe para ver a estrutura dos dados
        st.dataframe(finished_bets, use_container_width=True)