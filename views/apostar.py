# views/apostar.py
import streamlit as st
import datetime
from core import match_service, bet_service, user_service
from styles.betting import load_betting_styles, render_match_card, render_confirmation_box

def render():
    load_betting_styles()
    
    # Header
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1>Wyden 365 - Apostas Esportivas</h1>
            <p style="color: hsl(220 10% 60%); font-size: 1.1rem;">
                Clique em qualquer opção de aposta para começar!
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Busca as partidas
    matches = match_service.get_open_matches()
    
    if not matches:
        st.info("Nenhuma partida agendada no momento. Volte mais tarde!")
        st.stop()
        
    # Inicializa o "carrinho de apostas"
    if 'bet_intent' not in st.session_state:
        st.session_state['bet_intent'] = None

    # Loop para exibir cada partida
    st.subheader("Partidas Disponíveis")
    
    for match in matches:
        team_a_name = match.get('team_a', {}).get('name', 'Time A')
        team_b_name = match.get('team_b', {}).get('name', 'Time B')
        
        # Renderiza o card da partida
        render_match_card(team_a_name, team_b_name, match['match_datetime'])

        # Layout dos cards clicáveis de aposta
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Card clicável para vitória do time A
            if st.session_state.get('bet_intent') and st.session_state['bet_intent'].get('match_id') == match['id'] and st.session_state['bet_intent'].get('prediction') == 'A':
                # Já está selecionado - mostra como ativo
                st.markdown(f"""
                    <div class="bet-button-container" style="border-color: hsl(9 100% 59%) !important; background: hsl(9 100% 59% / 0.1) !important;">
                        <div class="feature-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                                <polyline points="9 22 9 12 15 12 15 22"></polyline>
                            </svg>
                        </div>
                        <div class="odds-label">Casa</div>
                        <div class="odds-display">{match['odds_a']:.2f}</div>
                        <div style="color: hsl(9 100% 59%); font-weight: 600; font-size: 0.9rem; margin-top: 0.5rem;">✓ Selecionado</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Card clicável normal
                st.markdown(f"""
                    <div class="bet-button-container">
                        <div class="feature-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                                <polyline points="9 22 9 12 15 12 15 22"></polyline>
                            </svg>
                        </div>
                        <div class="odds-label">Casa</div>
                        <div class="odds-display">{match['odds_a']:.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("", key=f"bet_a_{match['id']}", use_container_width=True,
                           help=f"Apostar na vitória de {team_a_name}"):
                    st.session_state['bet_intent'] = {
                        'match_id': match['id'],
                        'prediction': 'A',
                        'odds': match['odds_a'],
                        'label': f"Vitória de {team_a_name}",
                        'team_a': team_a_name,
                        'team_b': team_b_name,
                        'match_datetime': match['match_datetime']
                    }
                    st.rerun()

        with col2:
            # Card clicável para empate
            if st.session_state.get('bet_intent') and st.session_state['bet_intent'].get('match_id') == match['id'] and st.session_state['bet_intent'].get('prediction') == 'Empate':
                st.markdown(f"""
                    <div class="bet-button-container" style="border-color: hsl(9 100% 59%) !important; background: hsl(9 100% 59% / 0.1) !important;">
                        <div class="feature-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="8" y1="12" x2="16" y2="12"></line>
                            </svg>
                        </div>
                        <div class="odds-label">Empate</div>
                        <div class="odds-display">{match['odds_draw']:.2f}</div>
                        <div style="color: hsl(9 100% 59%); font-weight: 600; font-size: 0.9rem; margin-top: 0.5rem;">✓ Selecionado</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="bet-button-container">
                        <div class="feature-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="8" y1="12" x2="16" y2="12"></line>
                            </svg>
                        </div>
                        <div class="odds-label">Empate</div>
                        <div class="odds-display">{match['odds_draw']:.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("", key=f"bet_draw_{match['id']}", use_container_width=True,
                           help="Apostar no empate"):
                    st.session_state['bet_intent'] = {
                        'match_id': match['id'],
                        'prediction': 'Empate',
                        'odds': match['odds_draw'],
                        'label': "Empate",
                        'team_a': team_a_name,
                        'team_b': team_b_name,
                        'match_datetime': match['match_datetime']
                    }
                    st.rerun()

        with col3:
            # Card clicável para vitória do time B
            if st.session_state.get('bet_intent') and st.session_state['bet_intent'].get('match_id') == match['id'] and st.session_state['bet_intent'].get('prediction') == 'B':
                st.markdown(f"""
                    <div class="bet-button-container" style="border-color: hsl(9 100% 59%) !important; background: hsl(9 100% 59% / 0.1) !important;">
                        <div class="feature-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path d="M22 12H18L15 21H13L14 12H10L8 15H6L7 12H3L2 10H7L6 7H8L10 10H14L13 1H15L18 10H22L23 12L22 12Z"></path>
                            </svg>
                        </div>
                        <div class="odds-label">Fora</div>
                        <div class="odds-display">{match['odds_b']:.2f}</div>
                        <div style="color: hsl(9 100% 59%); font-weight: 600; font-size: 0.9rem; margin-top: 0.5rem;">✓ Selecionado</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="bet-button-container">
                        <div class="feature-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path d="M22 12H18L15 21H13L14 12H10L8 15H6L7 12H3L2 10H7L6 7H8L10 10H14L13 1H15L18 10H22L23 12L22 12Z"></path>
                            </svg>
                        </div>
                        <div class="odds-label">Fora</div>
                        <div class="odds-display">{match['odds_b']:.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("", key=f"bet_b_{match['id']}", use_container_width=True,
                           help=f"Apostar na vitória de {team_b_name}"):
                    st.session_state['bet_intent'] = {
                        'match_id': match['id'],
                        'prediction': 'B',
                        'odds': match['odds_b'],
                        'label': f"Vitória de {team_b_name}",
                        'team_a': team_a_name,
                        'team_b': team_b_name,
                        'match_datetime': match['match_datetime']
                    }
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

    # --- FORMULÁRIO DE APOSTA (aparece abaixo da partida selecionada) ---
    if st.session_state['bet_intent'] is not None:
        
        intent = st.session_state['bet_intent']
        
        # Verifica se o usuário está logado
        if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
            st.warning(" Autenticação Necessária")
            st.info("Você precisa estar logado para fazer apostas.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Cancelar", use_container_width=True):
                    st.session_state['bet_intent'] = None
                    st.rerun()
            
            with col2:
                if st.button("Fazer Login", type="primary", use_container_width=True):
                    st.session_state['view'] = 'login'
                    st.session_state['bet_intent'] = None
                    st.rerun()
        
        # Usuário logado - mostra formulário de aposta
        else:
            user_id = st.session_state['user_id']
            balance = user_service.get_user_balance(user_id)
            
            # Formata o saldo em Real brasileiro
            balance_brl = f"R$ {balance:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            
            # Mostra informações da aposta selecionada
            st.markdown("---")
            st.subheader("💰 Confirmar Aposta")
            
            # Informações da partida
            col1, col2, col3 = st.columns([2,1,2])
            with col1:
                st.markdown(f"**{intent['team_a']}**")
            with col2:
                st.markdown("**VS**")
            with col3:
                st.markdown(f"**{intent['team_b']}**")
            
            st.markdown(f"*{intent['match_datetime']}*")
            
            # Card de confirmação
            render_confirmation_box(intent['label'], intent['odds'], balance)
            
            # Input do valor
            st.subheader("💎 Valor da Aposta")
            
            if 'bet_amount' not in st.session_state:
                st.session_state['bet_amount'] = 10.0
            
            amount = st.number_input(
                "Valor (R$)", 
                min_value=1.00,
                max_value=float(balance) if balance > 0 else 1.00,
                value=st.session_state['bet_amount'],
                step=5.00, 
                format="%.2f",
                key="bet_amount_input"
            )
            
            st.session_state['bet_amount'] = amount
            
            # Calcula e mostra ganho potencial
            if amount > 0:
                potential_win = amount * intent['odds']
                profit = potential_win - amount
                
                # Formata em Real brasileiro
                potential_win_brl = f"R$ {potential_win:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                profit_brl = f"R$ {profit:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                
                st.markdown(f"""
                    <div class="potential-win-box">
                        <div class="potential-row">
                            <span class="potential-label">💰 Retorno Potencial:</span>
                            <span class="potential-value win">{potential_win_brl}</span>
                        </div>
                        <div class="potential-row">
                            <span class="potential-label">💎 Lucro Líquido:</span>
                            <span class="potential-value profit">{profit_brl}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Botões de ação
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if st.button("❌ Cancelar", use_container_width=True, key="cancel_bet"):
                    st.session_state['bet_intent'] = None
                    st.session_state['bet_amount'] = 10.0
                    st.rerun()
            
            with col2:
                if st.button("✅ Confirmar Aposta", type="primary", use_container_width=True, key="confirm_bet"):
                    if amount > balance:
                        st.error("💸 Saldo insuficiente para esta aposta.")
                    elif amount <= 0:
                        st.error("❌ O valor deve ser maior que zero.")
                    else:
                        success = bet_service.create_bet(
                            user_id=user_id,
                            match_id=intent['match_id'],
                            amount=amount,
                            prediction=intent['prediction']
                        )
                        
                        if success:
                            st.success("🎉 Aposta realizada com sucesso!")
                            st.balloons()
                            # Atualiza o saldo na sessão
                            st.session_state.user_balance = user_service.get_user_balance(user_id)
                        else:
                            st.error("❌ Erro ao registrar aposta. Tente novamente.")
                        
                        st.session_state['bet_intent'] = None
                        st.session_state['bet_amount'] = 10.0
                        st.rerun()