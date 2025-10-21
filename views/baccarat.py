import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh
from core import user_service, game_service
import os

# --- Funções de Interface ---

def display_hand(title, hand, value):
    """
    Função para exibir uma mão de cartas usando as imagens da pasta assets/cards/.
    """
    
    # --- MUDANÇA PRINCIPAL AQUI ---
    # Caminho base para a pasta de imagens, a partir da raiz do projeto.
    image_folder = "assets/cards/"

    st.metric(label=title, value=value)
    
    # Cria colunas para exibir as cartas lado a lado.
    card_cols = st.columns(len(hand) if hand else 1)
    
    for i, card_name in enumerate(hand): # ex: card_name vindo do backend é "AC"
        
        # Constrói o nome completo do arquivo. Ex: "AC" -> "assets/cards/AC.png"
        # IMPORTANTE: Se a sua extensão for diferente de .png, altere aqui.
        image_path = os.path.join(image_folder, f"{card_name}.png")
        
        # Verifica se o arquivo de imagem realmente existe antes de tentar exibi-lo.
        if os.path.exists(image_path):
            card_cols[i].image(image_path, width=100) # Ajuste a largura (width) conforme o design.
        else:
            # Mostra um aviso na tela e no console se a imagem não for encontrada.
            card_cols[i].warning(f"⚠️ {card_name}.png")
            print(f"AVISO: Imagem não encontrada no caminho '{image_path}'")

def display_history(history):
    """Exibe o histórico de resultados (a 'Big Road')."""
    st.subheader("Histórico de Resultados")
    history_map = {"Player": "🔵 P", "Banker": "🔴 B", "Tie": "🟢 T"}
    display_text = " | ".join([history_map.get(r, r) for r in history[-20:]])
    st.markdown(f"<p style='font-size: 20px; word-break: break-all;'>{display_text}</p>", unsafe_allow_html=True)

# --- Lógica Principal da View ---

def render():
    # --- 1. Bloco de Proteção ---
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("🔒 Acesso negado. Por favor, faça o login para jogar."); st.stop()

    # --- 2. O Game Loop ---
    st_autorefresh(interval=1000, key="game_refresher")

    # --- 3. Inicialização do Estado do Jogo ---
    if 'baccarat_state' not in st.session_state:
        st.session_state.baccarat_state = {
            "phase": "BETTING", "timer": 15, "history": [], "last_hand": None
        }
    state = st.session_state.baccarat_state
    user_id = st.session_state['user_id']

    # --- 4. Exibição do Header ---
    st.title("🎲 Baccarat ao Vivo")
    balance = user_service.get_user_balance(user_id)
    balance_placeholder = st.empty()
    if balance is not None:
        balance_placeholder.metric(label="Meu Saldo", value=f"R$ {balance:.2f}")
    display_history(state["history"])
    st.divider()

    # --- 5. Lógica das Fases do Jogo ---

    # --- FASE DE APOSTAS ---
    if state["phase"] == "BETTING":
        st.subheader(f"Faça sua aposta! Tempo restante: {state['timer']}s")
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
                    state["last_hand"] = result
                    state["phase"] = "DEALING"; state["timer"] = 5
                    st.rerun()

        state["timer"] -= 1
        if state["timer"] <= 0:
            st.info("Apostas encerradas!")
            sim_result = game_service.simulate_baccarat_hand()
            state["last_hand"] = {"simulation": sim_result}
            state["phase"] = "DEALING"; state["timer"] = 5
            time.sleep(1); st.rerun()

    # --- FASE DE DISTRIBUIÇÃO ---
    elif state["phase"] == "DEALING":
        st.subheader("Apostas encerradas! Revelando as cartas...")
        st.progress(state["timer"] / 5)
        sim_result = state["last_hand"]["simulation"]
        col1, col2 = st.columns(2)
        with col1: display_hand("Jogador", sim_result["player_hand"], sim_result["player_value"])
        with col2: display_hand("Banco", sim_result["banker_hand"], sim_result["banker_value"])

        state["timer"] -= 1
        if state["timer"] <= 0:
            state["phase"] = "RESULT"; state["timer"] = 5
            state["history"].append(sim_result["outcome"])
            st.rerun()

    # --- FASE DE RESULTADO ---
    elif state["phase"] == "RESULT":
        result_data = state["last_hand"]
        sim_result = result_data["simulation"]
        st.subheader(f"Resultado: {sim_result['outcome']} venceu! Próxima rodada em {state['timer']}s")
        
        if "bet_on" in result_data:
            if result_data['payout_amount'] > result_data['bet_amount']:
                st.success(f"Você apostou em {result_data['bet_on']} e ganhou R$ {result_data['payout_amount']:.2f}!")
            elif result_data['payout_amount'] == 0:
                st.error(f"Você apostou em {result_data['bet_on']} e perdeu R$ {result_data['bet_amount']:.2f}.")
            else: st.info("A aposta foi devolvida.")
        
        col1, col2 = st.columns(2)
        with col1: display_hand("Jogador", sim_result["player_hand"], sim_result["player_value"])
        with col2: display_hand("Banco", sim_result["banker_hand"], sim_result["banker_value"])

        state["timer"] -= 1
        if state["timer"] <= 0:
            state["phase"] = "BETTING"; state["timer"] = 15
            state["last_hand"] = None
            st.rerun()

