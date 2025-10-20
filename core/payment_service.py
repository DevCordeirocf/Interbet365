# core/payment_service.py

"""
Este módulo lida com toda a comunicação com a API do Mercado Pago.
Ele é responsável por:
1. Inicializar o SDK com as credenciais corretas (teste ou produção).
2. Criar preferências de pagamento para depósitos.
3. Processar solicitações de saque (atualmente um placeholder).
"""

import streamlit as st
import mercadopago
import time

def get_mp_sdk():
    """
    Inicializa o SDK do Mercado Pago com o Access Token correto
    baseado no ambiente definido em secrets.toml.
    """
    try:
        # Pega a configuração do ambiente, default é 'test' se não existir
        env = st.secrets.get("environment", "test")

        if env == "prod":
            access_token = st.secrets["MP_ACCESS_TOKEN_PROD"]
            print("SDK do Mercado Pago inicializado em modo PRODUÇÃO.")
        else:
            access_token = st.secrets["MP_ACCESS_TOKEN_TEST"]
            print("SDK do Mercado Pago inicializado em modo TESTE.")
            
        sdk = mercadopago.SDK(access_token)
        return sdk
    except KeyError as e:
        # Exibe um erro claro se uma das chaves estiver faltando no secrets.toml
        st.error(f"Credencial {e} do Mercado Pago não encontrada nos secrets.")
        return None

def create_payment_preference(username: str, user_id: int, amount: float) -> dict | None:
    """
    Cria uma Preferência de Pagamento no Mercado Pago e retorna os dados,
    incluindo o link para o checkout.
    """
    sdk = get_mp_sdk()
    if not sdk:
        return None

    # ==============================================================================
    # ATENÇÃO: CONFIGURAÇÃO DE URLS PARA DESENVOLVIMENTO
    # ==============================================================================
    # 1. NGROK URL: A URL base gerada pelo NGROK.
    #    Ela será usada tanto para o webhook quanto para o redirecionamento.
    ngrok_base_url = "https://27c33be09c45.ngrok-free.app" # SEM a barra no final

    # 2. Monta as URLs completas
    webhook_url = f"{ngrok_base_url}/webhook/mercado-pago"
    redirect_url = f"{ngrok_base_url}/Carteira" # ## MUDANÇA AQUI ##
    # ==============================================================================

    preference_data = {
        "items": [
            {
                "title": f"Depósito na Carteira Wyden365 - Usuário: {username}",
                "quantity": 1,
                "unit_price": amount,
                "currency_id": "BRL"
            }
        ],
        "payer": {
            "name": username,
        },
        "back_urls": {
            # ## CORREÇÃO ## Usamos a URL pública do ngrok aqui também.
            "success": redirect_url,
            "failure": redirect_url,
            "pending": redirect_url
        },
        "auto_return": "approved",
        "external_reference": f"user_{user_id}_deposit_{int(time.time())}",
        "notification_url": webhook_url
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        return preference
    except Exception as e:
        # Imprime o erro no console para depuração
        print(f"Erro ao criar preferência de pagamento: {e}") 
        # Mostra o erro na interface do Streamlit
        st.error("Ocorreu um erro ao se comunicar com o Mercado Pago. Tente novamente.")
        return None

def process_withdrawal(username: str, amount: float, pix_key: str) -> dict:
    """
    Processa um saque via PIX.
    ATENÇÃO: A API de Payouts do Mercado Pago é mais complexa e pode exigir
    aprovação e configuração adicionais. Este código é um placeholder funcional.
    """
    print(f"PLACEHOLDER: Saque solicitado por '{username}' de R${amount} para a chave '{pix_key}'.")
    
    # Na implementação real, você chamaria a API de Payouts aqui.
    # sdk = get_mp_sdk()
    # ... código para criar o Payout ...

    # Retorna uma resposta simulada para a interface.
    return {
        "success": True, 
        "message": "Sua solicitação de saque foi recebida e está em processamento."
    }