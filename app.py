import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
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

# ==========================================
# UI: Front-end (Dashboard)
# ==========================================
st.title("📦 Painel de Giro de Estoque - AC1")

# Botão de Atualização de Dados que força um re-run da UI e da query.
if st.button("🔄 Atualizar Dados"):
    st.cache_data.clear()
    st.rerun()

try:
    # Carregamento
    df = load_data()
    
    if not df.empty:
        # Lógica Backend (Cálculos de negócio)
        # Giro de Estoque = Quantidade Vendida / Quantidade em Estoque
        # Tratamento de divisão por zero caso o estoque chegue a zero
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
        
        # Gráfico Comparativo: Estoque vs Vendas (Front-end)
        st.subheader("📊 Quantidade em Estoque vs Quantidade Vendida")
        
        # Preparando os dados para o st.bar_chart
        chart_data = df[['nome_produto', 'quantidade_estoque_atual', 'quantidade_vendida_total']].set_index('nome_produto')
        st.bar_chart(chart_data)
        
        st.divider()
        
        # Identificação de Alertas (Regra: Estoque menor que 5)
        st.subheader("⚠️ Alertas de Reposição (Estoque Abaixo de 5 unidades)")
        alertas = df[df['quantidade_estoque_atual'] < 5]
        
        if not alertas.empty:
            # Exibe a tabela formatada dando foco do alerta
            st.dataframe(
                alertas[['nome_produto', 'quantidade_estoque_atual', 'quantidade_vendida_total', 'giro_estoque']].style.format({'giro_estoque': '{:.2f}'}),
                use_container_width=True
            )
        else:
            st.success("Tudo certo! Nenhum produto precisa de reposição no momento.")
            
        st.divider()
        st.subheader("📋 Tabela Completa de Produtos e Giro de Estoque")
        st.dataframe(
            df[['nome_produto', 'quantidade_estoque_atual', 'quantidade_vendida_total', 'giro_estoque', 'valor_unitario']].style.format({
                'giro_estoque': '{:.2f}',
                'valor_unitario': 'R$ {:.2f}'
            }),
            use_container_width=True
        )

    else:
        st.warning("Nenhum dado encontrado na tabela 'produtos_estoque'.")

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
