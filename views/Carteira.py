# views/carteira.py

import streamlit as st
# Importa os módulos do backend REAL
from core import database_mock, payment_service 

def render():
    # =====================================================================
    # 1. BLOCO DE PROTEÇÃO - Garante que apenas usuários logados vejam
    # =====================================================================
    """if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("🔒 Acesso negado. Por favor, faça o login primeiro.")
        st.stop() # Interrompe a execução do resto da página"""

    # Pega o nome de usuário da sessão para usar nas funções
    "username = st.session_state['username']"
    # NOTA: Garanta que, no seu Wyden365.py, você salve o ID do usuário na sessão
    # após o login. Ex: st.session_state['user_id'] = user_data['id']
    """ user_id = st.session_state.get('user_id', None)
     if not user_id:
        st.error("Erro: ID do usuário não encontrado na sessão. Faça o login novamente.")
        st.stop()"""


    # =====================================================================
    # 2. EXIBIÇÃO DO SALDO ATUAL
    # =====================================================================
    st.title("💵 Minha Carteira")

    current_balance = database_mock.get_user_balance(username="username")
    if current_balance is not None:
        st.metric(label="Saldo Disponível", value=f"R$ {current_balance:.2f}")
    else:
        st.error("Não foi possível carregar seu saldo.")
        current_balance = 0.0 # Define como 0 para evitar erros na lógica de saque


    # =====================================================================
    # 3. INTERFACE COM ABAS PARA DEPOSITAR E SACAR
    # =====================================================================
    tab_deposit, tab_withdraw = st.tabs(["Depositar", "Sacar"])

    # --- Aba de Depósito ---
    with tab_deposit:
        st.subheader("Depositar na Carteira")
        
        with st.form("deposit_form", clear_on_submit=True):
            amount_to_deposit = st.number_input(
                "Valor do depósito (R$)", 
                min_value=5.0, 
                step=5.0,
                format="%.2f"
            )
            submitted = st.form_submit_button("Gerar Link de Pagamento Pix")

            if submitted:
                if amount_to_deposit >= 5.0:
                    st.info("Gerando link de pagamento, aguarde...")
                    
                    # Chama a função REAL do payment_service
                    preference = payment_service.create_payment_preference(
            
                        username="luis",
                        user_id="1",
                        amount=amount_to_deposit
                    )
                    
                    if preference:
                        # Pega o link diretamente do dicionário 'preference'
                        payment_link = preference.get("init_point")
                        
                        # Verifica se o link foi encontrado e é uma string
                        if payment_link and isinstance(payment_link, str):
                            st.success("Link de pagamento gerado! Clique abaixo para pagar.")
                            st.link_button("Pagar com Mercado Pago", payment_link, use_container_width=True)
                            st.info("Após o pagamento ser aprovado, seu saldo será atualizado automaticamente.")
                        else:
                            st.error("Erro: A resposta da API não continha um link de pagamento válido.")
                            st.json(preference) # Mostra a resposta da API para ajudar a depurar
                    else:
                        st.error("Houve um erro ao gerar o link de pagamento. Tente novamente.")
                        st.info("Após o pagamento ser aprovado, seu saldo será atualizado automaticamente.")
                else:
                    st.warning("O valor mínimo para depósito é de R$ 5,00.")

    # --- Aba de Saque ---
    with tab_withdraw:
        st.subheader("Sacar da Carteira")

        with st.form("withdraw_form"):
            amount_to_withdraw = st.number_input(
                "Valor do saque (R$)",
                min_value=10.0,
                step=5.0,
                format="%.2f"
            )
            pix_key = st.text_input("Sua chave Pix")
            
            withdraw_submitted = st.form_submit_button("Solicitar Saque")

            if withdraw_submitted:
                if not pix_key:
                    st.warning("Por favor, insira sua chave Pix.")
                elif amount_to_withdraw > current_balance:
                    st.error("Saldo insuficiente para realizar o saque.")
                else:
                    st.info("Processando sua solicitação de saque...")
                    
                    # Chama a função de saque
                    # LEMBRETE: Esta função é um placeholder e precisa da lógica real
                    response = payment_service.process_withdrawal(
                        username="loius",
                        amount=amount_to_withdraw,
                        pix_key=pix_key
                    )
                    
                    if response["success"]:
                        username="luis"
                        # Debita o valor do saldo do usuário no banco de dados
                        database_mock.update_user_balance(username, -amount_to_withdraw)
                        st.success(response["message"])
                        st.rerun() # Recarrega a página para mostrar o novo saldo
                    else:
                        st.error(response["message"])