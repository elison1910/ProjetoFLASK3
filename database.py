import os
import sqlite3

#Apaga o arquivo database.db se existir
if os.path.exists('database.db'):
    os.remove('database.db')

#Cria um novo banco de dados e as tabelas necessárias
conn = sqlite3.connect('database.db')  # Cria ou abre o banco de dados
cursor = conn.cursor()

# Criar a tabela cargos
cursor.execute('''
CREATE TABLE IF NOT EXISTS cargos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao VARCHAR(200) NOT NULL
);
''')

#Cria a tabela users com referência à tabela cargos
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    cargo INTEGER,
    FOREIGN KEY (cargo) REFERENCES cargos(id)
);
''')


# PARTE DOS ATENDENTES
#Cria Tabela (Negócio) Atendimentos:
cursor.execute('''
CREATE TABLE Atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    atendente_id INTEGER,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    descricao TEXT,
    feedback_cliente VARCHAR(300),
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id),
    FOREIGN KEY (atendente_id) REFERENCES Users(id)
);
''')

#Cria Tabela (Entidade) Produtos:
cursor.execute('''
CREATE TABLE Produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INTEGER NOT NULL DEFAULT 0,
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES Categorias(id)
);
''')

#Cria Tabela (Entidade) Historico de Atendimentos:
cursor.execute('''
CREATE TABLE Historico_Atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    atendimento_id INTEGER,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    observacoes TEXT,
    atendente_id INTEGER,
    FOREIGN KEY (atendimento_id) REFERENCES Atendimentos(id),
    FOREIGN KEY (atendente_id) REFERENCES Users(id)
);
''')


# PARTE DOS GERENTES
#Cria Tabela (Negócio) Vendas:
cursor.execute('''
CREATE TABLE Vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    produto_id INTEGER,
    data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
    quantidade INTEGER NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id),
    FOREIGN KEY (produto_id) REFERENCES Produtos(id)
);
''')

#Cria Tabela (Entidade) Fornecedores:
cursor.execute('''
CREATE TABLE Fornecedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    contato VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(15),
    endereco TEXT
);
''')

cursor.execute('''
CREATE TABLE Avaliacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    cliente_id INTEGER,
    avaliacao INTEGER CHECK(avaliacao BETWEEN 1 AND 5),
    comentario TEXT,
    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES Produtos(id),
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id)
);
''')


#Efetivar a transação (commit)
conn.commit()

#Fechar a conexão
conn.close()