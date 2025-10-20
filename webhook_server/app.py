# webhook_server/app.py

import os
import mercadopago
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as variáveis de ambiente do arquivo .env (MP_ACCESS_TOKEN, SUPABASE_URL, etc.)
load_dotenv()

# ==============================================================================
# LÓGICA DE BANCO DE DADOS (Específica para o Servidor Webhook)
# ==============================================================================

def init_supabase_client() -> Client | None:
    """Inicializa e retorna o cliente Supabase usando credenciais do .env."""
    try:
        url = os.getenv("SUPABASE_URL")
        # Usamos a SERVICE_KEY aqui porque o webhook precisa de permissões de admin
        # para ignorar o RLS e atualizar o saldo de qualquer usuário.
        key = os.getenv("SUPABASE_SERVICE_KEY")

        if not url or not key:
            print("ERRO DO WEBHOOK: Credenciais do Supabase não encontradas no arquivo .env")
            return None
        return create_client(url, key)
    except Exception as e:
        print(f"ERRO DO WEBHOOK ao inicializar cliente Supabase: {e}")
        return None

def update_database_on_payment(supabase: Client, external_reference: str, amount: float) -> bool:
    """
    Atualiza o saldo do usuário no banco de dados após um pagamento aprovado.
    """
    print(f"WEBHOOK: Atualizando saldo para a referência: {external_reference}...")
    try:
        # Extrai o user_id da referência. O formato é "user_UUID_deposit_TIMESTAMP"
        parts = external_reference.split('_')
        if len(parts) < 2 or parts[0] != 'user':
            print(f"ERRO DO WEBHOOK: A referência externa '{external_reference}' tem um formato inválido.")
            return False
        user_id = parts[1]

        # 1. Pega o saldo atual do usuário
        profile_res = supabase.table('Profiles').select('balance').eq('id', user_id).single().execute()
        
        if not profile_res.data:
            print(f"ERRO DO WEBHOOK: Perfil para o usuário {user_id} não foi encontrado.")
            return False

        # 2. Calcula o novo saldo
        current_balance = profile_res.data['balance']
        new_balance = float(current_balance) + float(amount)

        # 3. Atualiza o saldo na tabela Profiles
        update_res = supabase.table('Profiles').update({'balance': new_balance}).eq('id', user_id).execute()

        # Opcional: Registra a transação como 'Concluída'
        # supabase.table('Transactions').update({'status': 'Concluído'}).eq('external_id', payment_id).execute()

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
                    # ** AQUI ESTÁ A MUDANÇA PRINCIPAL **
                    # Chamamos a função real que atualiza o banco de dados
                    update_database_on_payment(supabase_client, external_ref, amount)
                    
        except Exception as e:
            print(f"Erro ao processar o webhook: {e}")
            return jsonify({"status": "error"}), 500

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)