import streamlit as st
import datetime
from core import match_service
from styles import load_admin_styles

# ==============================
# FUNÇÕES AUXILIARES
# ==============================
def format_for_selectbox(items, key_col='id', value_col='name'):
    """Formata lista de dicts para uso em st.selectbox."""
    if not isinstance(items, list):
        items = []
        
    options = {item[key_col]: item[value_col] for item in items if key_col in item and value_col in item}
    formatted_options = [item[value_col] for item in items if value_col in item]
    return options, formatted_options

# ==============================
# RENDERIZAÇÃO DAS TABS
# ==============================

def render_modalities_tab():
    st.subheader("Adicionar Nova Modalidade")
    
    with st.form("modality_form", clear_on_submit=True):
        modality_name = st.text_input("Nome da Modalidade", placeholder="Ex: Futebol, Vôlei, Basquete")
        
        if st.form_submit_button("Criar Modalidade", use_container_width=True):
            if modality_name:
                result = match_service.create_modality(modality_name)
                if result:
                    st.success(f"Modalidade '{modality_name}' criada com sucesso!")
                    st.rerun()
                # Erro já é mostrado pelo service
            else:
                st.warning("O nome da modalidade não pode ser vazio.")
    
    st.divider()
    st.subheader("Modalidades Existentes")
    modalities = match_service.get_all_modalities()
    
    if modalities:
        st.dataframe(modalities, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma modalidade cadastrada ainda.")

def render_teams_tab():
    st.subheader("Adicionar Novo Time")
    modalities_data = match_service.get_all_modalities()
    
    if not modalities_data:
        st.warning("Você precisa criar uma Modalidade antes de criar um Time.")
    else:
        with st.form("team_form", clear_on_submit=True):
            team_name = st.text_input("Nome do Time", placeholder="Ex: Time da Computação")
            
            modality_map, modality_names = format_for_selectbox(modalities_data, 'id', 'name')
            selected_modality_name = st.selectbox("Modalidade do Time", modality_names)
            
            if st.form_submit_button("Criar Time", use_container_width=True):
                if team_name and selected_modality_name:
                    selected_modality_id = next((k for k, v in modality_map.items() if v == selected_modality_name), None)
                    if selected_modality_id:
                        result = match_service.create_team(team_name, selected_modality_id)
                        if result:
                            st.success(f"Time '{team_name}' criado com sucesso!")
                            st.rerun()
                        # Erro já é mostrado pelo service
                    else:
                         st.error("Modalidade selecionada inválida.")
                else:
                    st.warning("O nome do time e a modalidade são obrigatórios.")
    
    st.divider()
    st.subheader("Times Existentes")
    teams = match_service.get_all_teams()
    
    if teams:
        display_teams = [{'ID': t.get('id'), 'Nome': t.get('name'), 'Modalidade': t.get('modality', {}).get('name', 'N/A')} for t in teams]
        st.dataframe(display_teams, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum time cadastrado ainda.")

def render_matches_tab():
    st.subheader("Criar Nova Partida")
    teams_data = match_service.get_all_teams()
    modalities_data = match_service.get_all_modalities() 
    
    if not teams_data or len(teams_data) < 2:
        st.warning("Você precisa criar pelo menos dois Times antes de criar uma Partida.")
    elif not modalities_data: 
         st.warning("Você precisa criar pelo menos uma Modalidade antes de criar uma Partida.")
    else:
        with st.form("match_form", clear_on_submit=True):
            team_map, team_names = format_for_selectbox(teams_data, 'id', 'name')
            modality_map, modality_names = format_for_selectbox(modalities_data, 'id', 'name') 
            
            selected_modality_name = st.selectbox("Modalidade da Partida", modality_names)
            
            col1, col2 = st.columns(2)
            with col1:
                selected_team_a_name = st.selectbox("Time A", team_names, index=0)
            with col2:
                default_b_index = 1 if len(team_names) > 1 else 0
                selected_team_b_name = st.selectbox("Time B", team_names, index=default_b_index)
            
            col_date, col_time = st.columns(2)
            with col_date:
                match_date = st.date_input("Data da Partida", value=datetime.date.today() + datetime.timedelta(days=1)) 
            with col_time:
                match_time = st.time_input("Hora da Partida", value=datetime.time(19, 0)) 
            
            st.markdown("**Odds da Partida**")
            col_odds_a, col_odds_d, col_odds_b = st.columns(3)
            with col_odds_a:
                odds_a = st.number_input("Odds Time A", min_value=1.01, value=2.10, step=0.05, format="%.2f")
            with col_odds_d:
                odds_draw = st.number_input("Odds Empate", min_value=1.01, value=3.20, step=0.05, format="%.2f")
            with col_odds_b:
                odds_b = st.number_input("Odds Time B", min_value=1.01, value=2.90, step=0.05, format="%.2f")
            
            submitted = st.form_submit_button("Criar Partida", use_container_width=True)
            
            if submitted:
                team_a_id = next((k for k, v in team_map.items() if v == selected_team_a_name), None)
                team_b_id = next((k for k, v in team_map.items() if v == selected_team_b_name), None)
                modality_id = next((k for k, v in modality_map.items() if v == selected_modality_name), None) 

                if not team_a_id or not team_b_id or not modality_id:
                     st.error("Erro ao obter IDs dos times ou modalidade.")
                elif team_a_id == team_b_id:
                    st.error("Um time não pode jogar contra ele mesmo.")
                else:
                    full_match_datetime = datetime.datetime.combine(match_date, match_time)
                    
                    if full_match_datetime <= datetime.datetime.now():
                        st.error("A data e hora da partida devem ser no futuro.")
                    else:
                        match_time_str = full_match_datetime.isoformat()
                        
                        result = match_service.create_match(
                            team_a_id, team_b_id, match_time_str, odds_a, odds_b, odds_draw, modality_id
                        )
                        if result:
                            st.success("Partida criada com sucesso!")
                            st.rerun()
                        # Erro já é mostrado pelo service
    
    st.divider()
    render_finalize_matches_section()
    
    st.divider()
    st.subheader("Partidas Agendadas")
    matches = match_service.get_open_matches()
    
    if matches:
        display_matches = []
        for m in matches:
            # --- CORREÇÃO APLICADA AQUI TAMBÉM ---
            modality_data = m.get('modality')
            modality_name = modality_data.get('name', 'N/A') if modality_data else 'N/A'
            # ------------------------------------
            display_matches.append({
                'ID': m.get('id'),
                'Data/Hora': m.get('match_datetime'),
                'Time A': m.get('team_a', {}).get('name', 'N/A'),
                'Time B': m.get('team_b', {}).get('name', 'N/A'),
                'Modalidade': modality_name, 
                'Odds A': m.get('odds_a'),
                'Odds Empate': m.get('odds_draw'),
                'Odds B': m.get('odds_b'),
                'Status': m.get('status')
            })
        st.dataframe(display_matches, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma partida agendada no momento.")

def render_finalize_matches_section():
    st.subheader("Finalizar Partida Agendada")
    
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
            
            # --- CORREÇÃO APLICADA AQUI ---
            # Verifica se 'modality' não é None antes de pegar o nome
            modality_data = match.get('modality')
            modality_name = modality_data.get('name', 'N/A') if modality_data else 'N/A'
            # -------------------------------
            
            label = f"ID {match_id} | {modality_name}: {team_a} vs {team_b}" 
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
                horizontal=True,
                help="A = Time A venceu, B = Time B venceu"
            )
            
            submitted = st.form_submit_button("Finalizar Partida e Processar Apostas", use_container_width=True)
            
            if submitted:
                if not selected_match_label:
                    st.warning("Você precisa selecionar uma partida.")
                else:
                    match_id_to_finalize = match_map[selected_match_label]
                    st.info(f"Finalizando partida {match_id_to_finalize} com resultado: {result}...")
                    
                    with st.spinner("Processando... Pode levar um momento."):
                        success = match_service.finalize_match(match_id_to_finalize, result)
                    
                    if success:
                        st.success("Partida finalizada e apostas processadas com sucesso!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Ocorreu um erro ao finalizar a partida. Verifique os logs ou o saldo dos usuários.")

# ==============================
# FUNÇÃO PRINCIPAL DE RENDERIZAÇÃO
# ==============================
def render():
    """Renderiza a página de administração"""
    load_admin_styles()
    
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    if st.session_state.get('role') != 'admin':
        st.error("Acesso negado. Esta área é restrita para administradores.")
        st.stop()
    
    st.title("Painel de Administração")
    
    tab_matches, tab_teams, tab_modalities = st.tabs([
        "Gerenciar Partidas", 
        "Gerenciar Times", 
        "Gerenciar Modalidades"
    ])
    
    with tab_modalities:
        render_modalities_tab()
    
    with tab_teams:
        render_teams_tab()
    
    with tab_matches:
        render_matches_tab()

