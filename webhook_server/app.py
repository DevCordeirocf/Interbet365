import os
import mercadopago
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from pathlib import Path
from supabase import create_client, Client

dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

# ==============================================================================
# LÓGICA DE BANCO DE DADOS (Específica para o Servidor Webhook)
# ==============================================================================

def init_supabase_client() -> Client | None:
    try:
        url = os.getenv("SUPABASE_URL")

        key = os.getenv("SUPABASE_SERVICE_KEY") 
        # --- FIM DA CORREÇÃO ---

        if not url or not key:
            print("ERRO DO WEBHOOK: Credenciais SUPABASE_URL ou SUPABASE_SERVICE_KEY não encontradas no arquivo .env")
            return None
        print(f"WEBHOOK: Conectando ao Supabase URL: {url}")
        return create_client(url, key) 
    except Exception as e:
        print(f"ERRO DO WEBHOOK ao inicializar cliente Supabase: {e}")
        return None

def update_database_on_payment(supabase: Client, external_reference: str, amount: float) -> bool:
    print(f"WEBHOOK: Tentando atualizar saldo para a referência: {external_reference}...")
    try:
        parts = external_reference.split('_')
        if len(parts) < 2 or parts[0] != 'user':
            print(f"ERRO DO WEBHOOK: A referência externa '{external_reference}' tem um formato inválido.")
            return False
        user_id = parts[1]
        print(f"WEBHOOK: User ID extraído: {user_id}")

        profile_res = supabase.table('profiles').select('balance').eq('id', user_id).single().execute()
        

        if not profile_res.data:
            print(f"ERRO DO WEBHOOK: Perfil para o usuário {user_id} não foi encontrado na tabela 'profiles'.")
            return False
        

        current_balance = profile_res.data['balance']

        new_balance = float(current_balance) + float(amount)
        print(f"WEBHOOK: Saldo atual: {current_balance}, Valor a adicionar: {amount}, Novo saldo: {new_balance}")

        # 3. Atualiza o saldo na tabela Profiles
        update_res = supabase.table('profiles').update({'balance': new_balance}).eq('id', user_id).execute()

        if update_res.data:
             print(f"WEBHOOK: Saldo do usuário {user_id} atualizado para {new_balance} com sucesso!")

             return True
        else:
             print(f"ERRO DO WEBHOOK: Falha ao executar o update na tabela 'profiles' para o usuário {user_id}.")
             # Você pode querer logar update_res para ver o erro do Supabase
             return False
        
    except Exception as e:
        print(f"ERRO CRÍTICO DO WEBHOOK ao executar a atualização do saldo: {e}")
        import traceback
        traceback.print_exc()
        return False

# ==============================================================================
# SERVIDOR FLASK E ENDPOINT DO WEBHOOK
# ==============================================================================

app = Flask(__name__)

@app.route('/webhook/mercado-pago', methods=['POST'])
def mercadopago_webhook():
    notification = request.json
    print("\n--- Notificação Webhook Recebida ---")
    print(notification)

    # Verifica se é uma notificação de pagamento válida
    if notification and notification.get("type") == "payment" and "data" in notification and "id" in notification["data"]:
        payment_id = notification["data"]["id"]
        print(f"WEBHOOK: Recebido type 'payment' com ID: {payment_id}")
        
        env = os.getenv("ENVIRONMENT", "test")
        access_token = os.getenv("MP_ACCESS_TOKEN_PROD") if env == "prod" else os.getenv("MP_ACCESS_TOKEN_TEST")

        if not access_token:
            print(f"ERRO DO WEBHOOK: Access Token do MP não encontrado para o ambiente: {env}")
            return jsonify({"status": "error", "message": "configuração interna do servidor"}), 500
        
        try:
            print(f"WEBHOOK: Consultando API do MP para detalhes do pagamento {payment_id}...")
            sdk = mercadopago.SDK(access_token)
            payment_info = sdk.payment().get(payment_id)
            payment = payment_info.get("response") # Usar .get() é mais seguro

            if not payment:
                 print(f"ERRO DO WEBHOOK: Resposta da API do MP para get({payment_id}) não continha 'response'.")
                 return jsonify({"status": "error", "message": "resposta inesperada da API MP"}), 500

            print(f"WEBHOOK: Detalhes do pagamento obtidos. Status: {payment.get('status')}")

            # Processa apenas se o status for 'approved'
            if payment.get("status") == "approved":
                print("WEBHOOK: Status 'approved' detectado. Iniciando atualização do banco de dados...")
                supabase_client = init_supabase_client()
                if not supabase_client:
                    print("ERRO DO WEBHOOK: Falha ao inicializar o cliente Supabase.")
                    # Retorna erro 500 para o MP tentar novamente depois
                    return jsonify({"status": "error", "message": "falha na conexão com o banco de dados interno"}), 500
                
                external_ref = payment.get("external_reference")
                amount = payment.get("transaction_amount")
                
                if external_ref and amount is not None: # Verifica se amount não é None
                    print(f"WEBHOOK: Chamando update_database_on_payment com ref='{external_ref}', amount={amount}")
                    success = update_database_on_payment(supabase_client, external_ref, amount)
                    if not success:
                         # Se a atualização falhar, retorna erro para o MP
                         return jsonify({"status": "error", "message": "falha ao atualizar banco de dados interno"}), 500
                else:
                    print("ERRO DO WEBHOOK: 'external_reference' ou 'transaction_amount' ausentes nos detalhes do pagamento.")
                    # Não retorna erro 500 aqui, pois o pagamento foi aprovado, mas não conseguimos processá-lo.
            
            else:
                print(f"WEBHOOK: Status do pagamento não é 'approved' ({payment.get('status')}). Nenhuma ação necessária.")

        except Exception as e:
            print(f"ERRO CRÍTICO DO WEBHOOK ao processar notificação: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"status": "error", "message": "erro interno do servidor"}), 500

    else:
        print("WEBHOOK: Notificação recebida não é do tipo 'payment' ou está mal formatada.")

    # Responde 200 OK para o Mercado Pago acusar o recebimento da notificação
    print("--- Fim do Processamento do Webhook ---")
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    # Use 0.0.0.0 para ser acessível externamente (necessário para ngrok/deploy)
    app.run(host='0.0.0.0', port=5001, debug=True) # debug=True é útil para desenvolvimento
