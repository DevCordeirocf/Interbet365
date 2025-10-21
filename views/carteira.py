# views/carteira.py

import streamlit as st
from core import user_service
from core import payment_service 

def render():
    # --- 1. Bloco de Proteção ---
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("🔒 Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    # --- 2. Conteúdo da Página ---
    st.title("💵 Minha Carteira")
    
    user_id = st.session_state['user_id']
    balance = user_service.get_user_balance(user_id) # Usando a função real
    
    if balance is not None:
        st.metric(label="Saldo Disponível", value=f"R$ {balance:.2f}")
    else:
        st.error("Não foi possível carregar seu saldo.")

    tab_deposit, tab_withdraw = st.tabs(["Depositar", "Sacar"])

    with tab_deposit:
        st.subheader("Depositar na Carteira")
        st.write("O formulário para gerar o link do Mercado Pago ficará aqui.")
        # Cole o código do formulário de depósito aqui quando estiver pronto

    with tab_withdraw:
        st.subheader("Sacar da Carteira")
        st.write("O formulário para solicitar um saque (Pix) ficará aqui.")