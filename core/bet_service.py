# core/bet_service.py

import streamlit as st
from core.db import init_supabase_client
from core.user_service import update_user_balance # Precisamos disso

def create_bet(user_id: str, match_id: int, amount: float, prediction: str):
    """Cria uma nova aposta e debita o saldo do usuário."""
    supabase = init_supabase_client()
    if not supabase: return False

    # TODO: Implementar lógica de transação do Supabase (RPC) para ser mais seguro
    
    # Debita o saldo
    success = update_user_balance(user_id, -amount) # Usa sinal negativo
    
    if success:
        try:
            bet_data = {
                'user_id': user_id,
                'match_id': match_id,
                'bet_amount': amount,
                'prediction': prediction,
                'status': 'Pendente'
            }
            supabase.table('bets').insert(bet_data).execute()
            return True
        except Exception as e:
            st.error(f"Erro ao criar aposta: {e}")
            # Estorna o valor
            update_user_balance(user_id, amount)
            return False
    else:
        st.error("Saldo insuficiente ou erro ao debitar.")
        return False


def get_bets_by_user(user_id: str):
    """Busca todas as apostas de um usuário específico."""
    supabase = init_supabase_client()
    if not supabase: return []
    
    try:
        # Busca as apostas e faz JOIN para pegar o nome dos times
        response = supabase.table('bets').select(
            '*, match:matches(team_a:team_a_id(name), team_b:team_b_id(name), match_datetime)'
        ).eq('user_id', user_id).order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Erro ao buscar apostas: {e}"); return []