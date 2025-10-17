# webhook_server/app.py

import os
import mercadopago
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

# ... (sua função de placeholder do banco de dados) ...

app = Flask(__name__)

@app.route('/webhook/mercado-pago', methods=['POST'])
def mercadopago_webhook():
    notification = request.json
    print("Notificação recebida:", notification)

    if notification and notification.get("type") == "payment":
        payment_id = notification["data"]["id"]
        
        # Pega a configuração do ambiente, default é 'test'
        env = os.getenv("ENVIRONMENT", "test")

        if env == "prod":
            access_token = os.getenv("MP_ACCESS_TOKEN_PROD")
            print("Webhook processando com credenciais de PRODUÇÃO.")
        else:
            access_token = os.getenv("MP_ACCESS_TOKEN_TEST")
            print("Webhook processando com credenciais de TESTE.")

        if not access_token:
            print("ERRO: Access Token do MP não encontrado nas variáveis de ambiente para o ambiente:", env)
            return jsonify({"status": "error", "message": "configuração do servidor incompleta"}), 500
        
        try:
            sdk = mercadopago.SDK(access_token)
            payment_info = sdk.payment().get(payment_id)
            payment = payment_info["response"]

            if payment["status"] == "approved":
                external_ref = payment.get("external_reference")
                amount = payment.get("transaction_amount")
                if external_ref and amount:
                    # update_database_on_payment(external_ref, amount) # Sua função real
                    print(f"Pagamento {payment_id} aprovado e processado.")
                
        except Exception as e:
            print(f"Erro ao processar o webhook: {e}")
            return jsonify({"status": "error"}), 500

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)