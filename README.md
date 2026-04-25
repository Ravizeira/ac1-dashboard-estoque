--------------------------------------------------------------------------------
# Painel de Giro de Estoque - AC1 + AC2 (Análise de Dados, BI e Relatórios)
--------------------------------------------------------------------------------

Este projeto é a entrega evolutiva da **Avaliação Continuada (AC1 + AC2)** da disciplina de Construção de Software. Trata-se de um sistema Full-Stack com foco em **Business Intelligence, Análise de Dados e Relatórios Gerenciais**, operando nas 3 camadas exigidas (Front-end, Back-end e Banco de Dados Relacional).

## Arquitetura do Sistema (3 Camadas)
* **Front-end & Back-end:** Desenvolvido em **Python 3** utilizando o framework **Streamlit** para renderização reativa de telas e dashboards dinâmicos.
* **Integração / ORM:** Leitura, gravação e manipulação dos dados feitas com **SQLAlchemy** e **Pandas**.
* **Banco de Dados:** **PostgreSQL** (SGBD Relacional) garantindo a persistência real dos dados gerados.

## Origem dos Dados
Em conformidade com as regras de projetos de BI da disciplina, declaramos que **os dados apresentados neste painel não são sigilosos**. Tratam-se de dados fictícios gerados e armazenados pela própria aplicação no banco PostgreSQL durante a demonstração de uso do sistema.

## Funcionalidades Entregues nesta Sprint
O sistema foi desenhado para gerenciar e analisar produtos, vendas e a saúde do giro de estoque:

1. **Dashboard de BI (Análise de Dados Dinâmica):**
   * Cálculo automático do **Giro de Estoque** (`quantidade_vendida` / `estoque_atual`).
   * Gráfico comparativo reativo: *Vendas vs. Produtos em Estoque*.
   * **Alerta Inteligente:** Filtro automático destacando na tela produtos com estoque crítico (abaixo de 5 unidades) que necessitam de reposição imediata.
2. **Cadastro de Novo Produto:** Inserção direta de novos itens no banco de dados via formulário.
3. **Atualização de Estoque:** Simulação de movimentação para atualizar os cálculos dinâmicos do BI em tempo real.
4. **AC2 - Módulo de Relatórios em PDF:** Geração de relatório gerencial com resumo executivo, top produtos por giro e alertas de estoque crítico, com download direto pelo dashboard.

## Documentação da AC2 — Módulo de Relatórios em PDF

### Objetivo da entrega
Implementar uma funcionalidade inédita para a AC2, conectada ao mesmo fluxo full-stack já existente (Streamlit + SQLAlchemy + PostgreSQL), gerando valor analítico para tomada de decisão.

### O que foi implementado
1. **Nova aba no dashboard:** `🧾 Relatórios PDF (AC2)`.
2. **Geração de relatório gerencial em PDF** com dados lidos diretamente do banco.
3. **Filtro opcional para estoque crítico** (`quantidade_estoque_atual < 5`) antes da geração.
4. **Download do arquivo PDF** diretamente pela interface do Streamlit.

### Conteúdo do relatório gerado
* Data/hora de geração.
* Resumo executivo:
  * quantidade de produtos analisados;
  * total em estoque (unidades);
  * total vendido (unidades);
  * valor total estimado em estoque;
  * total de itens em alerta.
* Top 5 produtos por giro de estoque.
* Lista de produtos em estoque crítico.

### Arquivos alterados na AC2
* `app.py`: lógica de geração do PDF e nova aba de relatórios.
* `requirements.txt`: inclusão da dependência `fpdf2`.
* `README.md`: atualização de documentação da AC2.
* `gerar_pdf.py`: remoção da instalação dinâmica de pacote em tempo de execução.

### Como demonstrar a AC2
1. Execute: `streamlit run app.py`
2. Acesse a aba **Relatórios PDF (AC2)**.
3. (Opcional) Marque o filtro de estoque crítico.
4. Clique em **Gerar arquivo PDF**.
5. Clique em **Baixar Relatório PDF** e abra o arquivo para validar o conteúdo.

## Estrutura do Banco de Dados (`produtos_estoque`)
| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | SERIAL (PK) | Identificador único do produto |
| `nome_produto` | VARCHAR(255) | Nome descritivo |
| `quantidade_estoque_atual` | INT | Estoque corrente (Default: 0) |
| `quantidade_vendida_total` | INT | Quantidade faturada (Default: 0) |
| `valor_unitario` | NUMERIC(10,2) | Preço base |

## Como executar este projeto localmente

### 1. Preparando o Banco de Dados (PostgreSQL)
Crie um banco de dados vazio chamado `estoque_db` e execute o script SQL abaixo:
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
Clone este repositório e instale as dependências:
```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/ac1-dashboard-estoque.git
cd ac1-dashboard-estoque

# Ative um ambiente virtual (Recomendado)
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

# Instale os pacotes principais
pip install streamlit pandas sqlalchemy psycopg2-binary fpdf2
```

### 3. Variáveis de Ambiente e Execução
Configure suas credenciais de banco de dados no terminal antes de rodar (exemplo em PowerShell):
```powershell
$env:DB_TYPE='postgresql'
$env:DB_USER='postgres'
$env:DB_PASS='sua_senha_aqui'
$env:DB_HOST='localhost'
$env:DB_PORT='5432'
$env:DB_NAME='estoque_db'

# Execute a aplicação
streamlit run app.py
```
O dashboard ficará disponível em `http://localhost:8501`.
