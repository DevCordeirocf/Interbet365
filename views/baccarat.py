import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh
from core import user_service, game_service
import os

from styles.baccarat import load_baccarat_styles


def render_baccarat_table(player_cards, banker_cards, player_value, banker_value):
    p_cards = player_cards + [None] * (3 - len(player_cards))
    b_cards = banker_cards + [None] * (3 - len(banker_cards))
    image_folder = "assets/cards/"

    with st.container():
        
        col_player, col_banker = st.columns(2) 

        # --- COLUNA DO JOGADOR ---
        with col_player:
            st.markdown('<div class="player-area"><h4>Jogador</h4></div>', unsafe_allow_html=True) 
            
            slot_cols = st.columns(3) 
            
            for i in range(3):
                with slot_cols[i]:
                    card_name = p_cards[i]
                    is_third = (i == 2) 
                    
                    with st.container(): 
                        rotation_class = "third-card-rotated" if is_third else ""
                        st.markdown(f'<div class="card-container {rotation_class} d-flex align-items-center">', unsafe_allow_html=True)
                        
                        if card_name:
                            image_path = os.path.join(image_folder, f"{card_name}.png")
                            if os.path.exists(image_path):
                                st.image(image_path, width=100) 
                            else:
                                st.warning(f"{card_name}.png")
                                print(f"AVISO: Imagem não encontrada '{image_path}'")
                        else:
                             st.markdown('<div class="card-slot-empty"></div>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True) 

            st.markdown(f'<div class="baccarat-values player-value"><span class="value-label">{player_value}</span></div>', unsafe_allow_html=True)

        with col_banker:
            st.markdown('<div class="banker-area"><h4>Banco</h4></div>', unsafe_allow_html=True)
            
            slot_cols = st.columns(3)
            
            for i in range(3):
                 with slot_cols[i]:
                    card_name = b_cards[i]
                    is_third = (i == 2)
                    
                    with st.container():
                        rotation_class = "third-card-rotated" if is_third else ""
                        st.markdown(f'<div class="card-container {rotation_class} d-flex align-items-center">', unsafe_allow_html=True)
                        if card_name:
                            image_path = os.path.join(image_folder, f"{card_name}.png")
                            if os.path.exists(image_path):
                                st.image(image_path, width=100)
                            else:
                                st.warning(f"{card_name}.png")
                        else:
                             st.markdown('<div class="card-slot-empty"></div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="baccarat-values banker-value"><span class="value-label">{banker_value}</span></div>', unsafe_allow_html=True)


def display_history(history, max_cols=12, max_rows=6):
    st.subheader("Histórico")
    history_map = {"Player": "🔵", "Banker": "🔴", "Tie":    "🟢"}
    grid = [['' for _ in range(max_cols)] for _ in range(max_rows)]
    col_idx, row_idx, last_outcome = -1, 0, None
    for outcome in history:
        is_tie = outcome == "Tie"
        if is_tie:
            if col_idx >= 0 and row_idx < max_rows:
                 tie_row = max(0, row_idx -1 if last_outcome else 0) 
                 grid[tie_row][col_idx] += history_map.get(outcome, '')
            continue
        if last_outcome is None or outcome != last_outcome:
             col_idx += 1; row_idx = 0
             if col_idx >= max_cols: break
             last_outcome = outcome
        else:
             row_idx += 1
             if row_idx >= max_rows:
                 col_idx += 1; row_idx = max_rows - 1
                 if col_idx >= max_cols: break
        grid[row_idx][col_idx] = history_map.get(outcome, '')
    html_table = "<div class='baccarat-grid'><table>"
    for r in range(max_rows):
        html_table += "<tr>"
        for c in range(max_cols): html_table += f"<td>{grid[r][c]}</td>"
        html_table += "</tr>"
    html_table += "</table></div>"
    st.markdown(html_table, unsafe_allow_html=True)



def render():
    load_baccarat_styles() 
    
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("Acesso negado. Por favor, faça o login para jogar."); st.stop()
    st_autorefresh(interval=1000, key="game_refresher")
    if 'baccarat_state' not in st.session_state:
        st.session_state.baccarat_state = {"phase": "BETTING", "timer": 15, "history": [], "last_hand": None}
    state = st.session_state.baccarat_state
    user_id = st.session_state['user_id']

    # Título com ícone de ajuda
    if 'show_baccarat_help' not in st.session_state:
        st.session_state['show_baccarat_help'] = False

    col_title, col_help = st.columns([9, 1])
    with col_title:
        st.title("Baccarat ao Vivo")
    with col_help:
        # Botão com ícone de ajuda; ao clicar alterna a exibição do cartão de ajuda
        if st.button("?", key="baccarat_help_btn", help="Ajuda sobre como funcionam as apostas no Baccarat ao vivo"):
            st.session_state['show_baccarat_help'] = not st.session_state['show_baccarat_help']

    # Cartão de ajuda — exibido quando o usuário ativa o botão
    if st.session_state.get('show_baccarat_help'):
        with st.container():
            st.info(
                """
                Como funcionam as apostas no Baccarat ao vivo:

                • Fases do jogo:
                  1) BETTING — período para registrar apostas (ex.: 15s).
                  2) DEALING — cartas são reveladas e regras da terceira carta aplicadas.
                  3) RESULT — mostra o vencedor e pagamentos; depois volta para BETTING.

                • Tipos de aposta e pagamentos:
                  - Jogador (Player): paga 1:1.
                  - Banco (Banker): paga 0.95:1 (comissão simulada aplicada).
                  - Empate (Tie): paga 8:1.

                • Regras importantes:
                  - As mãos começam com duas cartas cada.
                  - A pontuação é o total das cartas mod 10 (por exemplo, 7+8 = 5).
                  - Regras da terceira carta são aplicadas automaticamente durante DEALING.

                • Como apostar aqui:
                  - Insira o valor no campo "Valor da Aposta".
                  - Clique no botão do lado correspondente (Jogador / Banco / Empate).
                  - Se o saldo for insuficiente, a aposta será recusada.

                • Exemplo rápido:
                  Apostando R$5 no Jogador e vencendo, você recebe R$5 de lucro (total R$10).

                Se precisar de mais detalhes sobre regras de terceira carta ou odds, abra a documentação do jogo ou contate o suporte.
                """
            )
    balance = user_service.get_user_balance(user_id)
    balance_placeholder = st.empty()
    if balance is not None: balance_placeholder.metric(label="Meu Saldo", value=f"R$ {balance:.2f}")
    st.divider()


    if state["phase"] == "BETTING":
        st.subheader(f"Faça sua aposta! Tempo restante: {state['timer']}s")
        render_baccarat_table([], [], 0, 0) 
        bet_amount = st.number_input("Valor da Aposta (R$)", min_value=1.00, value=5.00, step=1.00, format="%.2f", key="bet_amount_input")
        col1, col2, col3 = st.columns(3)
        bet_on = None
        if col1.button("Apostar no Jogador (1:1)", use_container_width=True): bet_on = "Player"
        if col2.button("Apostar no Banco (0.95:1)", use_container_width=True): bet_on = "Banker"
        if col3.button("Apostar no Empate (8:1)", use_container_width=True): bet_on = "Tie"
        
        if bet_on:
            if balance is not None and bet_amount > balance: st.error("Saldo insuficiente.")
            else:
                with st.spinner("Aposta registrada..."):
                    result = game_service.play_baccarat_hand(user_id, bet_on, bet_amount)
                    state["last_hand"] = result; state["phase"] = "DEALING"; state["timer"] = 5
                    st.rerun()

        state["timer"] -= 1
        if state["timer"] <= 0:
            st.info("Apostas encerradas!")
            sim_result = game_service.simulate_baccarat_hand()
            state["last_hand"] = {"simulation": sim_result}; state["phase"] = "DEALING"; state["timer"] = 5
            time.sleep(1); st.rerun()
            
        st.divider()
        display_history(state["history"])

    # --- FASE DE DISTRIBUIÇÃO ---
    elif state["phase"] == "DEALING":
        st.subheader("Apostas encerradas! Revelando as cartas...")
        st.progress(state["timer"] / 5)
        sim_result = state["last_hand"]["simulation"]
        render_baccarat_table(sim_result["player_hand"], sim_result["banker_hand"], sim_result["player_value"], sim_result["banker_value"])
        st.divider()
        display_history(state["history"])
        state["timer"] -= 1
        if state["timer"] <= 0:
            state["phase"] = "RESULT"; state["timer"] = 5; state["history"].append(sim_result["outcome"])
            st.rerun()

    # --- FASE DE RESULTADO ---
    elif state["phase"] == "RESULT":
        result_data = state["last_hand"]
        sim_result = result_data["simulation"]
        st.subheader(f"Resultado: {sim_result['outcome']} venceu! Próxima rodada em {state['timer']}s")
        render_baccarat_table(sim_result["player_hand"], sim_result["banker_hand"], sim_result["player_value"], sim_result["banker_value"])
        if "bet_on" in result_data:
            if result_data['payout_amount'] > result_data['bet_amount']: st.success(f"Você apostou em {result_data['bet_on']} e ganhou R$ {result_data['payout_amount']:.2f}!")
            elif result_data['payout_amount'] == 0: st.error(f"Você apostou em {result_data['bet_on']} e perdeu R$ {result_data['bet_amount']:.2f}.")
            else: st.info("A aposta foi devolvida.")
        st.divider()
        display_history(state["history"])
        state["timer"] -= 1
        if state["timer"] <= 0:
            state["phase"] = "BETTING"; state["timer"] = 15; state["last_hand"] = None
            st.rerun()

