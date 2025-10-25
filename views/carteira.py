

import streamlit as st
import locale
import time
from core import user_service, payment, payout
from styles.wallet import load_wallet_styles

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except Exception:
    pass

# =============================================================================
# FUNÇÕES DE RENDERIZAÇÃO DE COMPONENTES
# =============================================================================

def render_header():
    st.title("Minha Carteira")
    st.markdown('<p class="stSubheader">Gerencie seus depósitos e saques</p>', unsafe_allow_html=True)

def render_balance_card(balance):
    try:
        formatted_balance = locale.currency(balance, grouping=True, symbol='R$')
    except Exception:
        formatted_balance = f"R$ {balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    st.markdown(f"""
        <div class="balance-card">
            <div class="balance-label">Saldo Disponível</div>
            <div class="balance-value">{formatted_balance}</div>
        </div>
    """, unsafe_allow_html=True)

def render_feature_cards_deposit():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">Múltiplos Métodos</div>
                <div class="feature-desc">Cartão, Boleto e mais</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">Seguro</div>
                <div class="feature-desc">Pagamento via Mercado Pago</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">Conveniente</div>
                <div class="feature-desc">Ambiente que você já conhece</div>
            </div>
        """, unsafe_allow_html=True)

def render_feature_cards_withdraw():
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
                <div class="feature-title">Seguro</div>
                <div class="feature-desc">Processamento seguro</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">Mínimo R$ 10</div>
                <div class="feature-desc">Valor mínimo</div>
            </div>
        """, unsafe_allow_html=True)

# =============================================================================
# ABA 1: DEPÓSITO PIX DIRETO
# =============================================================================

def render_pix_deposit_tab(username, user_id, user_email):
    
    st.markdown("""
        <div class="section-header">
            <h2 style="margin: 0;">Depósito via PIX</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
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
    
    st.divider()
    
    if 'current_pix_payment' in st.session_state:
        display_pix_payment(st.session_state['current_pix_payment'])
    else:
        with st.form("pix_deposit_form"):
            st.markdown("### Quanto deseja depositar?")
            
            amount = st.number_input(
                "Valor (R$)",
                min_value=5.0,
                max_value=10000.0,
                value=50.0,
                step=5.0,
                format="%.2f",
                help="Valor mínimo: R$ 5,00"
            )
            
            st.markdown("### Dados do Pagamento (Obrigatórios)")
            
            email = st.text_input(
                "E-mail",
                value=user_email,
                placeholder="seu@email.com",
                help="E-mail para receber comprovante"
            )
            
            cpf = st.text_input(
                "CPF (obrigatório)",
                placeholder="000.000.000-00",
                max_chars=14,
                help="Seu CPF é obrigatório para gerar o PIX"
            )
            
            submitted = st.form_submit_button(" Gerar Código PIX", use_container_width=True)
            
            if submitted:
                if not email or not cpf:
                    st.error("Por favor, preencha seu e-mail e CPF.")
                elif amount < 5:
                    st.error("O valor mínimo para depósito é R$ 5,00")
                else:
                    with st.spinner("Gerando código PIX..."):
                        pix_result = payment.create_pix_payment(
                            username=username,
                            user_id=user_id,
                            amount=amount,
                            email=email,
                            cpf=cpf 
                        )
                    
                    if pix_result and pix_result.get("success"):
                        st.session_state['current_pix_payment'] = pix_result
                        st.success("PIX gerado com sucesso!")
                        time.sleep(0.5)
                        st.rerun()


def display_pix_payment(pix_data: dict):
    
    payment_id = pix_data.get('payment_id')
    qr_code = pix_data.get('qr_code')
    qr_code_base64 = pix_data.get('qr_code_base64')
    
    st.success("PIX gerado com sucesso!")
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.15)); 
                    border: 2px solid rgba(16, 185, 129, 0.3); 
                    border-radius: 16px; 
                    padding: 2rem; 
                    margin: 1rem 0;">
            <h3 style="text-align: center; color: #10b981; margin-bottom: 1.5rem;">
                Pague com PIX
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Escaneie o QR Code")
        if qr_code_base64:
            st.image(
                f"data:image/png;base64,{qr_code_base64}",
                caption="Use o app do seu banco",
                width=250
            )
        else:
            st.warning("QR Code não disponível")
    
    with col2:
        st.markdown("### Ou copie o código")
        if qr_code:
            st.text_area("PIX Copia e Cola", qr_code, height=250)
        else:
            st.error("Código PIX não disponível")
    
    st.divider()
    st.info(f"**ID do Pagamento:** `{payment_id}` | **Status:** `{pix_data.get('status')}`")
    
    col_check, col_cancel = st.columns(2)
    
    if st.button("Verificar Pagamento", use_container_width=True, type="primary"):
        with st.spinner("Verificando pagamento..."):
            status_info = payment.check_pix_payment_status(payment_id)
            
            if status_info:
                if status_info['status'] == 'approved':
                    st.success("Pagamento aprovado! Atualizando saldo...")
                    del st.session_state['current_pix_payment']
                    time.sleep(2)
                    st.balloons()
                    st.rerun()
                elif status_info['status'] == 'pending':
                    st.warning("Pagamento ainda pendente. Aguardando confirmação...")
                elif status_info['status'] == 'rejected':
                    st.error("Pagamento rejeitado. Tente novamente.")
                    del st.session_state['current_pix_payment']
                    time.sleep(1)
                    st.rerun()
                else:
                    st.info(f"Status: {status_info['status']}")
            else:
                st.error("Erro ao verificar status. Tente novamente.")
    
    if st.button("Cancelar", use_container_width=True):
        del st.session_state['current_pix_payment']
        st.rerun()

# =============================================================================
# ABA 2: DEPÓSITO CHECKOUT PRO
# =============================================================================

def render_deposit_checkout_tab(username, user_id, user_email):
    st.markdown("""
        <div class="section-header">
            <div class="section-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="hsl(11, 100%, 60%)" stroke-width="2">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <polyline points="19 12 12 19 5 12"></polyline>
                </svg>
            </div>
            <h2 style="margin: 0;">Depósito via Checkout Pro</h2>
        </div>
    """, unsafe_allow_html=True)
    
    render_feature_cards_deposit()
    st.markdown("---")
    
    with st.form("deposit_form_checkout", clear_on_submit=True):
        amount_to_deposit = st.number_input(
            "Valor do depósito (R$)", 
            min_value=5.0, 
            step=5.0, 
            format="%.2f",
            help="Valor mínimo: R$ 5,00"
        )
        
        submitted = st.form_submit_button("Gerar Link de Pagamento", use_container_width=True)

        if submitted:
            with st.spinner("Gerando link de pagamento seguro..."):
                preference = payment.create_payment_preference(
                    username=username,
                    user_id=user_id,
                    user_email=user_email,
                    amount=amount_to_deposit
                )
                
            if preference:
                payment_link = preference.get("init_point")
                if payment_link:
                    st.success("✓ Link de pagamento gerado com sucesso!")
                    st.link_button(
                        "Pagar com Mercado Pago", 
                        payment_link, 
                        use_container_width=True
                    )
                else:
                    st.error("✕ Erro ao gerar link de pagamento.")
            else:
                st.error("✕ Houve um erro ao se comunicar com o Mercado Pago.")

# =============================================================================
# ABA 3: SAQUE
# =============================================================================

def render_withdraw_tab(user_id, balance):
    
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
    st.markdown("---")

    with st.form("withdraw_form"):
        amount_to_withdraw = st.number_input(
            "Valor do saque (R$)", 
            min_value=10.0, 
            step=5.0, 
            format="%.2f",
            help="Valor mínimo: R$ 10,00"
        )
        
        pix_key_type_display = {
            "CPF": "CPF",
            "CNPJ": "CNPJ",
            "Telefone": "PHONE",
            "E-mail": "EMAIL",
            "Chave Aleatória": "EVP"
        }
        pix_key_type_label = st.selectbox(
            "Tipo de chave Pix",
            options=pix_key_type_display.keys()
        )
        pix_key_type = pix_key_type_display[pix_key_type_label]
        
        pix_key = st.text_input(
            "Sua chave Pix",
            placeholder="Digite sua chave PIX",
            help="Insira uma chave PIX válida para receber o saque"
        )
        
        withdraw_submitted = st.form_submit_button("Solicitar Saque", use_container_width=True)

        if withdraw_submitted:
            if not pix_key:
                st.warning("Por favor, insira sua chave Pix.")
            elif amount_to_withdraw > balance:
                st.error(f"✕ Saldo insuficiente. Você tem {locale.currency(balance, grouping=True, symbol='R$')} disponível.")
            else:
                with st.spinner("Processando sua solicitação de saque..."):
                    description_for_mp = f"Saque InterBet 365 - Usuário {user_id}"
                    
                    response = payout.process_withdrawal(
                        user_id=str(user_id),
                        amount=amount_to_withdraw, 
                        pix_key=pix_key,
                        pix_key_type=pix_key_type,
                        description=description_for_mp
                    )
                
                if response["success"]:
                    user_service.update_user_balance(user_id, -amount_to_withdraw)
                    st.success(f"✓ {response['message']}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"✕ {response['message']}")

# =============================================================================
# FUNÇÃO PRINCIPAL (RENDER) - ATUALIZADA
# =============================================================================

def render():
    
    load_wallet_styles()
    
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    render_header()
    
    user_id = st.session_state['user_id']
    username = st.session_state['username']
    user_email = st.session_state.get('email', '') 
    
    balance = user_service.get_user_balance(user_id)
    
    if balance is not None:
        render_balance_card(balance)
    else:
        st.error("✕ Não foi possível carregar seu saldo.")
        balance = 0.0
    
    tab_pix, tab_checkout, tab_withdraw = st.tabs([
        "PIX Instantâneo", 
        "Checkout Pro", 
        "Sacar"
    ])
    
    with tab_pix:
        render_pix_deposit_tab(username, user_id, user_email)
    
    with tab_checkout:
        render_deposit_checkout_tab(username, user_id, user_email)

    with tab_withdraw:
        render_withdraw_tab(user_id, balance)

