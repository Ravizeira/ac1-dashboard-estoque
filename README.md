--------------------------------------------------------------------------------
# Painel de Giro de Estoque - AC1 + AC2 + AC3 + Parte Final (BI, Relatórios, Movimentações e Reposição)
--------------------------------------------------------------------------------

Este projeto é a entrega evolutiva da **Avaliação Continuada (AC1 + AC2 + AC3 + Parte Final)** da disciplina de Construção de Software. Trata-se de um sistema Full-Stack com foco em **Business Intelligence, Análise de Dados e Relatórios Gerenciais**, operando nas 3 camadas exigidas (Front-end, Back-end e Banco de Dados Relacional).

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
3. **Movimentações de Estoque (Entrada/Saída):** Registro operacional de entradas e saídas com atualização de saldo e vendas para manter os indicadores de BI consistentes.
4. **AC2 - Módulo de Relatórios em PDF:** Geração de relatório gerencial com resumo executivo, top produtos por giro e alertas de estoque crítico, com download direto pelo dashboard.
5. **AC3 - Movimentações com Histórico:** Registro de entrada/saída com atualização automática do saldo e trilha de auditoria das últimas movimentações.
6. **Parte Final - Reposição Inteligente:** cálculo de sugestão de compra por produto, com persistência do plano no banco e visualização do volume recomendado.

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

## Documentação da AC3 — Movimentações com Histórico

### Objetivo da entrega
Implementar uma funcionalidade inédita para AC3 com fatiamento vertical completo (UI + regra de negócio + persistência), permitindo rastrear operações de estoque com auditabilidade.

### O que foi implementado
1. **Nova aba no dashboard:** `🔄 Movimentações (AC3)`.
2. **Registro de entrada e saída** por produto com quantidade e observação opcional.
3. **Validação de regra de negócio:** bloqueio de saída quando a quantidade solicitada excede o estoque disponível.
4. **Atualização automática no banco:**
   * `ENTRADA`: incrementa `quantidade_estoque_atual`;
   * `SAIDA`: decrementa `quantidade_estoque_atual` e incrementa `quantidade_vendida_total`.
5. **Histórico de movimentações:** listagem das últimas movimentações registradas.

### Persistência e modelo relacional da AC3
As movimentações ficam registradas na tabela `movimentacoes_estoque`, relacionada a `produtos_estoque` por chave estrangeira (`produto_id`), garantindo trilha de auditoria.

### Arquivos alterados na AC3
* `app.py`: criação da aba AC3, regra transacional de movimentação e consulta de histórico.
* `setup_db.py`: criação da tabela `movimentacoes_estoque` no setup inicial.
* `estrutura_dados.sql`: inclusão da estrutura SQL da nova tabela relacional.
* `README.md`: documentação da funcionalidade AC3.

### Como demonstrar a AC3
1. Execute: `streamlit run app.py`
2. Acesse a aba **Movimentações (AC3)**.
3. Selecione um produto e registre uma **ENTRADA**.
4. Registre uma **SAÍDA** válida para o mesmo produto.
5. Tente registrar uma saída maior que o estoque para demonstrar a validação de regra.
6. Mostre o **Histórico de Movimentações** na mesma aba.
7. Vá para **Dashboard de BI** e clique em **Atualizar Dados** para evidenciar os reflexos nos indicadores.

## Documentação da Parte Final — Reposição Inteligente

### Objetivo da entrega
Implementar uma funcionalidade inédita para a parte final do projeto, conectada ao fluxo já existente, gerando uma nova análise de reposição com persistência em banco.

### O que foi implementado
1. **Nova aba no dashboard:** `📦 Reposição Inteligente`.
2. **Cálculo de sugestão de compra** por produto com base em estoque e vendas acumuladas.
3. **Persistência do plano gerado** na tabela `reposicoes_inteligentes`.
4. **Visualização analítica** com métricas, gráfico e tabela do plano salvo.

### Regra adotada
* Estoque mínimo recomendado = maior entre 5 unidades e 10% das vendas acumuladas.
* Estoque meta = maior entre 10 unidades e 30% das vendas acumuladas.
* Quantidade sugerida = diferença entre a meta e o estoque atual, limitada a zero quando não houver necessidade de compra.

### Arquivos alterados na Parte Final
* `app.py`: criação da aba de reposição inteligente, regra de cálculo e persistência do plano.
* `setup_db.py`: criação da tabela `reposicoes_inteligentes`.
* `estrutura_dados.sql`: inclusão da nova tabela relacional.
* `README.md`: documentação da funcionalidade final.

### Como demonstrar a Parte Final
1. Execute: `streamlit run app.py`
2. Acesse a aba **Reposição Inteligente**.
3. Clique em **Gerar Plano de Reposição**.
4. Mostre as métricas, o gráfico e a tabela com o plano salvo no banco.

## Estrutura do Banco de Dados

### Tabela `produtos_estoque`
| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | SERIAL (PK) | Identificador único do produto |
| `nome_produto` | VARCHAR(255) | Nome descritivo |
| `quantidade_estoque_atual` | INT | Estoque corrente (Default: 0) |
| `quantidade_vendida_total` | INT | Quantidade faturada (Default: 0) |
| `valor_unitario` | NUMERIC(10,2) | Preço base |

### Tabela `movimentacoes_estoque`
| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | SERIAL (PK) | Identificador da movimentação |
| `produto_id` | INT (FK) | Produto movimentado (`produtos_estoque.id`) |
| `tipo_movimentacao` | VARCHAR(10) | Tipo (`ENTRADA` ou `SAIDA`) |
| `quantidade` | INT | Quantidade movimentada (> 0) |
| `observacao` | VARCHAR(255) | Observação opcional |
| `data_movimentacao` | TIMESTAMP | Data/hora do registro |

### Tabela `reposicoes_inteligentes`
| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | SERIAL (PK) | Identificador da sugestão |
| `produto_id` | INT (FK) | Produto analisado (`produtos_estoque.id`) |
| `estoque_atual` | INT | Saldo no momento do cálculo |
| `quantidade_vendida_total` | INT | Vendas acumuladas do produto |
| `estoque_minimo_recomendado` | INT | Limite mínimo calculado |
| `estoque_meta` | INT | Meta de estoque calculada |
| `quantidade_sugerida` | INT | Quantidade sugerida para compra |
| `prioridade` | VARCHAR(10) | Classificação (`ALTA`, `MEDIA`, `BAIXA`) |
| `motivo` | VARCHAR(255) | Justificativa da sugestão |
| `data_calculo` | TIMESTAMP | Data/hora do cálculo |
![[modelo_dados_logico.png]]


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

CREATE TABLE movimentacoes_estoque (
    id SERIAL PRIMARY KEY,
    produto_id INT NOT NULL REFERENCES produtos_estoque(id),
    tipo_movimentacao VARCHAR(10) NOT NULL CHECK (tipo_movimentacao IN ('ENTRADA', 'SAIDA')),
    quantidade INT NOT NULL CHECK (quantidade > 0),
    observacao VARCHAR(255),
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reposicoes_inteligentes (
    id SERIAL PRIMARY KEY,
    produto_id INT NOT NULL REFERENCES produtos_estoque(id),
    estoque_atual INT NOT NULL,
    quantidade_vendida_total INT NOT NULL,
    estoque_minimo_recomendado INT NOT NULL,
    estoque_meta INT NOT NULL,
    quantidade_sugerida INT NOT NULL,
    prioridade VARCHAR(10) NOT NULL CHECK (prioridade IN ('ALTA', 'MEDIA', 'BAIXA')),
    motivo VARCHAR(255),
    data_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
