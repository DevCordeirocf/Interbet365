import streamlit as st
from core.db import init_supabase_client
from core.user_service import update_user_balance

# --- LÓGICA DO ADMIN: MODALIDADES ---

def create_modality(name: str):
    supabase = init_supabase_client()
    if not supabase: return None
    try:
        return supabase.table('modalities').insert({'name': name}).execute().data
    except Exception as e:
        st.error(f"Erro ao criar modalidade: {e}"); return None

def get_all_modalities():
    supabase = init_supabase_client()
    if not supabase: return []
    try:
        return supabase.table('modalities').select('id, name').order('name').execute().data
    except Exception as e:
        st.error(f"Erro ao buscar modalidades: {e}"); return []

# --- LÓGICA DO ADMIN: TIMES ---

def create_team(name: str, modality_id: int):
    supabase = init_supabase_client()
    if not supabase: return None
    try:
        return supabase.table('teams').insert({'name': name, 'modality_id': modality_id}).execute().data
    except Exception as e:
        st.error(f"Erro ao criar time: {e}"); return None

def get_all_teams():
    supabase = init_supabase_client()
    if not supabase: return []
    try:
        return supabase.table('teams').select('id, name, modality:modality_id(name)').order('name').execute().data
    except Exception as e:
        st.error(f"Erro ao buscar times: {e}"); return []

# --- LÓGICA DO ADMIN: PARTIDAS ---

def create_match(team_a_id: int, team_b_id: int, match_datetime: str, odds_a: float, odds_b: float, odds_draw: float, modality_id: int):
    supabase = init_supabase_client()
    if not supabase: return None
    try:
        match_data = {
            'team_a_id': team_a_id, 
            'team_b_id': team_b_id, 
            'match_datetime': match_datetime,
            'odds_a': odds_a, 
            'odds_b': odds_b, 
            'odds_draw': odds_draw, 
            'status': 'Agendado',
            'modality_id': modality_id 
        }
        return supabase.table('matches').insert(match_data).execute().data
    except Exception as e:
        st.error(f"Erro ao criar partida: {e}"); return None

def get_open_matches():
    supabase = init_supabase_client()
    if not supabase: return []
    try:
        # --- ALTERAÇÃO 3: Pede o nome da modalidade no select ---
        response = supabase.table('matches').select(
            'id, match_datetime, status, odds_a, odds_b, odds_draw, '
            'team_a:team_a_id(name), ' # Pega só o nome do time A
            'team_b:team_b_id(name), ' # Pega só o nome do time B
            'modality:modality_id(name)' # Pega o nome da modalidade
        ).eq('status', 'Agendado').order('match_datetime', desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"Erro ao buscar partidas agendadas: {e}"); return []
    
def finalize_match(match_id: int, result: str):
    supabase = init_supabase_client()
    if not supabase:
        st.error("Falha ao conectar ao banco de dados.")
        return False

    try:
        match_response = supabase.table('matches').select('odds_a, odds_b, odds_draw').eq('id', match_id).single().execute()
        if not match_response.data:
            st.error(f"Partida {match_id} não encontrada.")
            return False
        
        match_data = match_response.data
        
        odds_map = {'A': match_data['odds_a'], 'B': match_data['odds_b'], 'Empate': match_data['odds_draw']}
        winning_odd = float(odds_map[result])

        bets_response = supabase.table('bets').select('*').eq('match_id', match_id).eq('status', 'Pendente').execute()
        pending_bets = bets_response.data
        
        st.info(f"Processando {len(pending_bets)} apostas pendentes...")
        
        processed_count = 0
        for bet in pending_bets:
            bet_id = bet['id']
            user_id = bet['user_id']
            bet_amount = float(bet.get('bet_amount', 0))
            
            if bet.get('prediction') == result:
                # Aposta Vencedora!
                payout_amount = bet_amount * winning_odd
                
                # Tenta pagar o usuário
                balance_updated = update_user_balance(user_id, payout_amount)
                
                if balance_updated:
                    # Atualiza o status da aposta para 'Ganha'
                    supabase.table('bets').update({'status': 'Ganha'}).eq('id', bet_id).execute()
                    print(f"Aposta {bet_id} ganha. Pagando {payout_amount} para {user_id}")
                    processed_count += 1
                else:
                    # Se não conseguir atualizar o saldo, loga erro e NÃO atualiza a aposta
                    st.error(f"Erro ao pagar aposta {bet_id} para usuário {user_id}. Saldo não atualizado.")
                    print(f"ERRO CRÍTICO: Falha ao atualizar saldo para aposta ganha {bet_id} (user {user_id})")
            
            else:
                # Aposta Perdida
                supabase.table('bets').update({'status': 'Perdida'}).eq('id', bet_id).execute()
                print(f"Aposta {bet_id} perdida.")
                processed_count += 1

        # Atualiza a partida para 'Finalizado' apenas se TODAS as apostas foram processadas (ou não havia apostas)
        if processed_count == len(pending_bets):
            supabase.table('matches').update({
                'status': 'Finalizado',
                'result': result
            }).eq('id', match_id).execute()
            st.success(f"Partida {match_id} finalizada com sucesso! Resultado: {result}. {len(pending_bets)} apostas processadas.")
            return True
        else:
            st.warning(f"Partida {match_id} NÃO finalizada. Algumas apostas não puderam ser pagas devido a erros de saldo.")
            return False

    except Exception as e:
        st.error(f"Erro crítico ao finalizar partida: {e}")
        return False 
