# core/payment_service.py - VERSÃO FINAL PRODUÇÃO

import streamlit as st
import time
import uuid 
import requests
import mercadopago # SDK v1
import mercadopago.config
from datetime import datetime, timedelta, timezone

def get_access_token_and_env():
    """
    Verifica o 'environment' e retorna o Access Token correto.
    Falha com um erro claro se o token do ambiente não for encontrado.
    """
    env = st.secrets.get("ENVIRONMENT", "test") # Lê 'ENVIRONMENT'
    access_token = None
    
    if env == "prod":
        print("Usando credenciais de PRODUÇÃO.")
        if "MP_ACCESS_TOKEN_PROD" not in st.secrets or not st.secrets["MP_ACCESS_TOKEN_PROD"]:
            st.error("Erro fatal: ENVIRONMENT='prod' mas MP_ACCESS_TOKEN_PROD não foi encontrado nos secrets.")
            return None, None
        access_token = st.secrets["MP_ACCESS_TOKEN_PROD"]
    
    else: # env == "test"
        print("Usando credenciais de TESTE.")
        if "MP_ACCESS_TOKEN_TEST" not in st.secrets or not st.secrets["MP_ACCESS_TOKEN_TEST"]:
            st.error("Erro fatal: ENVIRONMENT='test' mas MP_ACCESS_TOKEN_TEST não foi encontrado nos secrets.")
            return None, None
        access_token = st.secrets["MP_ACCESS_TOKEN_TEST"]
        
    return access_token, env

def get_mp_sdk():
    """
    Inicializa o SDK v1.x do Mercado Pago com o Access Token correto.
    """
    access_token, env = get_access_token_and_env()
    if not access_token:
        return None
        
    try:
        sdk = mercadopago.SDK(access_token)
        return sdk
    except Exception as e:
        st.error(f"Erro ao inicializar SDK: {e}")
        return None

def create_payment_preference(username: str, user_id: int, user_email: str, amount: float) -> dict | None:
    """
    Cria uma Preferência de Pagamento (Checkout Pro) usando o SDK v1.x.
    (Inclui TODOS os campos de Qualidade de Integração)
    """
    sdk = get_mp_sdk()
    if not sdk:
        return None 

    ngrok_base_url = "https://53c4-67fd-08ad.ngrok-free.app" 
    webhook_url = f"{ngrok_base_url}/webhook/mercado-pago" 
    redirect_url = f"{ngrok_base_url}/Carteira"

    preference_data = {
        # --- Ações Obrigatórias (Conciliação) ---
        "notification_url": webhook_url,
        "external_reference": f"user_{user_id}_deposit_pref_{int(time.time())}",
        
        # --- Itens (Aprovação) ---
        "items": [
            {
                "id": "SKU-DEPOSITO-WYDEN", # Código do item
                "title": f"Depósito na Carteira Wyden3G5 - {username}",
                "description": "Créditos para plataforma Wyden3G5", # Descrição
                "category_id": "games", # Categoria
                "quantity": 1,
                "unit_price": amount,
                "currency_id": "BRL"
            }
        ],
        
        # --- Comprador (Aprovação) ---
        "payer": { 
            "name": username,
            "email": user_email
        },
        
        # --- Experiência de Compra ---
        "back_urls": {
            "success": redirect_url,
            "failure": redirect_url,
            "pending": redirect_url
        },
        "auto_return": "approved",
        "statement_descriptor": "WYDEN365", # Nome na fatura
        "binary_mode": True, # Resposta binária
        
        "payment_methods": {
            "excluded_payment_methods": [],
            "excluded_payment_types": [],
            "installments": 1
        }
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})
        return preference
    except Exception as e:
        print(f"Erro ao criar preferência: {e}") 
        st.error("Ocorreu um erro ao se comunicar com o Mercado Pago (Depósito). Tente novamente.")
        return None

# =============================================================================
# FUNÇÃO DE CRIAR PIX DIRETO (Checkout API)
# =============================================================================
def create_pix_payment(username: str, user_id: str, amount: float, email: str, cpf: str) -> dict | None:
    """
    Cria um pagamento PIX direto (Checkout API) usando 'requests'.
    """
    try:
        access_token, env = get_access_token_and_env()
        if not access_token:
            return None 
    except Exception as e:
        st.error(f"Erro ao ler credenciais: {e}")
        return None

    external_reference = f"user_{user_id}_deposit_pix_{int(time.time())}"
    ngrok_base_url = "https://53c4-67fd-08ad.ngrok-free.app"
    webhook_url = f"{ngrok_base_url}/webhook/mercado-pago"

    brasil_tz = timezone(timedelta(hours=-3))
    expiration_time = datetime.now(brasil_tz) + timedelta(minutes=30)
    expiration_str = expiration_time.isoformat(timespec='milliseconds')

    if not cpf:
        st.error("Erro interno: CPF é obrigatório para gerar PIX.")
        return None
    cpf_clean = cpf.replace(".", "").replace("-", "").replace(" ", "")

    payment_data = {
        "transaction_amount": float(amount),
        "description": f"Depósito Carteira Wyden365 - {username}",
        "payment_method_id": "pix",
        "external_reference": external_reference,
        "notification_url": webhook_url,
        "date_of_expiration": expiration_str, 
        "payer": {
            "email": email,
            "identification": {
                "type": "CPF",
                "number": cpf_clean
            }
        }
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": str(uuid.uuid4())
    }
    
    url = "https://api.mercadopago.com/v1/payments"
    
    try:
        response = requests.post(url, json=payment_data, headers=headers)
        response_data = response.json()

        if response.status_code in [200, 201]:
            pix_data = response_data.get("point_of_interaction", {}).get("transaction_data", {})
            return {
                "success": True,
                "payment_id": response_data.get("id"),
                "status": response_data.get("status"),
                "qr_code": pix_data.get("qr_code", ""),
                "qr_code_base64": pix_data.get("qr_code_base64", ""),
                "ticket_url": pix_data.get("ticket_url", ""),
                "external_reference": external_reference,
                "expiration_date": response_data.get("date_of_expiration", "")
            }
        else:
            error_msg = response_data.get("message", "Erro desconhecido")
            error_details = response_data.get("cause", [])
            print(f"Erro ao criar pagamento PIX: {error_msg}")
            print(f"Detalhes completos: {response_data}")
            
            if error_details:
                error_description = error_details[0].get("description", error_msg)
                st.error(f"Erro ao gerar PIX: {error_description}")
            else:
                st.error(f"Erro ao gerar PIX: {error_msg}")
            
            return None

    except Exception as e:
        print(f"Erro crítico ao criar pagamento PIX: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Resposta da API: {response.text}")
        st.error("Erro ao se comunicar com o Mercado Pago. Tente novamente.")
        return None

# =============================================================================
# FUNÇÃO AUXILIAR: VERIFICAR STATUS DO PAGAMENTO PIX
# =============================================================================

def check_pix_payment_status(payment_id: str) -> dict | None:
    """
    Verifica o status de um pagamento PIX pelo ID.
    """
    access_token, env = get_access_token_and_env()
    if not access_token:
        return None

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            payment_data = response.json()
            return {
                "status": payment_data.get("status"),
                "status_detail": payment_data.get("status_detail"),
                "transaction_amount": payment_data.get("transaction_amount"),
                "date_approved": payment_data.get("date_approved")
            }
        return None
    except Exception as e:
        print(f"Erro ao verificar status do pagamento: {e}")
        return None

# =============================================================================
# FUNÇÃO DE SAQUE (PAYOUT)
# =============================================================================

def process_withdrawal(user_id: str, amount: float, pix_key: str, pix_key_type: str, description: str) -> dict:
    """
    Processa um saque via PIX (Payout) usando a biblioteca 'requests'
    para fazer a chamada de API manualmente (compatível com v1).
    """
    
    try:
        access_token, env = get_access_token_and_env()
        if not access_token:
            return {"success": False, "message": "Erro de configuração do servidor."}
            
        if "MP_SELLER_EMAIL" not in st.secrets:
             st.error("Erro fatal: MP_SELLER_EMAIL não foi encontrado nos secrets.")
             return {"success": False, "message": "Erro de configuração do servidor."}
        seller_email = st.secrets["MP_SELLER_EMAIL"]

    except Exception as e:
        print(f"ERRO CRÍTICO: Falha ao ler credenciais dos secrets: {e}")
        return {"success": False, "message": "Erro de configuração do servidor."}

    idempotency_key = str(uuid.uuid4())

    # Payload de SAQUE (Payout) v1
    payout_data = {
        "transaction_amount": amount,
        "description": description,
        "payment_method_id": "pix",
        "payer": {
            "email": seller_email 
        },
        "point_of_interaction": {
            "type": "PIX",
            "transaction_data": {
                "key": pix_key,
                "key_type": pix_key_type
            }
        }
    }
    
    url = "https://api.mercadopago.com/v1/payments"
    
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
