import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
import urllib.parse
from datetime import datetime
from fpdf import FPDF

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


def _safe_pdf_text(texto):
    return str(texto).encode("latin-1", "replace").decode("latin-1")


def generate_pdf_report(df_relatorio):
    dados = df_relatorio.copy()
    dados["giro_estoque"] = dados["quantidade_vendida_total"] / dados["quantidade_estoque_atual"].replace(0, 1)
    dados["valor_total_estoque"] = dados["quantidade_estoque_atual"] * dados["valor_unitario"]

    total_itens = len(dados)
    total_estoque = int(dados["quantidade_estoque_atual"].sum())
    total_vendas = int(dados["quantidade_vendida_total"].sum())
    valor_total = float(dados["valor_total_estoque"].sum())
    alertas = dados[dados["quantidade_estoque_atual"] < 5]
    top_giro = dados.sort_values("giro_estoque", ascending=False).head(5)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 15)
    pdf.cell(0, 10, _safe_pdf_text("Relatório Gerencial de Estoque - AC2"), ln=1, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, _safe_pdf_text(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"), ln=1)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, _safe_pdf_text("Resumo Executivo"), ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, _safe_pdf_text(f"Produtos analisados: {total_itens}"), ln=1)
    pdf.cell(0, 7, _safe_pdf_text(f"Total em estoque (unidades): {total_estoque}"), ln=1)
    pdf.cell(0, 7, _safe_pdf_text(f"Total vendido (unidades): {total_vendas}"), ln=1)
    pdf.cell(0, 7, _safe_pdf_text(f"Valor estimado do estoque: R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")), ln=1)
    pdf.cell(0, 7, _safe_pdf_text(f"Itens em alerta de reposição (<5): {len(alertas)}"), ln=1)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, _safe_pdf_text("Top 5 Produtos por Giro de Estoque"), ln=1)
    pdf.set_font("Arial", "", 10)
    if top_giro.empty:
        pdf.cell(0, 7, _safe_pdf_text("Nenhum dado disponível para cálculo de giro."), ln=1)
    else:
        for _, item in top_giro.iterrows():
            linha = f"- {item['nome_produto']}: giro {item['giro_estoque']:.2f}"
            pdf.cell(0, 7, _safe_pdf_text(linha), ln=1)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, _safe_pdf_text("Produtos em Estoque Crítico"), ln=1)
    pdf.set_font("Arial", "", 10)
    if alertas.empty:
        pdf.cell(0, 7, _safe_pdf_text("Nenhum produto em estoque crítico."), ln=1)
    else:
        for _, item in alertas.iterrows():
            linha = (
                f"- {item['nome_produto']} | Estoque: {int(item['quantidade_estoque_atual'])} | "
                f"Vendido: {int(item['quantidade_vendida_total'])}"
            )
            pdf.cell(0, 7, _safe_pdf_text(linha), ln=1)

    output = pdf.output(dest="S")
    if isinstance(output, str):
        return output.encode("latin-1")
    if isinstance(output, bytearray):
        return bytes(output)
    return output

# ==========================================
# UI: Front-end (Dashboard e CRUD)
# ==========================================
st.title("📦 Painel de Giro de Estoque - AC1 + AC2")

tab_dashboard, tab_cadastrar, tab_atualizar, tab_relatorios = st.tabs([
    "📊 Dashboard de BI",
    "➕ Novo Produto",
    "🔄 Atualizar Estoque",
    "🧾 Relatórios PDF (AC2)"
])

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

    # ABA 4: RELATÓRIO PDF (AC2)
    with tab_relatorios:
        st.subheader("Gerar Relatório Gerencial em PDF")
        st.caption("Funcionalidade inédita AC2: geração de relatório analítico a partir dos dados persistidos no banco.")

        if df.empty:
            st.warning("Não há dados para gerar relatório.")
        else:
            incluir_apenas_criticos = st.checkbox("Gerar somente com produtos em estoque crítico (<5 unidades)")
            df_relatorio = df[df["quantidade_estoque_atual"] < 5] if incluir_apenas_criticos else df

            st.dataframe(
                df_relatorio[["id", "nome_produto", "quantidade_estoque_atual", "quantidade_vendida_total", "valor_unitario"]]
                .style.format({"valor_unitario": "R$ {:.2f}"}),
                use_container_width=True
            )

            if st.button("📄 Gerar arquivo PDF"):
                if df_relatorio.empty:
                    st.error("Não há dados no filtro selecionado para gerar o PDF.")
                else:
                    try:
                        pdf_bytes = generate_pdf_report(df_relatorio)
                        nome_arquivo = f"relatorio_estoque_ac2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        st.success("Relatório gerado com sucesso.")
                        st.download_button(
                            label="⬇️ Baixar Relatório PDF",
                            data=pdf_bytes,
                            file_name=nome_arquivo,
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Erro ao gerar o relatório: {e}")



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
