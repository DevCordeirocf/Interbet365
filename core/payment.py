
import streamlit as st
import time
import uuid 
import requests
import mercadopago
from datetime import datetime, timedelta, timezone

def get_access_token_and_env():
    env = st.secrets.get("ENVIRONMENT", "test") 
    access_token = None
    
    if env == "prod":
        print("Usando credenciais de PRODUÇÃO.")
        if "MP_ACCESS_TOKEN_PROD" not in st.secrets or not st.secrets["MP_ACCESS_TOKEN_PROD"]:
            st.error("Erro fatal: ENVIRONMENT='prod' mas MP_ACCESS_TOKEN_PROD não foi encontrado nos secrets.")
            return None, None
        access_token = st.secrets["MP_ACCESS_TOKEN_PROD"]
    
    else: 
        print("Usando credenciais de TESTE.")
        if "MP_ACCESS_TOKEN_TEST" not in st.secrets or not st.secrets["MP_ACCESS_TOKEN_TEST"]:
            st.error("Erro fatal: ENVIRONMENT='test' mas MP_ACCESS_TOKEN_TEST não foi encontrado nos secrets.")
            return None, None
        access_token = st.secrets["MP_ACCESS_TOKEN_TEST"]
        
    return access_token, env


def get_mp_sdk():
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
    sdk = get_mp_sdk()
    if not sdk:
        return None 

    ngrok_base_url = "https://53c4-67fd-08ad.ngrok-free.app" 
    webhook_url = f"{ngrok_base_url}/webhook/mercado-pago" 
    redirect_url = f"{ngrok_base_url}/Carteira"

    preference_data = {
        "notification_url": webhook_url,
        "external_reference": f"user_{user_id}_deposit_pref_{int(time.time())}",
        
        "items": [
            {
                "id": "SKU-DEPOSITO-WYDEN", 
                "title": f"Depósito na Carteira Wyden3G5 - {username}",
                "description": "Créditos para plataforma Wyden3G5", 
                "category_id": "games", 
                "quantity": 1,
                "unit_price": amount,
                "currency_id": "BRL"
            }
        ],
        
        "payer": { 
            "name": username,
            "email": user_email
        },
        
        "back_urls": {
            "success": redirect_url,
            "failure": redirect_url,
            "pending": redirect_url
        },
        "auto_return": "approved",
        "statement_descriptor": "WYDEN365",
        "binary_mode": True, 
        
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
# FUNÇÕES DE DEPÓSITO (PIX DIRETO / CHECKOUT API)
# =============================================================================

def create_pix_payment(username: str, user_id: str, amount: float, email: str, cpf: str) -> dict | None:
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
