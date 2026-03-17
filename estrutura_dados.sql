-- estrutura_dados.sql
-- Script compatível com PostgreSQL (usando SERIAL). 
-- Caso utilize MySQL, mude 'SERIAL' para 'INT AUTO_INCREMENT'.

CREATE TABLE produtos_estoque (
    id SERIAL PRIMARY KEY,
    nome_produto VARCHAR(255) NOT NULL,
    quantidade_estoque_atual INT NOT NULL,
    quantidade_vendida_total INT NOT NULL,
    valor_unitario DECIMAL(10, 2) NOT NULL,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserindo dados fictícios com variações de giro e estoque para a loja de Pudins
INSERT INTO produtos_estoque (nome_produto, quantidade_estoque_atual, quantidade_vendida_total, valor_unitario, data_atualizacao) VALUES
('Pudim Tradicional', 20, 150, 15.00, CURRENT_TIMESTAMP),      -- Giro alto (150/20 = 7.5)
('Pudim de Doce de Leite', 15, 80, 18.00, CURRENT_TIMESTAMP),     -- Giro médio (80/15 = 5.33)
('Pudim de Nutella', 3, 15, 22.00, CURRENT_TIMESTAMP),           -- Alerta reposição (stock < 5)
('Pudim de Pistache', 25, 5, 25.00, CURRENT_TIMESTAMP),           -- Giro baixo (5/25 = 0.2)
('Pudim Vegano', 2, 8, 20.00, CURRENT_TIMESTAMP),                 -- Alerta reposição (stock < 5)
('Pudim de Café', 10, 40, 16.00, CURRENT_TIMESTAMP),              -- Giro médio (40/10 = 4)
('Pudim de Chocolate Branco', 4, 60, 19.00, CURRENT_TIMESTAMP);   -- Alerta reposição e Giro altíssimo (60/4 = 15)
