# core/match_service.py

import streamlit as st
from core.db import init_supabase_client # Importa o conector

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
        return supabase.table('teams').select('id, name, modalities(name)').order('name').execute().data
    except Exception as e:
        st.error(f"Erro ao buscar times: {e}"); return []

# --- LÓGICA DO ADMIN: PARTIDAS ---

def create_match(team_a_id: int, team_b_id: int, match_datetime: str, odds_a: float, odds_b: float, odds_draw: float):
    supabase = init_supabase_client()
    if not supabase: return None
    try:
        match_data = {
            'team_a_id': team_a_id, 'team_b_id': team_b_id, 'match_datetime': match_datetime,
            'odds_a': odds_a, 'odds_b': odds_b, 'odds_draw': odds_draw, 'status': 'Agendado'
        }
        return supabase.table('matches').insert(match_data).execute().data
    except Exception as e:
        st.error(f"Erro ao criar partida: {e}"); return None

def get_open_matches():
    supabase = init_supabase_client()
    if not supabase: return []
    try:
        response = supabase.table('matches').select(
            'id, match_datetime, status, odds_a, odds_b, odds_draw, '
            'team_a:team_a_id(name), team_b:team_b_id(name)'
        ).eq('status', 'Agendado').order('match_datetime', desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"Erro ao buscar partidas agendadas: {e}"); return []