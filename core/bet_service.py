
import streamlit as st
from core.db import init_supabase_client
from core.user_service import update_user_balance 

def create_bet(user_id: str, match_id: int, amount: float, prediction: str):
    supabase = init_supabase_client()
    if not supabase: return False

    
    success = update_user_balance(user_id, -amount) 
    
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
            update_user_balance(user_id, amount)
            return False
    else:
        st.error("Saldo insuficiente ou erro ao debitar.")
        return False


def get_bets_by_user(user_id: str):
    supabase = init_supabase_client()
    if not supabase: return []
    
    try:
        response = supabase.table('bets').select(
            '*, match:matches(id, match_datetime, odds_a, odds_b, odds_draw, team_a:team_a_id(name), team_b:team_b_id(name))'
        ).eq('user_id', user_id).order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Erro ao buscar apostas: {e}"); return []