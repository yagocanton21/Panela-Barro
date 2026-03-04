-- 1. Tabela de Produtos
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco_base DECIMAL(10, 2) NOT NULL, -- Preço por kg ou por unidade
    categoria VARCHAR(50), 
    unidade_medida VARCHAR(10) DEFAULT 'kg' -- 'kg' ou 'un'
);

-- 2. Tabela de Comandas (O cartão físico)
CREATE TABLE comandas (
    id SERIAL PRIMARY KEY,
    numero_cartao INTEGER UNIQUE NOT NULL,
    aberta_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fechada_em TIMESTAMP,
    total DECIMAL(10, 2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'aberta'
);

-- 3. Tabela de Pedidos (Registro detalhado das pesagens)
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    comanda_id INTEGER REFERENCES comandas(id) ON DELETE CASCADE,
    produto_id INTEGER REFERENCES produtos(id),
    quantidade DECIMAL(10, 3) NOT NULL, -- Suporta gramas (ex: 0.452)
    valor_pago DECIMAL(10, 2) NOT NULL, -- (quantidade * preco_base)
    momento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dados iniciais para teste
INSERT INTO produtos (nome, preco_base, categoria, unidade_medida) 
VALUES ('Buffet Livre/Quilo', 69.90, 'Buffet', 'kg');

INSERT INTO produtos (nome, preco_base, categoria, unidade_medida) 
VALUES ('Refrigerante Lata', 6.00, 'Bebida', 'un');
