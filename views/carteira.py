# views/carteira.py

import streamlit as st
from core import user_service, payment_service

def render():
    # Bloco de proteção
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("🔒 Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    st.title("💵 Minha Carteira")
    
    user_id = st.session_state['user_id']
    username = st.session_state['username']
    
    # --- 1. Exibição do Saldo (Dado de Saída) ---
    balance = user_service.get_user_balance(user_id)
    if balance is not None:
        st.metric(label="Saldo Disponível", value=f"R$ {balance:.2f}")
    else:
        st.error("Não foi possível carregar seu saldo."); balance = 0.0

    
    tab_deposit, tab_withdraw = st.tabs(["Depositar", "Sacar"])

    # --- 2. Aba de Depósito (Inputs e Ações) ---
    with tab_deposit:
        st.subheader("Depositar na Carteira")
        
        with st.form("deposit_form", clear_on_submit=True):
            amount_to_deposit = st.number_input("Valor do depósito (R$)", min_value=5.0, step=5.0, format="%.2f")
            submitted = st.form_submit_button("Gerar Link de Pagamento")

            if submitted:
                st.info("Gerando link de pagamento, aguarde...")
                preference = payment_service.create_payment_preference(
                    username=username,
                    user_id=user_id,
                    amount=amount_to_deposit
                )
                if preference:
                    payment_link = preference.get("init_point")
                    if payment_link:
                        st.link_button("Pagar com Mercado Pago", payment_link, use_container_width=True)
                    else:
                        st.error("Erro ao gerar link de pagamento.")
                else:
                    st.error("Houve um erro ao se comunicar com o Mercado Pago.")

    # --- 3. Aba de Saque (Inputs e Ações) ---
    with tab_withdraw:
        st.subheader("Sacar da Carteira")

        with st.form("withdraw_form"):
            amount_to_withdraw = st.number_input("Valor do saque (R$)", min_value=10.0, step=5.0, format="%.2f")
            pix_key = st.text_input("Sua chave Pix")
            withdraw_submitted = st.form_submit_button("Solicitar Saque")

            if withdraw_submitted:
                if not pix_key:
                    st.warning("Por favor, insira sua chave Pix.")
                elif amount_to_withdraw > balance:
                    st.error("Saldo insuficiente para realizar o saque.")
                else:
                    # Lógica de Saque (Placeholder do Service + Atualização do Saldo)
                    st.info("Processando sua solicitação de saque...")
                    response = payment_service.process_withdrawal(username, amount_to_withdraw, pix_key)
                    if response["success"]:
                        # Debita o valor do saldo
                        user_service.update_user_balance(user_id, -amount_to_withdraw)
                        st.success(response["message"])
                        st.rerun()
                    else:
                        st.error(response["message"])