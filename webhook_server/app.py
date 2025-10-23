# webhook_server/app.py

import os
import mercadopago
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# ==============================================================================
# LÓGICA DE BANCO DE DADOS (Específica para o Servidor Webhook)
# ==============================================================================

def init_supabase_client() -> Client | None:
    try:
        url = os.getenv("SUPABASE_URL")

        if not url or not key:
            print("ERRO DO WEBHOOK: Credenciais do Supabase não encontradas no arquivo .env")
            return None
        return create_client(url, key)
    except Exception as e:
        print(f"ERRO DO WEBHOOK ao inicializar cliente Supabase: {e}")
        return None

def update_database_on_payment(supabase: Client, external_reference: str, amount: float) -> bool:
    print(f"WEBHOOK: Atualizando saldo para a referência: {external_reference}...")
    try:
        parts = external_reference.split('_')
        if len(parts) < 2 or parts[0] != 'user':
            print(f"ERRO DO WEBHOOK: A referência externa '{external_reference}' tem um formato inválido.")
            return False
        user_id = parts[1]

        profile_res = supabase.table('profiles').select('balance').eq('id', user_id).single().execute()
        
        if not profile_res.data:
            print(f"ERRO DO WEBHOOK: Perfil para o usuário {user_id} não foi encontrado.")
            return False

        current_balance = profile_res.data['balance']
        new_balance = float(current_balance) + float(amount)

        update_res = supabase.table('profiles').update({'balance': new_balance}).eq('id', user_id).execute()


        print(f"WEBHOOK: Saldo do usuário {user_id} atualizado para {new_balance} com sucesso!")
        return True
        
    except Exception as e:
        print(f"ERRO DO WEBHOOK ao executar a atualização do saldo: {e}")
        return False

# ==============================================================================
# SERVIDOR FLASK E ENDPOINT DO WEBHOOK
# ==============================================================================

app = Flask(__name__)

@app.route('/webhook/mercado-pago', methods=['POST'])
def mercadopago_webhook():
    notification = request.json
    print("Notificação recebida:", notification)

    if notification and notification.get("type") == "payment":
        payment_id = notification["data"]["id"]
        
        env = os.getenv("ENVIRONMENT", "test")
        access_token = os.getenv("MP_ACCESS_TOKEN_PROD") if env == "prod" else os.getenv("MP_ACCESS_TOKEN_TEST")

        if not access_token:
            print(f"ERRO: Access Token do MP não encontrado para o ambiente: {env}")
            return jsonify({"status": "error", "message": "configuração do servidor incompleta"}), 500
        
        try:
            sdk = mercadopago.SDK(access_token)
            payment_info = sdk.payment().get(payment_id)
            payment = payment_info["response"]

            if payment.get("status") == "approved":
                supabase_client = init_supabase_client()
                if not supabase_client:
                    return jsonify({"status": "error", "message": "falha na conexão com o banco de dados"}), 500
                
                external_ref = payment.get("external_reference")
                amount = payment.get("transaction_amount")
                
                if external_ref and amount:
                    update_database_on_payment(supabase_client, external_ref, amount)
                    
        except Exception as e:
            print(f"Erro ao processar o webhook: {e}")
            return jsonify({"status": "error"}), 500

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)