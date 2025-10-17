_users = {}

def get_user_by_username(username: str) -> dict | None:

    print(f"MOCK DB: Buscando usuário '{username}'...")
    user_data = _users.get(username)
    if user_data:
        print(f"MOCK DB: Usuário '{username}' encontrado.")
    else:
        print(f"MOCK DB: Usuário '{username}' não encontrado.")
    return user_data

def create_user(username: str, hashed_password: str, role: str = 'user') -> bool:

    print(f"MOCK DB: Tentando criar o usuário '{username}'...")
    if username in _users:
        print(f"MOCK DB: Falha ao criar. Usuário '{username}' já existe.")
        return False  
    
    _users[username] = {
        'username': username,
        'hashed_password': hashed_password,
        'role': role,
        'balance': 0.0 
    }
    print(f"MOCK DB: Usuário '{username}' criado com sucesso!")
    print(f"MOCK DB: Estado atual dos usuários: {_users}")
    return True


"-=-=-=-=-=-=-=-=-=-=- MOCK Carteira -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-"

def get_user_balance(username: str) -> float | None:
    """
    Retorna o saldo de um usuário do nosso dicionário de mock.
    """
    username= "luis"
    user = get_user_by_username(username)
    if user:
        return user.get('balance', 10.0)
    return None

def update_user_balance(username: str, amount: float) -> bool:
    """
    Atualiza o saldo de um usuário, somando ou subtraindo um valor.
    """
    amount= 0
    if username in _users:
        _users[username]['balance'] += amount
        print(f"MOCK DB: Saldo de '{username}' atualizado. Novo saldo: {_users[username]['balance']}")
        return True
    return False