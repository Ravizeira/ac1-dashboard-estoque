import os
import urllib.parse
from sqlalchemy import create_engine, text

db_type = 'postgresql+pg8000'
db_user = 'postgres'
db_pass = os.environ.get('DB_PASS', '102010@gu')
db_host = 'localhost'
db_port = '5432'
db_name = 'postgres' # Conecta ao banco default para checar e criar

db_pass_encoded = urllib.parse.quote_plus(db_pass)
db_url = f"{db_type}://{db_user}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}"

try:
    engine = create_engine(db_url, isolation_level='AUTOCOMMIT')
    with engine.connect() as conn:
        print("Connected successfully to default postgres db!")
        # Verifica se o banco existe
        res = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='estoque_db';")).scalar()
        if not res:
            print("Creating database estoque_db...")
            conn.execute(text("CREATE DATABASE estoque_db"))
            print("Database estoque_db created successfully!")
        else:
            print("Database estoque_db already exists.")
except Exception as e:
    import traceback
    traceback.print_exc()
