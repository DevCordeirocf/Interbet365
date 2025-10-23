# views/carteira.py - VERSÃO COMPLETA COM 3 ABAS
# (PIX Direto, Checkout Pro, Saque)

import streamlit as st
import locale
import time
from core import user_service, payment_service
from styles.wallet import load_wallet_styles

# Tenta configurar locale pt_BR
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except Exception:
    pass

# =============================================================================
# FUNÇÕES DE RENDERIZAÇÃO DE COMPONENTES
# (Funções que existiam no seu arquivo original)
# =============================================================================

def render_header():
    """Renderiza o header da página"""
    st.title("Minha Carteira")
    st.markdown('<p class="stSubheader">Gerencie seus depósitos e saques</p>', unsafe_allow_html=True)

def render_balance_card(balance):
    """Renderiza o card de saldo com design destacado"""
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
    """Renderiza os cards de features para depósito Checkout Pro"""
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
# ABA 1: DEPÓSITO PIX DIRETO (Seu novo código)
# =============================================================================

def render_pix_deposit_tab(username, user_id, user_email):
    """Renderiza a aba de depósito via PIX direto (sem Checkout Pro)"""
    
    st.markdown("""
        <div class="section-header">
            <div class="section-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="hsl(11, 100%, 60%)" stroke-width="2">
                    <rect x="2" y="5" width="20" height="14" rx="2"></rect>
                    <line x1="2" y1="10" x2="22" y2="10"></line>
                </svg>
            </div>
            <h2 style="margin: 0;">💳 Depósito via PIX</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Instantâneo</div>
                <div class="feature-desc">Crédito em segundos</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <div class="feature-title">Seguro</div>
                <div class="feature-desc">100% protegido</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <div class="feature-title">Simples</div>
                <div class="feature-desc">Pague pelo celular</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Verifica se já existe um PIX gerado na sessão
    if 'current_pix_payment' in st.session_state:
        display_pix_payment(st.session_state['current_pix_payment'])
    else:
        # Formulário para gerar PIX
        with st.form("pix_deposit_form"):
            st.markdown("### 💰 Quanto deseja depositar?")
            
            amount = st.number_input(
                "Valor (R$)",
                min_value=5.0,
                max_value=10000.0,
                value=50.0,
                step=5.0,
                format="%.2f",
                help="Valor mínimo: R$ 5,00"
            )
            
            st.markdown("### 📧 Dados do Pagamento (Obrigatórios)")
            
            email = st.text_input(
                "E-mail",
                value=user_email,
                placeholder="seu@email.com",
                help="E-mail para receber comprovante"
            )
            
            # --- CORREÇÃO DE BUG ---
            # CPF é obrigatório para a API, removemos o "(opcional)"
            cpf = st.text_input(
                "CPF (obrigatório)",
                placeholder="000.000.000-00",
                max_chars=14,
                help="Seu CPF é obrigatório para gerar o PIX"
            )
            
            submitted = st.form_submit_button("🔐 Gerar Código PIX", use_container_width=True)
            
            if submitted:
                # --- CORREÇÃO DE BUG ---
                # Adicionada verificação de CPF
                if not email or not cpf:
                    st.error("❌ Por favor, preencha seu e-mail e CPF.")
                elif amount < 5:
                    st.error("❌ O valor mínimo para depósito é R$ 5,00")
                else:
                    # Criar pagamento PIX
                    with st.spinner("🔄 Gerando código PIX..."):
                        pix_result = payment_service.create_pix_payment(
                            username=username,
                            user_id=user_id,
                            amount=amount,
                            email=email,
                            cpf=cpf # Passa o CPF que agora é obrigatório
                        )
                    
                    if pix_result and pix_result.get("success"):
                        st.session_state['current_pix_payment'] = pix_result
                        st.success("✅ PIX gerado com sucesso!")
                        time.sleep(0.5)
                        st.rerun()


def display_pix_payment(pix_data: dict):
    """Exibe o QR Code e informações do PIX gerado"""
    
    payment_id = pix_data.get('payment_id')
    qr_code = pix_data.get('qr_code')
    qr_code_base64 = pix_data.get('qr_code_base64')
    
    st.success("✅ PIX gerado com sucesso!")
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.15)); 
                    border: 2px solid rgba(16, 185, 129, 0.3); 
                    border-radius: 16px; 
                    padding: 2rem; 
                    margin: 1rem 0;">
            <h3 style="text-align: center; color: #10b981; margin-bottom: 1.5rem;">
                💳 Pague com PIX
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📱 Escaneie o QR Code")
        if qr_code_base64:
            st.image(
                f"data:image/png;base64,{qr_code_base64}",
                caption="Use o app do seu banco",
                width=250 # Tamanho fixo
            )
        else:
            st.warning("⚠️ QR Code não disponível")
    
    with col2:
        st.markdown("### 📋 Ou copie o código")
        if qr_code:
            st.text_area("PIX Copia e Cola", qr_code, height=250)
        else:
            st.error("❌ Código PIX não disponível")
    
    st.divider()
    st.info(f"**🆔 ID do Pagamento:** `{payment_id}` | **Status:** `{pix_data.get('status')}`")
    
    col_check, col_cancel = st.columns(2)
    
    if st.button("🔄 Verificar Pagamento", use_container_width=True, type="primary"):
        with st.spinner("🔍 Verificando pagamento..."):
            status_info = payment_service.check_pix_payment_status(payment_id)
            
            if status_info:
                if status_info['status'] == 'approved':
                    st.success("✅ Pagamento aprovado! Atualizando saldo...")
                    # Limpar sessão
                    del st.session_state['current_pix_payment']
                    time.sleep(2)
                    st.balloons()
                    st.rerun()
                elif status_info['status'] == 'pending':
                    st.warning("⏳ Pagamento ainda pendente. Aguardando confirmação...")
                elif status_info['status'] == 'rejected':
                    st.error("❌ Pagamento rejeitado. Tente novamente.")
                    del st.session_state['current_pix_payment']
                    time.sleep(1)
                    st.rerun()
                else:
                    st.info(f"ℹ️ Status: {status_info['status']}")
            else:
                st.error("❌ Erro ao verificar status. Tente novamente.")
    
    if st.button("❌ Cancelar", use_container_width=True):
        del st.session_state['current_pix_payment']
        st.rerun()

# =============================================================================
# ABA 2: DEPÓSITO CHECKOUT PRO (Seu código antigo)
# =============================================================================

def render_deposit_checkout_tab(username, user_id, user_email):
    """Renderiza a aba de depósito (Checkout Pro) com design moderno"""    
    st.markdown("""
        <div class="section-header">
            <div class="section-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="hsl(11, 100%, 60%)" stroke-width="2">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <polyline points="19 12 12 19 5 12"></polyline>
                </svg>
            </div>
            <h2 style="margin: 0;">🔗 Depósito via Checkout Pro</h2>
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
                preference = payment_service.create_payment_preference(
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
                        "💳 Pagar com Mercado Pago", 
                        payment_link, 
                        use_container_width=True
                    )
                else:
                    st.error("✕ Erro ao gerar link de pagamento.")
            else:
                st.error("✕ Houve um erro ao se comunicar com o Mercado Pago.")

# =============================================================================
# ABA 3: SAQUE (Seu código antigo)
# =============================================================================

def render_withdraw_tab(user_id, balance):
    """Renderiza a aba de saque com design moderno"""
    
    st.markdown("""
        <div class="section-header">
            <div class="section-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="hsl(11, 100%, 60%)" stroke-width="2">
                    <line x1="12" y1="19" x2="12" y2="5"></line>
                    <polyline points="5 12 12 5 19 12"></polyline>
                </svg>
            </div>
            <h2 style="margin: 0;">💸 Sacar da Carteira</h2>
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
                st.warning("⚠ Por favor, insira sua chave Pix.")
            elif amount_to_withdraw > balance:
                st.error(f"✕ Saldo insuficiente. Você tem {locale.currency(balance, grouping=True, symbol='R$')} disponível.")
            else:
                with st.spinner("Processando sua solicitação de saque..."):
                    description_for_mp = f"Saque Wyden365 - Usuário {user_id}"
                    
                    response = payment_service.process_withdrawal(
                        user_id=user_id,
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
    """Função principal de renderização da página de carteira"""
    
    load_wallet_styles()
    
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("✕ Acesso negado. Por favor, faça o login primeiro.")
        st.stop()
    
    render_header()
    
    user_id = st.session_state['user_id']
    username = st.session_state['username']
    user_email = st.session_state.get('email', '') # Pega o email da sessão
    
    balance = user_service.get_user_balance(user_id)
    
    if balance is not None:
        render_balance_card(balance)
    else:
        st.error("✕ Não foi possível carregar seu saldo.")
        balance = 0.0
    
    # --- ESTRUTURA DE ABAS ATUALIZADA ---
    tab_pix, tab_checkout, tab_withdraw = st.tabs([
        "💳 PIX Instantâneo", 
        "🔗 Checkout Pro", 
        "💸 Sacar"
    ])
    
    with tab_pix:
        render_pix_deposit_tab(username, user_id, user_email)
    
    with tab_checkout:
        render_deposit_checkout_tab(username, user_id, user_email)

    with tab_withdraw:
        render_withdraw_tab(user_id, balance)
