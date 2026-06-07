import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
import urllib.parse
from datetime import datetime
from fpdf import FPDF

# Configuração da página Streamlit
st.set_page_config(page_title="Painel de Giro de Estoque - AC1/AC2/AC3/Parte Final", layout="wide")

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


def ensure_movements_table():
    query = text("""
        CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
            id SERIAL PRIMARY KEY,
            produto_id INT NOT NULL REFERENCES produtos_estoque(id),
            tipo_movimentacao VARCHAR(10) NOT NULL CHECK (tipo_movimentacao IN ('ENTRADA', 'SAIDA')),
            quantidade INT NOT NULL CHECK (quantidade > 0),
            observacao VARCHAR(255),
            data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    with engine.begin() as conn:
        conn.execute(query)


ensure_movements_table()


def ensure_replenishment_table():
    query = text("""
        CREATE TABLE IF NOT EXISTS reposicoes_inteligentes (
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
        )
    """)
    with engine.begin() as conn:
        conn.execute(query)


ensure_replenishment_table()

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


def register_movement(produto_id, tipo_movimentacao, quantidade, observacao):
    tipo = tipo_movimentacao.upper()
    if tipo not in ("ENTRADA", "SAIDA"):
        raise ValueError("Tipo de movimentação inválido.")

    with engine.begin() as conn:
        estoque_atual = conn.execute(
            text("SELECT quantidade_estoque_atual FROM produtos_estoque WHERE id = :id"),
            {"id": int(produto_id)}
        ).scalar()

        if estoque_atual is None:
            raise ValueError("Produto não encontrado.")

        if tipo == "SAIDA" and int(estoque_atual) < int(quantidade):
            raise ValueError("Saída inválida: estoque insuficiente.")

        if tipo == "ENTRADA":
            conn.execute(text("""
                UPDATE produtos_estoque
                SET quantidade_estoque_atual = quantidade_estoque_atual + :quantidade
                WHERE id = :id
            """), {"quantidade": int(quantidade), "id": int(produto_id)})
        else:
            conn.execute(text("""
                UPDATE produtos_estoque
                SET quantidade_estoque_atual = quantidade_estoque_atual - :quantidade,
                    quantidade_vendida_total = quantidade_vendida_total + :quantidade
                WHERE id = :id
            """), {"quantidade": int(quantidade), "id": int(produto_id)})

        conn.execute(text("""
            INSERT INTO movimentacoes_estoque (produto_id, tipo_movimentacao, quantidade, observacao)
            VALUES (:produto_id, :tipo_movimentacao, :quantidade, :observacao)
        """), {
            "produto_id": int(produto_id),
            "tipo_movimentacao": tipo,
            "quantidade": int(quantidade),
            "observacao": observacao.strip() if observacao else None
        })


def load_movements():
    query = """
        SELECT
            m.id,
            m.data_movimentacao,
            p.nome_produto,
            m.tipo_movimentacao,
            m.quantidade,
            m.observacao
        FROM movimentacoes_estoque m
        JOIN produtos_estoque p ON p.id = m.produto_id
        ORDER BY m.data_movimentacao DESC, m.id DESC
        LIMIT 200
    """
    return pd.read_sql(query, engine)


def build_replenishment_plan(df_base):
    if df_base.empty:
        return pd.DataFrame()

    dados = df_base.copy()
    dados["estoque_minimo_recomendado"] = dados["quantidade_vendida_total"].apply(
        lambda qtd_vendida: max(5, int(round(float(qtd_vendida) * 0.10)))
    )
    dados["estoque_meta"] = dados["quantidade_vendida_total"].apply(
        lambda qtd_vendida: max(10, int(round(float(qtd_vendida) * 0.30)))
    )
    dados["quantidade_sugerida"] = (
        dados["estoque_meta"] - dados["quantidade_estoque_atual"]
    ).clip(lower=0).astype(int)

    def _classificar_prioridade(row):
        if row["quantidade_estoque_atual"] <= row["estoque_minimo_recomendado"]:
            return "ALTA"
        if row["quantidade_estoque_atual"] < row["estoque_meta"]:
            return "MEDIA"
        return "BAIXA"

    dados["prioridade"] = dados.apply(_classificar_prioridade, axis=1)
    dados["motivo"] = dados.apply(
        lambda row: (
            f"Meta de reposição: {int(row['estoque_meta'])} unidades "
            f"(mínimo recomendado: {int(row['estoque_minimo_recomendado'])})."
        ),
        axis=1,
    )
    dados = dados[dados["quantidade_sugerida"] > 0].copy()
    if dados.empty:
        return dados

    prioridade_ordem = {"ALTA": 0, "MEDIA": 1, "BAIXA": 2}
    dados["ordem_prioridade"] = dados["prioridade"].map(prioridade_ordem)

    return dados[
        [
            "id",
            "nome_produto",
            "quantidade_estoque_atual",
            "quantidade_vendida_total",
            "estoque_minimo_recomendado",
            "estoque_meta",
            "quantidade_sugerida",
            "prioridade",
            "motivo",
            "ordem_prioridade",
        ]
    ].sort_values(
        by=["ordem_prioridade", "quantidade_sugerida", "nome_produto"],
        ascending=[True, False, True],
    ).drop(columns=["ordem_prioridade"])


def save_replenishment_plan(df_plan):
    if df_plan.empty:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM reposicoes_inteligentes"))
        return

    data_calculo = datetime.now()
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM reposicoes_inteligentes"))
        for _, row in df_plan.iterrows():
            conn.execute(
                text("""
                    INSERT INTO reposicoes_inteligentes (
                        produto_id,
                        estoque_atual,
                        quantidade_vendida_total,
                        estoque_minimo_recomendado,
                        estoque_meta,
                        quantidade_sugerida,
                        prioridade,
                        motivo,
                        data_calculo
                    )
                    VALUES (
                        :produto_id,
                        :estoque_atual,
                        :quantidade_vendida_total,
                        :estoque_minimo_recomendado,
                        :estoque_meta,
                        :quantidade_sugerida,
                        :prioridade,
                        :motivo,
                        :data_calculo
                    )
                """),
                {
                    "produto_id": int(row["id"]),
                    "estoque_atual": int(row["quantidade_estoque_atual"]),
                    "quantidade_vendida_total": int(row["quantidade_vendida_total"]),
                    "estoque_minimo_recomendado": int(row["estoque_minimo_recomendado"]),
                    "estoque_meta": int(row["estoque_meta"]),
                    "quantidade_sugerida": int(row["quantidade_sugerida"]),
                    "prioridade": row["prioridade"],
                    "motivo": row["motivo"],
                    "data_calculo": data_calculo,
                },
            )


def load_replenishment_plan():
    query = """
        SELECT
            r.id,
            r.data_calculo,
            p.nome_produto,
            r.estoque_atual,
            r.quantidade_vendida_total,
            r.estoque_minimo_recomendado,
            r.estoque_meta,
            r.quantidade_sugerida,
            r.prioridade,
            r.motivo
        FROM reposicoes_inteligentes r
        JOIN produtos_estoque p ON p.id = r.produto_id
        ORDER BY
            CASE r.prioridade
                WHEN 'ALTA' THEN 1
                WHEN 'MEDIA' THEN 2
                ELSE 3
            END,
            r.quantidade_sugerida DESC,
            r.id DESC
    """
    return pd.read_sql(query, engine)


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
st.title("📦 Painel de Giro de Estoque")

tab_dashboard, tab_cadastrar, tab_atualizar, tab_relatorios, tab_reposicao = st.tabs([
    "📊 Dashboard de BI",
    "➕ Novo Produto",
    "🔄 Movimentações (AC3)",
    "🧾 Relatórios PDF (AC2)",
    "📦 Reposição Inteligente"
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

    # ABA 3: MOVIMENTAÇÕES COM HISTÓRICO (AC3)
    with tab_atualizar:
        st.subheader("Registrar Entrada / Saída de Estoque")
        if not df.empty:
            with st.form("form_movimentacao_estoque"):
                opcoes_produtos = dict(zip(df['nome_produto'], df['id']))
                produto_selecionado = st.selectbox("Selecione o Produto", options=list(opcoes_produtos.keys()))

                tipo_movimentacao = st.selectbox("Tipo de Movimentação", options=["ENTRADA", "SAIDA"])
                quantidade_movimentada = st.number_input("Quantidade", min_value=1, step=1, value=1)
                observacao_movimentacao = st.text_input("Observação (Opcional)", max_chars=255)

                submit_movimentacao = st.form_submit_button("💾 Registrar Movimentação")

                if submit_movimentacao:
                    id_alvo = opcoes_produtos[produto_selecionado]
                    try:
                        register_movement(id_alvo, tipo_movimentacao, quantidade_movimentada, observacao_movimentacao)
                        st.success(
                            f"Movimentação registrada: {tipo_movimentacao} de {quantidade_movimentada} unidade(s) para '{produto_selecionado}'."
                        )
                        st.info("Acesse o Dashboard e clique em 'Atualizar Dados' para refletir os novos saldos.")
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Erro ao registrar movimentação: {e}")

            st.divider()
            st.subheader("📜 Histórico de Movimentações")
            try:
                historico = load_movements()
                if historico.empty:
                    st.info("Nenhuma movimentação registrada até o momento.")
                else:
                    st.dataframe(historico, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao carregar histórico: {e}")
        else:
            st.warning("Não há produtos cadastrados para registrar movimentações.")

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

    # ABA 5: REPOSIÇÃO INTELIGENTE (PARTE FINAL)
    with tab_reposicao:
        st.subheader("Planejamento de Reposição Inteligente")
        st.caption("Funcionalidade nova da parte final: calcula sugestões de compra e salva o plano no banco.")
        st.info(
            "Regra adotada: estoque mínimo recomendado = maior entre 5 unidades e 10% das vendas acumuladas; "
            "estoque meta = maior entre 10 unidades e 30% das vendas acumuladas."
        )

        if df.empty:
            st.warning("Não há dados para gerar o plano de reposição.")
        else:
            if st.button("⚙️ Gerar Plano de Reposição"):
                try:
                    plano = build_replenishment_plan(df)
                    save_replenishment_plan(plano)
                    if plano.empty:
                        st.success("Nenhum produto precisa de reposição com os parâmetros atuais.")
                    else:
                        st.success(f"Plano gerado e salvo no banco para {len(plano)} produto(s).")
                except Exception as e:
                    st.error(f"Erro ao gerar o plano de reposição: {e}")

            try:
                plano_salvo = load_replenishment_plan()
                if plano_salvo.empty:
                    st.info("Clique em 'Gerar Plano de Reposição' para criar a primeira recomendação.")
                else:
                    total_produtos = len(plano_salvo)
                    total_unidades = int(plano_salvo["quantidade_sugerida"].sum())
                    alertas_altos = int((plano_salvo["prioridade"] == "ALTA").sum())

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Produtos com sugestão", total_produtos)
                    with col2:
                        st.metric("Unidades sugeridas", total_unidades)
                    with col3:
                        st.metric("Prioridade alta", alertas_altos)

                    st.divider()
                    st.subheader("📊 Sugestão de Compra por Produto")
                    st.bar_chart(
                        plano_salvo.set_index("nome_produto")[["quantidade_sugerida"]]
                    )

                    st.divider()
                    st.subheader("📋 Plano de Reposição Salvo")
                    plano_exibicao = plano_salvo.copy()
                    plano_exibicao["data_calculo"] = pd.to_datetime(plano_exibicao["data_calculo"]).dt.strftime("%d/%m/%Y %H:%M:%S")
                    st.dataframe(
                        plano_exibicao[[
                            "data_calculo",
                            "nome_produto",
                            "estoque_atual",
                            "quantidade_vendida_total",
                            "estoque_minimo_recomendado",
                            "estoque_meta",
                            "quantidade_sugerida",
                            "prioridade",
                            "motivo"
                        ]],
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Erro ao carregar o plano de reposição: {e}")



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
