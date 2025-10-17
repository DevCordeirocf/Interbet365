# test_auth_script.py

from core.auth import hash_password, verify_password

print("--- INICIANDO TESTE DE AUTENTICAÇÃO ---")

senha_original = "minhasenha123"
print(f"Senha Original: {senha_original}")

senha_com_hash = hash_password(senha_original)
print(f"Senha com Hash: {senha_com_hash}")
print("-" * 20)


print("Testando com a senha CORRETA...")
verificacao_correta = verify_password(senha_original, senha_com_hash)
print(f"Resultado: {verificacao_correta}") 
assert verificacao_correta is True, "ERRO: A senha correta não foi verificada!"
print("✅ Teste com senha correta passou!")
print("-" * 20)

print("Testando com a senha ERRADA...")
verificacao_errada = verify_password("senha_errada_qualquer", senha_com_hash)
print(f"Resultado: {verificacao_errada}") 
assert verificacao_errada is False, "ERRO: A senha errada foi aceita!"
print("✅ Teste com senha errada passou!")
print("-" * 20)

print("--- TESTE DE AUTENTICAÇÃO CONCLUÍDO COM SUCESSO ---")