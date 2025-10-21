# Wyden365 🏆

## Visão Geral do Projeto

O Wyden365 é uma aplicação web interativa desenvolvida com **Streamlit** que simula uma plataforma de apostas. Ele oferece funcionalidades de autenticação de usuário, gestão de carteira, registro e acompanhamento de apostas, além de uma área administrativa para controle da plataforma. A aplicação utiliza **Supabase** como backend para gerenciamento de banco de dados e autenticação, garantindo uma experiência segura e escalável.

## Funcionalidades Principais

*   **Autenticação de Usuário**: Sistema completo de login e registro com e-mail e senha, gerenciado pelo Supabase Auth.
*   **Navegação Intuitiva**: Interface de usuário amigável com um menu de opções horizontal para fácil acesso às diferentes seções da aplicação.
*   **Apostas**: Seção dedicada onde os usuários podem realizar suas apostas.
*   **Minhas Apostas**: Visualização e acompanhamento das apostas realizadas pelo usuário.
*   **Carteira**: Gestão de fundos do usuário, com provável integração de pagamentos via **Mercado Pago**.
*   **Painel Administrativo**: Área restrita para administradores com funcionalidades de gestão da plataforma.
*   **Backend Robusto**: Utiliza **Flask** e possivelmente **webhooks** para processamento em segundo plano, como integração com Mercado Pago.

## Tecnologias Utilizadas

O projeto Wyden365 é construído com as seguintes tecnologias:

*   **Streamlit**: Framework Python para criação rápida de aplicações web interativas.
*   **Streamlit-Option-Menu**: Componente para menus de navegação estilizados no Streamlit.
*   **Supabase**: Plataforma de backend como serviço (BaaS) que oferece banco de dados PostgreSQL, autenticação, armazenamento e APIs em tempo real.
*   **psycopg2-binary**: Adaptador PostgreSQL para Python, utilizado para conexão com o banco de dados Supabase.
*   **Mercado Pago**: Plataforma de pagamentos online, integrada para transações financeiras na carteira do usuário.
*   **Pydantic**: Biblioteca para validação de dados e configurações.
*   **Flask**: Microframework web Python, possivelmente utilizado para lidar com webhooks ou APIs específicas.
*   **python-dotenv**: Para gerenciar variáveis de ambiente de forma segura.

## Estrutura do Projeto

```
Wyden365/
├── core/                  # Módulos principais da aplicação (ex: db.py, user_service.py)
├── models.py              # Definições de modelos de dados (se houver)
├── views/                 # Páginas/Módulos da aplicação (ex: apostar.py, carteira.py, admin.py)
├── webhook_server/        # Possível servidor de webhook (ex: para Mercado Pago)
├── Wyden365.py            # Ponto de entrada principal da aplicação Streamlit
├── requirements.txt       # Dependências do projeto
├── README.md              # Este arquivo
```

## Como Executar o Projeto Localmente

Para configurar e executar o Wyden365 em sua máquina local, siga os passos abaixo:

### Pré-requisitos

Certifique-se de ter o Python 3.8+ instalado em seu sistema.

### 1. Clonar o Repositório

```bash
git clone https://github.com/DevCordeirocf/Wyden365.git
cd Wyden365
```

### 2. Criar e Ativar um Ambiente Virtual

É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto.

```bash
python -m venv venv
source venv/bin/activate  # No Windows: .\venv\Scripts\activate
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (`Wyden365/.env`) e adicione suas credenciais do Supabase e Mercado Pago. Exemplo:

```dotenv
SUPABASE_URL="SUA_URL_SUPABASE"
SUPABASE_KEY="SUA_CHAVE_ANON_SUPABASE"
MERCADOPAGO_ACCESS_TOKEN="SEU_ACCESS_TOKEN_MERCADOPAGO"
```

### 5. Executar a Aplicação Streamlit

```bash
streamlit run Wyden365.py
```

A aplicação será aberta automaticamente no seu navegador padrão. Se não, acesse `http://localhost:8501`.

### 6. Executar o Servidor de Webhook (se aplicável)

Se o projeto incluir um servidor de webhook (ex: para Mercado Pago), navegue até o diretório `webhook_server` e execute-o. (Assumindo que `app.py` seja o arquivo principal do webhook).

```bash
cd webhook_server
python app.py # Ou o comando de execução apropriado para seu webhook server
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a licença [MIT](https://opensource.org/licenses/MIT).
