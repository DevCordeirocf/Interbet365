

import streamlit as st
import time
import uuid 
import requests # <--- IMPORTAMOS O REQUESTS

# --- IMPORTAÇÕES CORRIGIDAS (v1.x) ---
# Esta é a sintaxe de importação correta para a versão
# antiga do SDK que você tem instalada.
import mercadopago
import mercadopago.config 
# -------------------------------------

def get_mp_sdk():
    """
    Inicializa o SDK v1.x do Mercado Pago com o Access Token correto.
    """
    try:
        access_token = st.secrets["MP_ACCESS_TOKEN_PROD"]
        sdk = mercadopago.SDK(access_token)
        print(sdk)
        return sdk
    except KeyError as e:
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
        st.error(f"Credencial {e} do Mercado Pago não encontrada nos secrets.")
        return None

def create_payment_preference(username: str, user_id: int, amount: float) -> dict | None:
    """
    Cria uma Preferência de Pagamento (Checkout Pro) usando o SDK v1.x.
    """
    sdk = get_mp_sdk()
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
    if not sdk:
        return None

    ngrok_base_url = "https://53c4-67fd-08ad.ngrok-free.app" 
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
    webhook_url = f"{ngrok_base_url}/webhook/mercado-pagos" 
    redirect_url = f"{ngrok_base_url}/Carteira"

    preference_data = {
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
        "items": [
            {
                "title": f"Depósito na Carteira Wyden3G5 - Usuário: {username}",
                "quantity": 1,
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
                "unit_price": amount,
                "currency_id": "BRL"
            }
        ],
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
        "payer": {
            "name": username,
        },
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
        "back_urls": {
            "success": redirect_url,
            "failure": redirect_url,
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
            "pending": redirect_url
        },
        "auto_return": "approved",
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
        "external_reference": f"user_{user_id}_deposit_{int(time.time())}",
        "notification_url": webhook_url,
        "payment_methods": {
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
            "excluded_payment_methods": [],
            "excluded_payment_types": [],
            "installments": 1
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
        }
    }

    try:
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
        # A sintaxe v1.x espera o JSON diretamente
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
        return preference
    except Exception as e:
        print(f"Erro ao criar preferência: {e}") 
# ... (código get_mp_sdk e create_payment_preference permanecem os mesmos) ...
        st.error("Ocorreu um erro ao se comunicar com o Mercado Pago (Depósito). Tente novamente.")
        return None

# --- FUNÇÃO DE SAQUE (PAYOUT) USANDO 'REQUESTS' (SOLUÇÃO MANUAL) ---

def process_withdrawal(user_id: str, amount: float, pix_key: str, pix_key_type: str, description: str) -> dict:
# ... (código de process_withdrawal permanece o mesmo) ...
    """
    Processa um saque via PIX (Payout) usando a biblioteca 'requests'
    para fazer a chamada de API manualmente, já que o SDK v1 não
# ... (código de process_withdrawal permanece o mesmo) ...
    dá suporte ou está quebrado no seu ambiente.
    """
    
    try:
# ... (código de process_withdrawal permanece o mesmo) ...
        # 1. Obter o Access Token e o E-mail do Vendedor dos secrets
        env = st.secrets.get("environment", "test")
        if env == "prod":
# ... (código de process_withdrawal permanece o mesmo) ...
            access_token = st.secrets["MP_ACCESS_TOKEN_PROD"]
        else:
            access_token = st.secrets["MP_ACCESS_TOKEN_TEST"]
            
        seller_email = st.secrets["MP_SELLER_EMAIL"]

    except KeyError as e:
# ... (código de process_withdrawal permanece o mesmo) ...
        print(f"ERRO CRÍTICO: Credencial {e} não definida nos secrets.toml")
        return {"success": False, "message": "Erro de configuração do servidor."}

    # 2. Criar uma chave de Idempotência única
# ... (código de process_withdrawal permanece o mesmo) ...
    idempotency_key = str(uuid.uuid4())

    # 3. Montar o JSON (payload) para a API de Payouts
    # --- CORREÇÃO FINAL ---
    # Este é o formato JSON correto para a API /v1/payments (v1)
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
    
    # 4. Definir a URL da API de Payouts (Saques)
    # --- CORREÇÃO FINAL ---
    # Voltamos para /v1/payments, que é a API correta para o JSON acima
    url = "https://api.mercadopago.com/v1/payments"
    
    # 5. Montar os Headers da requisição
    headers = {
# ... (código de process_withdrawal permanece o mesmo) ...
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": idempotency_key
# ... (código de process_withdrawal permanece o mesmo) ...
    }

    try:
        # 6. Fazer a chamada de API manual
# ... (código de process_withdrawal permanece o mesmo) ...
        response = requests.post(url, json=payout_data, headers=headers)
        
        # 7. Analisar a resposta
# ... (código de process_withdrawal permanece o mesmo) ...
        api_response = response.json() # Converte a resposta JSON em um dicionário

        if response.status_code in [200, 201]:
# ... (código de process_withdrawal permanece o mesmo) ...
            status = api_response.get("status", "desconhecido")
            status_detail = api_response.get("status_detail", "Sucesso")
            
            print(f"Saque criado com sucesso. ID: {api_response.get('id')}, Status: {status}")
# ... (código de process_withdrawal permanece o mesmo) ...
            
            return {
                "success": True, 
# ... (código de process_withdrawal permanece o mesmo) ...
                "message": f"Solicitação de saque recebida. Status: {status_detail}",
                "payment_id": api_response.get("id"),
                "status": status
# ... (código de process_withdrawal permanece o mesmo) ...
            }
        else:
            # Captura a mensagem de erro da API
# ... (código de process_withdrawal permanece o mesmo) ...
            error_message = api_response.get("message", "Erro desconhecido")
            print(f"Erro ao processar saque: {error_message}")
            return {"success": False, "message": f"Erro do Mercado Pago: {error_message}"}

    except Exception as e:
# ... (código de process_withdrawal permanece o mesmo) ...
        print(f"Erro crítico na chamada da API de Payout (Requests): {e}")
        if 'response' in locals() and response.text:
             print(f"Detalhes do erro da API: {response.text}")
# ... (código de process_withdrawal permanece o mesmo) ...
             return {"success": False, "message": f"Erro da API: {response.text}"}
        return {"success": False, "message": "Ocorreu um erro inesperado ao processar o saque."}

