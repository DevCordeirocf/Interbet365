> ⚠️ **Aviso Importante: Projeto Descontinuado**
> 
> Este repositório contém o código-fonte de um projeto desenvolvido para fins **estritamente acadêmicos**. O desenvolvimento foi **finalizado** e o projeto **não receberá mais atualizações ou manutenção**.

# InterBet 365 - Um Estudo de Caso em Streamlit e APIs

O InterBet 365 foi uma aplicação web funcional que simulava uma plataforma de apostas, criada como um trabalho prático para demonstrar habilidades em desenvolvimento de software, integração de APIs e gestão de sistemas web.

## Status do Projeto: Arquivado

O projeto foi concluído e está **arquivado**. A decisão de não dar continuidade ao desenvolvimento foi tomada devido à **natureza controversa do tema de apostas**, que pode ser mal interpretado. O código é mantido neste repositório exclusivamente como um registro de portfólio e para fins de consulta técnica.

**Este projeto não é um serviço comercial e não deve ser utilizado para fins de apostas reais.**

## Visão Geral da Arquitetura

A plataforma foi construída utilizando um conjunto de tecnologias modernas para criar uma experiência de usuário interativa e um backend robusto:

*   **Frontend e Interface do Usuário:** **Streamlit**, um framework Python que permite a criação rápida de aplicações web ricas em dados.
*   **Backend e Banco de Dados:** **Supabase**, uma alternativa open-source ao Firebase, que forneceu o banco de dados PostgreSQL, autenticação de usuários e APIs de acesso aos dados.
*   **Servidor de Notificações (Webhook):** Um microserviço construído com **Flask** para receber e processar notificações em tempo real, como a confirmação de pagamentos.
*   **Integração de Pagamentos:** A API do **Mercado Pago** foi utilizada para simular as transações de depósito e saque na carteira virtual dos usuários.

## Como Executar Localmente (Para Fins de Estudo)

Se você deseja analisar o código ou executá-lo em um ambiente local, siga os passos abaixo.

### 1. Clonar o Repositório

```bash
git clone https://github.com/DevCordeirocf/Interbet365.git
cd Interbet365
```

### 2. Instalar as Dependências

É altamente recomendado criar um ambiente virtual antes de instalar as dependências.

```bash
# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
# Ative o ambiente (Linux/macOS)
source venv/bin/activate
# No Windows: .\venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto (`Interbet365/.env`). Este arquivo centraliza todas as credenciais e configurações sensíveis. Preencha-o com suas próprias chaves de API:

```env
# Credenciais do Mercado Pago e Ambiente
# Mude para "prod" para usar as chaves de produção
ENVIRONMENT="test"
MP_ACCESS_TOKEN_TEST="SEU_TOKEN_DE_TESTE_DO_MERCADO_PAGO"
MP_ACCESS_TOKEN_PROD="SEU_TOKEN_DE_PRODUCAO_DO_MERCADO_PAGO"
MP_SELLER_EMAIL="SEU_EMAIL_DE_VENDEDOR_DO_MERCADO_PAGO"

# Credenciais do Supabase
SUPABASE_URL="SUA_URL_DO_PROJETO_SUPABASE"
SUPABASE_SERVICE_KEY="SUA_CHAVE_DE_SERVICO_(SERVICE_ROLE)_DO_SUPABASE"
```

### 4. Executar a Aplicação Principal

Com as dependências instaladas e o arquivo `.env` configurado, inicie a aplicação Streamlit:

```bash
streamlit run Wyden365.py
```

A aplicação estará disponível em `http://localhost:8501`.

### 5. Executar o Servidor de Webhook

Para que as notificações de pagamento funcionem, o servidor Flask precisa ser executado em um terminal separado. Você também precisará de uma ferramenta como o [ngrok](https://ngrok.com/) para expor sua porta local à internet e fornecer uma URL válida ao Mercado Pago.

```bash
# Em um novo terminal, navegue até a pasta do webhook
cd webhook_server

# Execute o servidor Flask
python app.py
```

---

Este README foi criado para contextualizar o estado atual do projeto e guiar desenvolvedores que queiram estudar o código-fonte. Qualquer uso fora do escopo acadêmico é desaconselhado.
