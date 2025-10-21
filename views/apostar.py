# views/apostar.py

import streamlit as st
from core import match_service, bet_service, user_service
# Não precisamos mais importar 'views/login' aqui

def render():
    st.title("🏆 Apostar")
    # ... (seu código para listar as partidas) ...
    matches = match_service.get_open_matches()
    if not matches:
        st.info("Nenhuma partida agendada no momento."); st.stop()

    for match in matches:
        # ... (seu código para exibir o card da partida) ...
        team_a_name = match.get('team_a', {}).get('name', 'Time A')
        if st.button(f"Apostar em {team_a_name}", key=f"bet_a_{match['id']}"):
            
            # AQUI ESTÁ A MUDANÇA
            if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
                # Se não estiver logado, muda o estado da aplicação
                st.session_state['view'] = 'login'
                st.rerun()
            else:
                # Se estiver logado, continua para o fluxo de aposta
                st.session_state['bet_intent'] = {'match_id': match['id'], 'prediction': 'A'}
                st.rerun()
    
    # ... (Resto do seu código para lidar com 'bet_intent' quando logado) ...
    if 'bet_intent' in st.session_state and 'authenticated' in st.session_state:
        # ... (seu formulário de aposta para usuários logados) ...
        pass