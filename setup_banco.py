import os
import urllib.parse
from sqlalchemy import create_engine, text

# 1. Configuração da Conexão (igual ao seu app.py)
db_type = os.getenv("DB_TYPE", "postgresql")
db_user = os.getenv("DB_USER", "postgres")
db_pass = os.getenv("DB_PASS", "COLOQUE_SUA_NOVA_SENHA_AQUI") # <--- Altere aqui!
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "estoque_db")

db_pass_encoded = urllib.parse.quote_plus(db_pass)
db_url = f"{db_type}://{db_user}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

# 2. Query para criar a tabela
sql_create = """
CREATE TABLE IF NOT EXISTS produtos_estoque (
    id SERIAL PRIMARY KEY,
    nome_produto VARCHAR(100) NOT NULL,
    quantidade_estoque_atual INTEGER NOT NULL,
    quantidade_vendida_total INTEGER NOT NULL,
    valor_unitario DECIMAL(10, 2)
);
"""

# 3. Query para inserir os dados da Com Amor, Pudim
# Coloquei alguns com estoque baixo (< 5) para o seu sistema gerar o "Alerta de Reposição" no vídeo!
sql_insert = """
INSERT INTO produtos_estoque (nome_produto, quantidade_estoque_atual, quantidade_vendida_total, valor_unitario)
VALUES 
('Pudim Tradicional (Leite Condensado)', 10, 45, 45.00),
('Pudim de Chocolate', 3, 20, 50.00),
('Pudim de Pistache', 2, 15, 65.00),
('Embalagem Plástica (Unidade)', 50, 150, 1.50),
('Adesivo com Logomarca', 4, 150, 0.50);
"""

# 4. Executando os comandos no banco
with engine.connect() as conn:
    # Cria a tabela
    conn.execute(text(sql_create))
    
    # Verifica se a tabela já tem dados para não duplicar
    result = conn.execute(text("SELECT COUNT(*) FROM produtos_estoque"))
    count = result.scalar()
    
    if count == 0:
        # Se estiver vazia, insere os dados
        conn.execute(text(sql_insert))
        print("✅ Tabela criada e produtos da Com Amor, Pudim inseridos com sucesso!")
    else:
        print("⚠️ A tabela já existe e já possui dados.")
        
    # Confirma as alterações no banco de dados
    conn.commit()