import os
import urllib.parse
from sqlalchemy import create_engine, text

def main():
    print("Iniciando rotina de criacao de tabela e populacao...")
    print("="*60)
    
    # 1. Carregar variáveis do ambiente
    db_type = os.getenv("DB_TYPE", "postgresql")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "senha")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "estoque_db")

    print(f"Banco: {db_name} | Host: {db_host}")

    db_pass_encoded = urllib.parse.quote_plus(db_pass)
    db_url = f"{db_type}://{db_user}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}"

    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            print(">> Conexao ao banco realizada com sucesso!")
            
            # 2. Criar a Tabela
            conn.execute(text('''
            CREATE TABLE IF NOT EXISTS produtos_estoque (
                id SERIAL PRIMARY KEY,
                nome_produto VARCHAR(255) NOT NULL,
                quantidade_estoque_atual INT NOT NULL,
                quantidade_vendida_total INT NOT NULL,
                valor_unitario DECIMAL(10, 2) NOT NULL,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            '''))
            conn.commit()
            print(">> Tabela 'produtos_estoque' criada (ou ja existente).")
            
            # 3. Popular Dados (Só inserimos se não existir nada antes, evitando duplicados em execução dupla)
            res = conn.execute(text('SELECT COUNT(*) FROM produtos_estoque')).scalar()
            
            if res == 0:
                conn.execute(text('''
                INSERT INTO produtos_estoque (nome_produto, quantidade_estoque_atual, quantidade_vendida_total, valor_unitario) VALUES
                ('Pudim Tradicional', 20, 150, 15.00),
                ('Pudim de Doce de Leite', 15, 80, 18.00),
                ('Pudim de Nutella', 3, 15, 22.00),
                ('Pudim de Pistache', 25, 5, 25.00),
                ('Pudim Vegano', 2, 8, 20.00),
                ('Pudim de Café', 10, 40, 16.00),
                ('Pudim de Chocolate Branco', 4, 60, 19.00);
                '''))
                conn.commit()
                print(">> Dados populares ficticios inseridos com sucesso!")
            else:
                print(">> Tabela ja contem dados. Populacao nao foi refeita para evitar redundancia.")
                
        print(">> Setup DB finalizado com sucesso! Voce ja pode rodar o seu app.py pelo Streamlit.")
    except Exception as e:
        print("\n[ERRO FATAL]")
        print("Houve um erro ao se conectar / executar consultas:")
        print(f"Detalhes técnicos: {e}")
        print("\nDica: Certifique-se que você:")
        print("1. Configurou as variaveis de ambiente corretamente no PowerShell ($env:DB_PASS=...).")
        print("2. O PostgreSQL esta rodando no seu computador usando o usuario correto.")
        print("3. O banco de dados chamado 'estoque_db' de fato existe la dentro (pode precisar criar no pgAdmin antes).")

if __name__ == "__main__":
    main()
