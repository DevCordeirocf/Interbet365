# views/apostar.py

import streamlit as st
import datetime
from core import match_service, bet_service, user_service

def render():
    st.title("🏆 Apostar")
    st.write("Veja as partidas agendadas e faça sua aposta.")

    # --- 1. Busca as partidas do banco de dados ---
    matches = match_service.get_open_matches()
    
    if not matches:
        st.info("Nenhuma partida agendada no momento. Volte mais tarde!")
        st.stop()
        
    # --- 2. Inicializa o "carrinho de apostas" (bet intent) ---
    # Isso é para lembrar qual aposta o usuário selecionou
    if 'bet_intent' not in st.session_state:
        st.session_state['bet_intent'] = None

    # --- 3. Loop para exibir cada partida ---
    for match in matches:
        # Extrai os nomes dos times. O 'get' evita erros se o JOIN falhar.
        team_a_name = match.get('team_a', {}).get('name', 'Time A')
        team_b_name = match.get('team_b', {}).get('name', 'Time B')
        
        st.divider()
        st.subheader(f"{team_a_name} vs {team_b_name}")
        st.caption(f"Data: {match['match_datetime']}")

        # Layout dos botões de aposta
        col1, col2, col3 = st.columns(3)
        
        with col1:
            label_a = f"Vence: {team_a_name} ({match['odds_a']})"
            if st.button(label_a, key=f"bet_a_{match['id']}", use_container_width=True):
                # Guarda a intenção de aposta na sessão
                st.session_state['bet_intent'] = {
                    'match_id': match['id'],
                    'prediction': 'A',
                    'odds': match['odds_a'],
                    'label': f"Vitória de {team_a_name}"
                }
                st.rerun() # Recarrega a página para mostrar o formulário

        with col2:
            label_draw = f"Empate ({match['odds_draw']})"
            if st.button(label_draw, key=f"bet_draw_{match['id']}", use_container_width=True):
                st.session_state['bet_intent'] = {
                    'match_id': match['id'],
                    'prediction': 'Empate',
                    'odds': match['odds_draw'],
                    'label': "Empate"
                }
                st.rerun()

        with col3:
            label_b = f"Vence: {team_b_name} ({match['odds_b']})"
            if st.button(label_b, key=f"bet_b_{match['id']}", use_container_width=True):
                st.session_state['bet_intent'] = {
                    'match_id': match['id'],
                    'prediction': 'B',
                    'odds': match['odds_b'],
                    'label': f"Vitória de {team_b_name}"
                }
                st.rerun()

    # --- 4. Formulário de Confirmação de Aposta ---
    # Este bloco só aparece APÓS o usuário clicar em uma aposta
    if st.session_state['bet_intent'] is not None:
        
        intent = st.session_state['bet_intent']
        
        # --- 4a. Verifica se o usuário está logado ---
        if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
            st.warning("Você precisa estar logado para apostar.")
            if st.button("Ir para o Login"):
                st.session_state['view'] = 'login' # Muda o estado do Wyden365.py
                st.session_state['bet_intent'] = None # Limpa a intenção
                st.rerun()
            if st.button("Cancelar"):
                st.session_state['bet_intent'] = None
                st.rerun()
        
        # --- 4b. Se estiver logado, mostra o formulário ---
        else:
            user_id = st.session_state['user_id']
            balance = user_service.get_user_balance(user_id)
            
            st.divider()
            with st.form("bet_confirmation_form", clear_on_submit=True):
                st.subheader(f"Confirmar Aposta: {intent['label']}")
                st.write(f"Odds: {intent['odds']}")
                st.write(f"Seu Saldo: R$ {balance:.2f}")
                
                amount = st.number_input("Valor da Aposta (R$)", min_value=1.00, step=0.50, format="%.2f")
                
                submitted = st.form_submit_button("Confirmar Aposta")
                
                if submitted:
                    if amount > balance:
                        st.error("Saldo insuficiente para esta aposta.")
                    else:
                        # Chama a função do backend
                        success = bet_service.create_bet(
                            user_id=user_id,
                            match_id=intent['match_id'],
                            amount=amount,
                            prediction=intent['prediction']
                        )
                        if success:
                            st.success("Aposta realizada com sucesso!")
                        else:
                            st.error("Houve um erro ao registrar sua aposta.")
                        
                        st.session_state['bet_intent'] = None # Limpa a intenção
                        st.rerun() # Recarrega a página

            if st.button("Cancelar Aposta"):
                st.session_state['bet_intent'] = None
                st.rerun()