# Painel de Giro de Estoque - AC1

Este projeto é a entrega da **Avaliação Continuada 1 (AC1)**, que consiste em um sistema Full-Stack (3 camadas: Front-end, Back-end e Banco de Dados) focado em **Análise de Dados e BI**.

A aplicação foi desenvolvida em **Python + Streamlit** no front-end, e utiliza o banco de dados relacional **PostgreSQL** para o armazenamento persistente dos dados de estoque.

## 🚀 Funcionalidades do Projeto

O sistema foi desenhado para gerenciar e analisar produtos, vendas e giro de estoque:

*   **📊 Dashboard de BI (Análise de Dados):**
    *   Cálculo automático do Giro de Estoque (`quantidade_vendida / estoque_atual`).
    *   Métricas totais de mercado.
    *   Gráfico comparativo de vendas x produtos em estoque.
    *   **Sistema de Alertas Inteligente:** Filtra e exibe automaticamente na tela produtos com estoque crítico (abaixo de 5 unidades) que necessitam de reposição.
*   **➕ Cadastro de Novo Produto:** Insere diretamente no banco Postgres via SQLAlchemy.
*   **🔄 Atualização de Estoque:** Adiciona entrada de produtos existentes para simular movimentação e atualizar os cálculos dinâmicos do BI em tempo real.

## 🛠️ Tecnologias Utilizadas (3 Camadas)

*   **Front-end & Back-end:** Python 3 + [Streamlit](https://streamlit.io/) (Renderização reativa).
*   **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/) (SGBD Relacional exigido na AC1).
*   **Integração/ORM:** SQLAlchemy + Pandas (Leitura e gravação de dados).

## 🗃️ Estrutura do Banco de Dados

Tabela principal: `produtos_estoque`
*   `id`: Identificador único (Primary Key)
*   `nome_produto`: Nome descritivo (String)
*   `quantidade_estoque_atual`: Estoque corrente (Int)
*   `quantidade_vendida_total`: Quantidade já faturada (Int)
*   `valor_unitario`: Preço base (Float)

## ⚙️ Como executar este projeto localmente

Para rodar este dashboard, você precisa ter o Python e o PostgreSQL instalados na sua máquina.

### 1. Preparando o Banco de Dados (PostgreSQL)
Abra seu gerenciador de banco (ex: PgAdmin ou DBeaver), crie um banco de dados vazio chamado `estoque_db` e rode o script SQL para arquitetar a tabela base:

```sql
CREATE TABLE produtos_estoque (
    id SERIAL PRIMARY KEY,
    nome_produto VARCHAR(255) NOT NULL,
    quantidade_estoque_atual INT DEFAULT 0,
    quantidade_vendida_total INT DEFAULT 0,
    valor_unitario NUMERIC(10, 2) NOT NULL
);
```

### 2. Configurando o Ambiente Python
Clone este repositório e instale as dependências via terminal.
```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/ac1-dashboard-estoque.git
cd ac1-dashboard-estoque

# Ative um ambiente virtual (Opcional, mas recomendado)
python -m venv .venv
# (Windows): .venv\Scripts\activate
# (Mac/Linux): source .venv/bin/activate

# Instale os pacotes principais
pip install streamlit pandas sqlalchemy psycopg2-binary
```

### 3. Variáveis de Ambiente e Execução
O sistema utiliza variáveis de ambiente para segurança das credenciais (Regra do projeto). No PowerShell do Windows, defina as variáveis para o seu banco:

```powershell
$env:DB_TYPE='postgresql'
$env:DB_USER='postgres'
$env:DB_PASS='sua_senha_aqui'
$env:DB_HOST='localhost'
$env:DB_PORT='5432'
$env:DB_NAME='estoque_db'

# Após salvar as credenciais no terminal, rode o sistema:
streamlit run app.py
```

O dashboard ficará disponível em `http://localhost:8501`.

---
*Projeto acadêmico desenvolvido para composição de nota com foco em organização de projetos de software ágeis e arquitetura de 3 camadas.*
