import streamlit as st
import datetime
from core import match_service, bet_service, user_service
from styles.betting import load_betting_styles, render_match_card, render_confirmation_box

def render():
    load_betting_styles()
    
    # Header com estilo novo
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1>Wyden 365 - Apostas Esportivas</h1>
            <p style="color: hsl(220 10% 60%); font-size: 1.1rem;">
                Aposte nos seus times favoritos para vencedor do intercursos!
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- 1. Busca as partidas do banco de dados ---
    matches = match_service.get_open_matches()
    
    if not matches:
        st.info("Nenhuma partida agendada no momento. Volte mais tarde!")
        st.stop()
        
    # --- 2. Inicializa o "carrinho de apostas" (bet intent) ---
    if 'bet_intent' not in st.session_state:
        st.session_state['bet_intent'] = None

    # --- 3. Loop para exibir cada partida ---
    st.subheader(" Partidas Disponíveis")
    
    for match in matches:
        # Extrai os nomes dos times
        team_a_name = match.get('team_a', {}).get('name', 'Time A')
        team_b_name = match.get('team_b', {}).get('name', 'Time B')
        
        # Usa a nova função render_match_card
        render_match_card(team_a_name, team_b_name, match['match_datetime'])

        # Layout dos botões de aposta
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Renderiza o botão com HTML customizado para controle total
            st.markdown(f"""
                <div class="bet-button-container">
                    <div class="odds-label"> Casa</div>
                    <div class="odds-display">{match['odds_a']:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Apostar", key=f"bet_a_{match['id']}", use_container_width=True):
                st.session_state['bet_intent'] = {
                    'match_id': match['id'],
                    'prediction': 'A',
                    'odds': match['odds_a'],
                    'label': f"Vitória de {team_a_name}",
                    'team_a': team_a_name,
                    'team_b': team_b_name
                }
                st.rerun()

        with col2:
            st.markdown(f"""
                <div class="bet-button-container">
                    <div class="odds-label"> Empate</div>
                    <div class="odds-display">{match['odds_draw']:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Apostar", key=f"bet_draw_{match['id']}", use_container_width=True):
                st.session_state['bet_intent'] = {
                    'match_id': match['id'],
                    'prediction': 'Empate',
                    'odds': match['odds_draw'],
                    'label': "Empate",
                    'team_a': team_a_name,
                    'team_b': team_b_name
                }
                st.rerun()

        with col3:
            st.markdown(f"""
                <div class="bet-button-container">
                    <div class="odds-label"> Fora</div>
                    <div class="odds-display">{match['odds_b']:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Apostar", key=f"bet_b_{match['id']}", use_container_width=True):
                st.session_state['bet_intent'] = {
                    'match_id': match['id'],
                    'prediction': 'B',
                    'odds': match['odds_b'],
                    'label': f"Vitória de {team_b_name}",
                    'team_a': team_a_name,
                    'team_b': team_b_name
                }
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

    # --- 4. Formulário de Confirmação de Aposta ---
    if st.session_state['bet_intent'] is not None:
        
        intent = st.session_state['bet_intent']
        
        # --- 4a. Verifica se o usuário está logado ---
        if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
            st.warning(" Autenticação Necessária")
            st.info("Você precisa estar logado para fazer apostas.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(" Cancelar", use_container_width=True):
                    st.session_state['bet_intent'] = None
                    st.rerun()
            
            with col2:
                if st.button(" Fazer Login", type="primary", use_container_width=True):
                    st.session_state['view'] = 'login'
                    st.session_state['bet_intent'] = None
                    st.rerun()
        
        # --- 4b. Se estiver logado, mostra o formulário ---
        else:
            user_id = st.session_state['user_id']
            balance = user_service.get_user_balance(user_id)
            
            # Usa a nova função render_confirmation_box
            render_confirmation_box(intent['label'], intent['odds'], balance)
            
            # Inicializa o valor da aposta no session_state se não existir
            if 'bet_amount' not in st.session_state:
                st.session_state['bet_amount'] = 1.0
            
            st.subheader(" Valor da Aposta")
            
            # Input com callback para atualização em tempo real
            amount = st.number_input(
                "Valor (R$)", 
                min_value=1.00,
                max_value=float(balance) if balance > 0 else 1.00,
                value=st.session_state['bet_amount'],
                step=0.50, 
                format="%.2f",
                key="bet_amount_input",
                label_visibility="collapsed"
            )
            
            # Atualiza o session_state
            st.session_state['bet_amount'] = amount
            
            # Calcula e mostra ganho potencial em tempo real
            if amount > 0:
                potential_win = amount * intent['odds']
                profit = potential_win - amount
                
                st.markdown(f"""
                    <div class="potential-win-box">
                        <div class="potential-row">
                            <span class="potential-label"> Retorno Potencial:</span>
                            <span class="potential-value win">R$ {potential_win:.2f}</span>
                        </div>
                        <div class="potential-row">
                            <span class="potential-label"> Lucro Líquido:</span>
                            <span class="potential-value profit">R$ {profit:.2f}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Botões de ação
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if st.button(" Cancelar", use_container_width=True, key="cancel_bet"):
                    st.session_state['bet_intent'] = None
                    st.session_state['bet_amount'] = 1.0
                    st.rerun()
            
            with col2:
                if st.button(" Confirmar Aposta", type="primary", use_container_width=True, key="confirm_bet"):
                    if amount > balance:
                        st.error(" Saldo insuficiente para esta aposta.")
                    elif amount <= 0:
                        st.error(" O valor deve ser maior que zero.")
                    else:
                        success = bet_service.create_bet(
                            user_id=user_id,
                            match_id=intent['match_id'],
                            amount=amount,
                            prediction=intent['prediction']
                        )
                        
                        if success:
                            st.success(" Aposta realizada com sucesso!")
                            st.balloons()
                            # Atualiza o saldo na sessão
                            st.session_state.user_balance = user_service.get_user_balance(user_id)
                        else:
                            st.error(" Erro ao registrar aposta. Tente novamente.")
                        
                        st.session_state['bet_intent'] = None
                        st.session_state['bet_amount'] = 1.0
                        st.rerun()