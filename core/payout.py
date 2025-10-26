
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
import time
import uuid 
import requests

# =============================================================================
# FUNÇÃO AUXILIAR DE AUTENTICAÇÃO
# =============================================================================

def get_access_token_and_env():
    # A função load_dotenv() já foi chamada no início do arquivo.
    # O Streamlit não carrega variáveis de ambiente automaticamente, mas o python-dotenv sim.
    env = os.getenv("ENVIRONMENT", "test") 
    access_token = None
    
    if env == "prod":
        print("Usando credenciais de PRODUÇÃO.")
        if not os.getenv("MP_ACCESS_TOKEN_PROD"):
            st.error("Erro fatal: ENVIRONMENT='prod' mas MP_ACCESS_TOKEN_PROD não foi encontrado no .env.")
            return None, None
        access_token = os.getenv("MP_ACCESS_TOKEN_PROD")
    
    else: 
        print("Usando credenciais de TESTE.")
        if not os.getenv("MP_ACCESS_TOKEN_TEST"):
            st.error("Erro fatal: ENVIRONMENT='test' mas MP_ACCESS_TOKEN_TEST não foi encontrado no .env.")
            return None, None
        access_token = os.getenv("MP_ACCESS_TOKEN_TEST")
        
    return access_token, env

# =============================================================================
# FUNÇÃO DE SAQUE (PAYOUT)
# =============================================================================

def process_withdrawal(user_id: str, amount: float, pix_key: str, pix_key_type: str, description: str) -> dict:
    
    try:
        access_token, env = get_access_token_and_env()
        if not access_token:
            return {"success": False, "message": "Erro de configuração do servidor."}
            
        if not os.getenv("MP_SELLER_EMAIL"): 
             st.error("Erro fatal: MP_SELLER_EMAIL não foi encontrado no .env.")
             return {"success": False, "message": "Erro de configuração do servidor."}

    except Exception as e:
        print(f"ERRO CRÍTICO: Falha ao ler credenciais do .env: {e}")
        return {"success": False, "message": "Erro de configuração do servidor."}

    idempotency_key = str(uuid.uuid4())
    payout_data = {
        "amount": float(amount),
        "receiver_id": pix_key,
        "receiver_type": "PIX",
        "currency_id": "BRL",
        "description": description,
        "external_reference": f"payout_user_{user_id}_{int(time.time())}"
    }
    
    url = "https://api.mercadopago.com/v1/payouts"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": idempotency_key
    }

    try:
        response = requests.post(url, json=payout_data, headers=headers)
        api_response = response.json()

        if response.status_code in [200, 201]:
            status = api_response.get("status", "desconhecido")
            status_detail = api_response.get("status_detail", "Sucesso")
            
            print(f"Saque criado com sucesso. ID: {api_response.get('id')}, Status: {status}")
            
            return {
                "success": True, 
                "message": f"Solicitação de saque recebida. Status: {status_detail}",
                "payment_id": api_response.get("id"),
                "status": status
            }
        else:
            error_message = api_response.get("message", "Erro desconhecido")
            print(f"Erro ao processar saque: {error_message}")
            return {"success": False, "message": f"Erro do Mercado Pago: {error_message}"}

    except Exception as e:
        print(f"Erro crítico na chamada da API de Payout: {e}")
        if 'response' in locals() and response.text:
             print(f"Detalhes do erro da API: {response.text}")
             return {"success": False, "message": f"Erro da API: {response.text}"}
        return {"success": False, "message": "Ocorreu um erro inesperado ao processar o saque."}
