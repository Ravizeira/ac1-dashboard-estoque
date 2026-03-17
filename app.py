import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
import urllib.parse

# Configuração da página Streamlit
st.set_page_config(page_title="Painel de Giro de Estoque - AC1", layout="wide")

# ==========================================
# Configuração e Conexão com Banco de Dados
# ==========================================
# Utilizamos @st.cache_resource para evitar criar múltiplas conexões com o banco de dados
@st.cache_resource
def init_connection():
    # As credenciais são lidas de variáveis de ambiente por segurança.
    # Exigência do Projeto AC1: Utilizar Banco Real (PostgreSQL/MySQL), não SQLite!
    db_type = os.getenv("DB_TYPE", "postgresql") # Para MySQL mude a env var para: mysql+mysqlconnector ou pymysql
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "102010gu")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432") # Padrão Postgres (Use 3306 se for MySQL)
    db_name = os.getenv("DB_NAME", "estoque_db")
    
    db_pass_encoded = urllib.parse.quote_plus(db_pass)
    # URL de Conexão com SQLAlchemy
    db_url = f"{db_type}://{db_user}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}"
    
    # Cria a engine de conexão com o banco
    engine = create_engine(db_url)
    return engine

engine = init_connection()

# ==========================================
# Lógica de Consulta e Regras de Negócio
# ==========================================
def load_data():
    query = "SELECT * FROM produtos_estoque"
    # Fazendo a leitura baseada no backend SQL diretamente para um DataFrame Pandas
    df = pd.read_sql(query, engine)
    return df

def add_product(nome, qtd_estoque, qtd_vendida, valor):
    query = text("""
        INSERT INTO produtos_estoque (nome_produto, quantidade_estoque_atual, quantidade_vendida_total, valor_unitario)
        VALUES (:nome, :qtd_estoque, :qtd_vendida, :valor)
    """)
    with engine.begin() as conn:
        conn.execute(query, {
            "nome": nome, 
            "qtd_estoque": qtd_estoque,
            "qtd_vendida": qtd_vendida,
            "valor": valor
        })

def update_stock(produto_id, quantidade_adicional):
    query = text("""
        UPDATE produtos_estoque 
        SET quantidade_estoque_atual = quantidade_estoque_atual + :qtd_adicional
        WHERE id = :id
    """)
    with engine.begin() as conn:
        conn.execute(query, {"qtd_adicional": quantidade_adicional, "id": int(produto_id)})

# ==========================================
# UI: Front-end (Dashboard e CRUD)
# ==========================================
st.title("📦 Painel de Giro de Estoque - AC1")

tab_dashboard, tab_cadastrar, tab_atualizar = st.tabs(["📊 Dashboard de BI", "➕ Novo Produto", "🔄 Atualizar Estoque"])

try:
    df = load_data()
    
    # ABA 1: DASHBOARD
    with tab_dashboard:
        if st.button("🔄 Atualizar Dados"):
            st.cache_data.clear()
            st.rerun()

        if not df.empty:
            # Lógica Backend (Cálculos de negócio)
            df['giro_estoque'] = df['quantidade_vendida_total'] / df['quantidade_estoque_atual'].replace(0, 1)
            
            # UI: Métricas Principais
            total_estoque = df['quantidade_estoque_atual'].sum()
            total_vendas = df['quantidade_vendida_total'].sum()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total de Produtos em Estoque", int(total_estoque))
            with col2:
                st.metric("Total de Vendas", int(total_vendas))
                
            st.divider()
            
            # Gráfico Comparativo
            st.subheader("📊 Quantidade em Estoque vs Quantidade Vendida")
            chart_data = df[['nome_produto', 'quantidade_estoque_atual', 'quantidade_vendida_total']].set_index('nome_produto')
            st.bar_chart(chart_data)
            
            st.divider()
            
            # Alertas
            st.subheader("⚠️ Alertas de Reposição (Estoque Abaixo de 5 unidades)")
            alertas = df[df['quantidade_estoque_atual'] < 5]
            
            if not alertas.empty:
                st.dataframe(
                    alertas[['nome_produto', 'quantidade_estoque_atual', 'quantidade_vendida_total', 'giro_estoque']].style.format({'giro_estoque': '{:.2f}'}),
                    use_container_width=True
                )
            else:
                st.success("Tudo certo! Nenhum produto precisa de reposição no momento.")
                
            st.divider()
            st.subheader("📋 Tabela Completa de Produtos e Giro de Estoque")
            st.dataframe(
                df[['id', 'nome_produto', 'quantidade_estoque_atual', 'quantidade_vendida_total', 'giro_estoque', 'valor_unitario']].style.format({
                    'giro_estoque': '{:.2f}',
                    'valor_unitario': 'R$ {:.2f}'
                }),
                use_container_width=True
            )
        else:
            st.warning("Nenhum dado encontrado na tabela 'produtos_estoque'.")

    # ABA 2: CADASTRAR PRODUTO
    with tab_cadastrar:
        st.subheader("Cadastrar Novo Produto")
        with st.form("form_novo_produto"):
            nome_input = st.text_input("Nome do Produto")
            col1, col2 = st.columns(2)
            with col1:
                estoque_input = st.number_input("Quantidade Inicial em Estoque", min_value=0, step=1, value=0)
                vendas_input = st.number_input("Quantidade Vendida (Opcional)", min_value=0, step=1, value=0)
            with col2:
                valor_input = st.number_input("Valor Unitário (R$)", min_value=0.0, step=0.01, value=0.00, format="%.2f")
            
            submit_novo = st.form_submit_button("💾 Cadastrar Produto")
            
            if submit_novo:
                if nome_input.strip() == "":
                    st.error("O nome do produto é obrigatório!")
                else:
                    try:
                        add_product(nome_input, estoque_input, vendas_input, valor_input)
                        st.success(f"Produto '{nome_input}' cadastrado com sucesso no banco de dados!")
                        # Opcional: Adicionar um botão auxiliar para limpar cache ou instruir reload
                        st.info("Acesse a aba 'Dashboard de BI' e clique em 'Atualizar Dados' para ver as mudanças.")
                    except Exception as e:
                        st.error(f"Erro ao cadastrar: {e}")

    # ABA 3: ATUALIZAR ESTOQUE
    with tab_atualizar:
        st.subheader("Dar Entrada no Estoque")
        if not df.empty:
            with st.form("form_att_estoque"):
                # Cria um dicionário mapeando "Nome do Produto" para "ID"
                opcoes_produtos = dict(zip(df['nome_produto'], df['id']))
                produto_selecionado = st.selectbox("Selecione o Produto", options=list(opcoes_produtos.keys()))
                
                qtd_entrada = st.number_input("Quantidade a Adicionar", min_value=1, step=1, value=1)
                
                submit_entrada = st.form_submit_button("📦 Adicionar ao Estoque")
                
                if submit_entrada:
                    id_alvo = opcoes_produtos[produto_selecionado]
                    try:
                        update_stock(id_alvo, qtd_entrada)
                        st.success(f"Foram adicionadas {qtd_entrada} unidades ao estoque de '{produto_selecionado}'.")
                        st.info("Acesse a aba 'Dashboard de BI' e clique em 'Atualizar Dados' para ver as mudanças.")
                    except Exception as e:
                        st.error(f"Erro ao atualizar o estoque: {e}")
        else:
            st.warning("Não há produtos cadastrados para atualizar o estoque.")



except Exception as e:
    st.error(f"Erro de Conexão/Execução com o Banco de Dados.")
    st.error(f"Detalhes do erro: {e}")
    st.info("Para resolver: \n\n"
            "1. Garanta que seu Banco de Dados (MySQL ou PostgreSQL) está rodando.\n"
            "2. Execute o script `estrutura_dados.sql` para criar e popular a tabela.\n"
            "3. Configure as variáveis de ambiente antes de executar o Streamlit.\n\n"
            "**Exemplo via PowerShell (Windows)**:\n\n"
            "`$env:DB_USER='seu_usuario'`\n\n"
            "`$env:DB_PASS='sua_senha'`\n\n"
            "`$env:DB_NAME='seu_banco'`\n\n"
            "`$env:DB_TYPE='postgresql' # ou 'mysql+mysqlconnector'`\n\n"
            "`streamlit run app.py`")
