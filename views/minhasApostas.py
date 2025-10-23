# views/minhasApostas.py

import streamlit as st
import locale
from core import bet_service
from styles.mybets import load_mybets_styles

# Tenta configurar locale pt_BR; se falhar, usaremos fallback
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except Exception:
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR')
    except Exception:
        # não interrompe; usaremos fallback na formatação
        pass

def format_brl(value: float) -> str:
    """Formata número como Real brasileiro (R$ 10.000,00) com fallback."""
    try:
        return locale.currency(value, grouping=True)
    except Exception:
        s = f"{value:,.2f}"
        # transforma 1,234,567.89 -> 1.234.567,89
        s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"R$ {s}"

def format_odd(odd: float) -> str:
    """Formata odd com fallback."""
    try:
        return f"{odd:.2f}x"
    except Exception:
        return str(odd)

def extract_odd(bet: dict) -> float:
    """Tenta extrair a odd de diversos campos possíveis."""
    # Tenta alguns campos comuns para a odd
    for key in ('odd', 'odds', 'odds_a', 'odds_b', 'odd_value'):
        if key in bet and bet.get(key) is not None:
            try:
                return float(bet.get(key))
            except Exception:
                continue
    # fallback: retorna 1.0 se não encontrar
    return 1.0

def render():
    # Carrega estilos CSS customizados
    load_mybets_styles()
    
    # Bloco de proteção
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("✕ Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    # --- CABEÇALHO CORRIGIDO ---
    # O HTML estava fora do markdown e havia títulos duplicados
    st.markdown("""
        <div class="icon-header">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="hsl(11, 100%, 60%)" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
            </svg>
        </div>
    """, unsafe_allow_html=True)
    st.title("Minhas Apostas")
    # --- FIM DA CORREÇÃO ---
    
    # Obtém dados do usuário
    user_id = st.session_state['user_id']
    all_bets = bet_service.get_bets_by_user(user_id)
    
    # Verifica se há apostas
    if not all_bets:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-title">Nenhuma aposta encontrada</div>
                <div class="empty-state-desc">Você ainda não fez nenhuma aposta. Que tal começar agora?</div>
            </div>
        """, unsafe_allow_html=True)
        st.stop()
        
    # Separa as apostas em abas
    tab_pending, tab_finished = st.tabs([" Apostas Pendentes", " Apostas Finalizadas"])
    
    with tab_pending:
        st.subheader("Aguardando Resultado")
        pending_bets = [bet for bet in all_bets if bet['status'] == 'Pendente']
        
        if not pending_bets:
            st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-title">Nenhuma aposta pendente</div>
                    <div class="empty-state-desc">Você não tem apostas aguardando resultado no momento.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.write(f"**{len(pending_bets)} aposta(s) pendente(s)**")
            st.markdown("---")
            
            for bet in pending_bets:
                # Pega os nomes dos times (o JOIN já foi feito no bet_service)
                match_info = bet.get('match', {}) or {}
                team_a = match_info.get('team_a', {}).get('name', 'Time A')
                team_b = match_info.get('team_b', {}).get('name', 'Time B')

                # Extrai valores com formatação correta
                amount = float(bet.get('bet_amount', 0))

                # Determina a odd correta a partir dos dados da partida
                odds_a = None
                odds_b = None
                odds_draw = None
                try:
                    odds_a = float(match_info.get('odds_a')) if match_info.get('odds_a') is not None else None
                    odds_b = float(match_info.get('odds_b')) if match_info.get('odds_b') is not None else None
                    odds_draw = float(match_info.get('odds_draw')) if match_info.get('odds_draw') is not None else None
                except Exception:
                    pass

                prediction = bet.get('prediction')
                if prediction == 'A':
                    odd = odds_a if odds_a is not None else extract_odd(bet)
                elif prediction == 'B':
                    odd = odds_b if odds_b is not None else extract_odd(bet)
                elif prediction == 'Empate' or prediction == 'Draw':
                    odd = odds_draw if odds_draw is not None else extract_odd(bet)
                else:
                    odd = extract_odd(bet)

                potential = amount * (float(odd) if odd is not None else 1.0)
                
                # --- BLOCO DUPLICADO REMOVIDO DAQUI ---
                # O código anterior tinha um bloco duplicado que
                # sobrescrevia a odd correta com uma errada.

                # Monta o header do expander
                header = f"Aposta de {format_brl(amount)} • {team_a} vs {team_b}"
                
                with st.expander(header):
                    st.markdown(f"**Partida:** {team_a} vs {team_b}")
                    st.markdown(f"**Sua Previsão:** {prediction or bet.get('prediction', '-')}")
                    st.markdown(f"**Valor Apostado:** {format_brl(amount)}")
                    st.markdown(f"**Odd:** {format_odd(odd)}")
                    st.markdown(f"**Retorno Potencial:** {format_brl(potential)}")
                    st.markdown(f"**Status:** {bet.get('status', '-')}")
                
                # --- BLOCO DUPLICADO E MAL FORMATADO REMOVIDO DAQUI ---
                # Havia outro bloco de `st.markdown` duplicado
                # e fora do `with st.expander`

    with tab_finished:
        st.subheader("Histórico de Apostas")
        finished_bets = [bet for bet in all_bets if bet['status'] != 'Pendente']
        
        if not finished_bets:
            st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-title">Nenhuma aposta finalizada</div>
                    <div class="empty-state-desc">Você ainda não possui apostas finalizadas.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.write(f"**{len(finished_bets)} aposta(s) finalizada(s)**")
            st.markdown("---")
            
            # Exibe as apostas finalizadas como cards customizados
            for bet in finished_bets:
                match_info = bet.get('match', {}) or {}
                team_a = match_info.get('team_a', {}).get('name', 'Time A')
                team_b = match_info.get('team_b', {}).get('name', 'Time B')

                amount = float(bet.get('bet_amount', 0))

                # extrai odds da partida quando disponível
                odds_a = None
                odds_b = None
                odds_draw = None
                try:
                    odds_a = float(match_info.get('odds_a')) if match_info.get('odds_a') is not None else None
                    odds_b = float(match_info.get('odds_b')) if match_info.get('odds_b') is not None else None
                    odds_draw = float(match_info.get('odds_draw')) if match_info.get('odds_draw') is not None else None
                except Exception:
                    pass

                prediction = bet.get('prediction')
                if prediction == 'A':
                    odd = odds_a if odds_a is not None else extract_odd(bet)
                elif prediction == 'B':
                    odd = odds_b if odds_b is not None else extract_odd(bet)
                elif prediction == 'Empate' or prediction == 'Draw':
                    odd = odds_draw if odds_draw is not None else extract_odd(bet)
                else:
                    odd = extract_odd(bet)

                potential = amount * (float(odd) if odd is not None else 1.0)
                
                # --- BLOCO DUPLICADO REMOVIDO DAQUI ---
                # O código anterior sobrescrevia a odd correta
                # com `odd = extract_odd(bet)`
                
                status = bet.get('status', '-')
                result = bet.get('result', '')
                
                # Define cor do status
                status_color = "#10b981" if status == "Ganhou" else "#ef4444" if status == "Perdeu" else "#f59e0b"

                # Define o valor do retorno com base no status
                payout_display = 0.0
                if status == "Ganhou":
                    payout_display = potential
                elif status == "Perdeu":
                    payout_display = 0.0 # Perdeu
                else: # Empate/Cancelado
                    payout_display = amount # Devolve a aposta

                # Renderiza card customizado
                html = f"""
                <div style="display:flex;flex-direction:column;gap:8px;padding:16px;border-radius:12px;margin-bottom:12px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);transition:all 0.3s ease;">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                        <div style="font-weight:700;font-size:1.1rem;color:white;">{team_a} <span style="color:rgba(255,255,255,0.5);font-size:0.9rem;">vs</span> {team_b}</div>
                        <div style="font-size:0.9rem;color:{status_color};font-weight:600;text-transform:uppercase;letter-spacing:0.05em;">{status} {('• ' + result) if result else ''}</div>
                    </div>
                    <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:0.95rem;color:rgba(255,255,255,0.8);">
                        <span>Previsão: <strong style="color:white;">{bet.get('prediction', '-')}</strong></span>
                        <span>Valor: <strong style="color:white;">{format_brl(amount)}</strong></span>
                        <span>Odd: <strong style="color:white;">{format_odd(odd)}</strong></span>
                        <span>Retorno: <strong style="color:{status_color};">{format_brl(payout_display)}</strong></span>
                    </div>
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)
