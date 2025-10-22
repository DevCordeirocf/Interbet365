import streamlit as st
import locale
from core import user_service, payment_service
from styles.wallet import load_wallet_styles

# Configura o locale para português do Brasil
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    print("Locale pt_BR.UTF-8 não encontrado, usando locale padrão.")
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except:
        print("Locale C.UTF-8 também não encontrado, formatação pode falhar.")


def render_header():
    """Renderiza o header da página"""
    st.markdown("""
    """, unsafe_allow_html=True)
    
    st.title("Minha Carteira")
    st.markdown('<p class="stSubheader">Gerencie seus depósitos e saques</p>', unsafe_allow_html=True)

def render_balance_card(balance):
    """Renderiza o card de saldo com design destacado usando classes CSS"""
    try:
        # Tenta formatar usando locale
        formatted_balance = locale.currency(balance, grouping=True, symbol='R$')
    except Exception:
        # Fallback: formatação manual
        formatted_balance = f"R$ {balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    st.markdown(f"""
        <div class="balance-card">
            <div class="balance-label">Saldo Disponível</div>
            <div class="balance-value">{formatted_balance}</div>
        </div>
    """, unsafe_allow_html=True)

def render_feature_cards_deposit():
    """Renderiza os cards de features para depósito"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
                    </svg>
                </div>
                <div class="feature-title">Instantâneo</div>
                <div class="feature-desc">Crédito imediato</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                    </svg>
                </div>
                <div class="feature-title">Seguro</div>
                <div class="feature-desc">Pagamento via Mercado Pago</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="2" y="5" width="20" height="14" rx="2"></rect>
                        <line x1="2" y1="10" x2="22" y2="10"></line>
                    </svg>
                </div>
                <div class="feature-title">Flexível</div>
                <div class="feature-desc">Funcional a qualquer momento</div>
            </div>
        """, unsafe_allow_html=True)

def render_feature_cards_withdraw():
    """Renderiza os cards de features para saque"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">Via PIX</div>
                <div class="feature-desc">Rápido e fácil</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">24-48h</div>
                <div class="feature-desc">Processamento</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">Mínimo R$ 10</div>
                <div class="feature-desc">Valor mínimo</div>
            </div>
        """, unsafe_allow_html=True)

def render_deposit_tab(username, user_id):
    """Renderiza a aba de depósito com design moderno usando classes CSS"""    
    st.markdown("""
        <div class="section-header">
            <div class="section-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="hsl(11, 100%, 60%)" stroke-width="2">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <polyline points="19 12 12 19 5 12"></polyline>
                </svg>
            </div>
            <h2 style="margin: 0;">Depositar na Carteira</h2>
        </div>
    """, unsafe_allow_html=True)
    
    render_feature_cards_deposit()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form("deposit_form", clear_on_submit=True):
        amount_to_deposit = st.number_input(
            "Valor do depósito (R$)", 
            min_value=5.0, 
            step=5.0, 
            format="%.2f",
            help="Valor mínimo: R$ 5,00"
        )
        
        submitted = st.form_submit_button(" Gerar Link de Pagamento", use_container_width=True)

        if submitted:
            with st.spinner("Gerando link de pagamento seguro..."):
                preference = payment_service.create_payment_preference(
                    username=username,
                    user_id=user_id,
                    amount=amount_to_deposit
                )
                
            if preference:
                payment_link = preference.get("init_point")
                if payment_link:
                    st.success("✓ Link de pagamento gerado com sucesso!")
                    st.link_button(
                        "💳 Pagar com Mercado Pago", 
                        payment_link, 
                        use_container_width=True
                    )
                else:
                    st.error("✕ Erro ao gerar link de pagamento.")
            else:
                st.error("✕ Houve um erro ao se comunicar com o Mercado Pago.")

def render_withdraw_tab(user_id, balance):
    """Renderiza a aba de saque com design moderno usando classes CSS"""
    
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="section-header">
            <div class="section-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="hsl(11, 100%, 60%)" stroke-width="2">
                    <line x1="12" y1="19" x2="12" y2="5"></line>
                    <polyline points="5 12 12 5 19 12"></polyline>
                </svg>
            </div>
            <h2 style="margin: 0;">Sacar da Carteira</h2>
        </div>
    """, unsafe_allow_html=True)
    
    render_feature_cards_withdraw()
    
    st.markdown('</div>', unsafe_allow_html=True)

    with st.form("withdraw_form"):
        amount_to_withdraw = st.number_input(
            "Valor do saque (R$)", 
            min_value=10.0, 
            step=5.0, 
            format="%.2f",
            help="Valor mínimo: R$ 10,00"
        )
        
        # --- ATUALIZAÇÃO 1: SELETOR PARA O TIPO DE CHAVE ---
        pix_key_type_display = st.selectbox(
            "Tipo de Chave Pix",
            options=["CPF", "E-mail", "Celular", "Chave Aleatória"],
            index=0,
            help="Selecione o tipo de chave PIX que você vai informar abaixo."
        )
        
        pix_key = st.text_input(
            "Sua chave Pix",
            placeholder="Digite sua chave PIX",
            help="Insira a chave PIX correspondente ao tipo selecionado acima."
        )
        
        withdraw_submitted = st.form_submit_button(" Solicitar Saque", use_container_width=True)

        if withdraw_submitted:
            
            # --- ATUALIZAÇÃO 2: MAPEAR O TIPO DE CHAVE E CRIAR DESCRIÇÃO ---
            # Mapeia o nome amigável para o valor da API do Mercado Pago
            api_key_type_map = {
                "CPF": "CPF",
                "E-mail": "EMAIL",
                "Celular": "PHONE",
                "Chave Aleatória": "RANDOM_KEY"
            }
            api_pix_key_type = api_key_type_map[pix_key_type_display]
            
            # Cria uma descrição padrão para o saque
            description_for_mp = f"Saque Wyden365 - Usuário {st.session_state['username']}"
            
            # Validações
            if not pix_key:
                st.warning("⚠ Por favor, insira sua chave Pix.")
            elif amount_to_withdraw > balance:
                try:
                    formatted_balance = locale.currency(balance, grouping=True, symbol='R$')
                except Exception:
                    formatted_balance = f"R$ {balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                st.error(f"✕ Saldo insuficiente. Você tem {formatted_balance} disponível.")
            else:
                # Processamento do saque
                with st.spinner("Processando sua solicitação de saque..."):
                    
                    # --- ATUALIZAÇÃO 3: CHAMADA DE FUNÇÃO CORRETA ---
                    response = payment_service.process_withdrawal(
                        user_id=user_id, 
                        amount=amount_to_withdraw, 
                        pix_key=pix_key,
                        pix_key_type=api_pix_key_type, # Novo argumento
                        description=description_for_mp   # Novo argumento
                    )
                
                if response["success"]:
                    # Debita o valor do saldo
                    user_service.update_user_balance(user_id, -amount_to_withdraw)
                    st.success(f"✓ {response['message']}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"✕ {response['message']}")

def render():
    """Função principal de renderização da página de carteira"""
    
    load_wallet_styles()
    
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("✕ Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    render_header()
    
    user_id = st.session_state['user_id']
    username = st.session_state['username']
    
    balance = user_service.get_user_balance(user_id)
    
    if balance is not None:
        render_balance_card(balance)
    else:
        st.error("✕ Não foi possível carregar seu saldo.")
        balance = 0.0
    
    tab_deposit, tab_withdraw = st.tabs([" Depositar", " Sacar"])

    with tab_deposit:
        render_deposit_tab(username, user_id)

    with tab_withdraw:
        render_withdraw_tab(user_id, balance)
