import streamlit as st
import datetime
from core import match_service
from styles import load_admin_styles

# ==============================
# FUNÇÕES AUXILIARES
# ==============================
def format_for_selectbox(items, key_col='id', value_col='name'):
    """Transforma uma lista de dicts em opções para st.selectbox."""
    options = {item[key_col]: item[value_col] for item in items}
    formatted_options = [item[value_col] for item in items]
    return options, formatted_options

def render_modalities_tab():
    """Renderiza a tab de modalidades"""
    st.subheader("Adicionar Nova Modalidade")
    
    with st.form("modality_form", clear_on_submit=True):
        modality_name = st.text_input("Nome da Modalidade", placeholder="Ex: Futebol, Vôlei, Basquete")
        
        if st.form_submit_button("Criar Modalidade", use_container_width=True):
            if modality_name:
                match_service.create_modality(modality_name)
                st.success(f"Modalidade '{modality_name}' criada com sucesso!")
                st.rerun()
            else:
                st.warning("O nome da modalidade não pode ser vazio.")
    
    st.divider()
    st.subheader("Modalidades Existentes")
    modalities = match_service.get_all_modalities()
    
    if modalities:
        st.dataframe(modalities, use_container_width=True)
    else:
        st.info("Nenhuma modalidade cadastrada ainda.")

def render_teams_tab():
    """Renderiza a tab de times"""
    st.subheader("Adicionar Novo Time")
    modalities_data = match_service.get_all_modalities()
    
    if not modalities_data:
        st.warning("Você precisa criar uma Modalidade antes de criar um Time.")
    else:
        with st.form("team_form", clear_on_submit=True):
            team_name = st.text_input("Nome do Time", placeholder="Ex: Time da Computação")
            
            # Prepara dados para o selectbox
            modality_map, modality_names = format_for_selectbox(modalities_data, 'id', 'name')
            selected_modality_name = st.selectbox("Modalidade do Time", modality_names)
            
            if st.form_submit_button("Criar Time", use_container_width=True):
                if team_name:
                    # Encontra o ID da modalidade selecionada
                    selected_modality_id = [k for k, v in modality_map.items() if v == selected_modality_name][0]
                    match_service.create_team(team_name, selected_modality_id)
                    st.success(f"Time '{team_name}' criado com sucesso!")
                    st.rerun()
                else:
                    st.warning("O nome do time não pode ser vazio.")
    
    st.divider()
    st.subheader("Times Existentes")
    teams = match_service.get_all_teams()
    
    if teams:
        st.dataframe(teams, use_container_width=True)
    else:
        st.info("Nenhum time cadastrado ainda.")

def render_matches_tab():
    """Renderiza a tab de partidas"""
    st.subheader("Criar Nova Partida")
    teams_data = match_service.get_all_teams()
    
    if not teams_data or len(teams_data) < 2:
        st.warning("Você precisa criar pelo menos dois Times antes de criar uma Partida.")
    else:
        with st.form("match_form", clear_on_submit=True):
            team_map, team_names = format_for_selectbox(teams_data, 'id', 'name')
            
            # Seleção dos times
            col1, col2 = st.columns(2)
            with col1:
                selected_team_a_name = st.selectbox("Time A", team_names, index=0)
            with col2:
                selected_team_b_name = st.selectbox("Time B", team_names, index=1 if len(team_names) > 1 else 0)
            
            # Data e hora da partida
            col_date, col_time = st.columns(2)
            with col_date:
                match_date = st.date_input("Data da Partida", value=datetime.date.today())
            with col_time:
                match_time = st.time_input("Hora da Partida", value=datetime.datetime.now().time())
            
            # Odds
            st.markdown("**Odds da Partida**")
            col_odds_a, col_odds_d, col_odds_b = st.columns(3)
            with col_odds_a:
                odds_a = st.number_input("Odds Time A", min_value=1.01, value=2.00, step=0.1)
            with col_odds_d:
                odds_draw = st.number_input("Odds Empate", min_value=1.01, value=3.00, step=0.1)
            with col_odds_b:
                odds_b = st.number_input("Odds Time B", min_value=1.01, value=2.00, step=0.1)
            
            submitted = st.form_submit_button("Criar Partida", use_container_width=True)
            
            if submitted:
                team_a_id = [k for k, v in team_map.items() if v == selected_team_a_name][0]
                team_b_id = [k for k, v in team_map.items() if v == selected_team_b_name][0]
                
                if team_a_id == team_b_id:
                    st.error("Um time não pode jogar contra ele mesmo.")
                else:
                    # Combina data e hora
                    full_match_datetime = datetime.datetime.combine(match_date, match_time)
                    match_time_str = full_match_datetime.isoformat()
                    
                    match_service.create_match(team_a_id, team_b_id, match_time_str, odds_a, odds_b, odds_draw)
                    st.success("Partida criada com sucesso!")
                    st.rerun()
    
    st.divider()
    render_finalize_matches_section()
    
    st.divider()
    st.subheader("Partidas Agendadas")
    matches = match_service.get_open_matches()
    
    if matches:
        st.dataframe(matches, use_container_width=True)
    else:
        st.info("Nenhuma partida agendada no momento.")

def render_finalize_matches_section():
    """Renderiza a seção de finalizar partidas"""
    st.subheader("Finalizar Partida Agendada")
    
    # Busca partidas abertas
    open_matches = match_service.get_open_matches()
    
    if not open_matches:
        st.info("Nenhuma partida agendada para finalizar.")
    else:
        match_map = {}
        formatted_match_names = []
        
        for match in open_matches:
            team_a = match.get('team_a', {}).get('name', 'Time A')
            team_b = match.get('team_b', {}).get('name', 'Time B')
            match_id = match['id']
            
            label = f"ID {match_id} | {team_a} vs {team_b}"
            formatted_match_names.append(label)
            match_map[label] = match_id
        
        with st.form("finalize_match_form"):
            selected_match_label = st.selectbox(
                "Selecione a partida para finalizar", 
                formatted_match_names
            )
            
            result = st.radio(
                "Resultado Final", 
                ['A', 'B', 'Empate'], 
                horizontal=True
            )
            
            submitted = st.form_submit_button("Finalizar Partida e Processar Apostas", use_container_width=True)
            
            if submitted:
                if not selected_match_label:
                    st.warning("Você precisa selecionar uma partida.")
                else:
                    match_id_to_finalize = match_map[selected_match_label]
                    st.info(f"Finalizando partida {match_id_to_finalize} com resultado: {result}...")
                    
                    success = match_service.finalize_match(match_id_to_finalize, result)
                    
                    if success:
                        st.success("Partida finalizada e apostas processadas com sucesso!")
                        st.rerun()
                    else:
                        st.error("Ocorreu um erro ao finalizar a partida.")

# ==============================
# FUNÇÃO PRINCIPAL DE RENDERIZAÇÃO
# ==============================
def render():
    """Renderiza a página de administração"""
    # Carrega CSS customizado
    load_admin_styles()
    
    # Proteção de acesso
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    if st.session_state['role'] != 'admin':
        st.error("Acesso negado. Esta área é restrita para administradores.")
        st.stop()
    
    # Título principal
    st.title("Painel de Administração")
    
    # Tabs principais
    tab_matches, tab_teams, tab_modalities = st.tabs([
        "Gerenciar Partidas", 
        "Gerenciar Times", 
        "Gerenciar Modalidades"
    ])
    
    # Renderiza cada tab
    with tab_modalities:
        render_modalities_tab()
    
    with tab_teams:
        render_teams_tab()
    
    with tab_matches:
        render_matches_tab()