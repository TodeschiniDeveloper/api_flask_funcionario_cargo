create database projeto;
use projeto;
-- Tabela de Usuários
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Projetos
CREATE TABLE projetos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    data_inicio DATE,
    status VARCHAR(50) DEFAULT 'Pendente',
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela de Tarefas
CREATE TABLE tarefas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    concluida BOOLEAN DEFAULT FALSE,
    data_limite DATE,
    projeto_id INT NOT NULL,
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE
);
INSERT INTO usuarios (nome, email, senha_hash) VALUES
('Ana Silva', 'ana.silva@email.com', 'hash_da_senha_da_ana'), -- ID será 1
('Bruno Costa', 'bruno.costa@email.com', 'hash_da_senha_do_bruno'); -- ID será 2
INSERT INTO projetos (nome, descricao, data_inicio, status, usuario_id) VALUES
('API de E-commerce', 'Desenvolver a API REST para a nova loja virtual.', '2025-11-01', 'Em Andamento', 1),
('Website Institucional', 'Criar o novo site da empresa com um blog integrado.', '2025-10-20', 'Concluído', 1);
INSERT INTO projetos (nome, descricao, data_inicio, status, usuario_id) VALUES
('Aplicativo Mobile de Fitness', 'App para iOS e Android para monitoramento de treinos.', '2026-01-15', 'Pendente', 2);
INSERT INTO tarefas (titulo, concluida, data_limite, projeto_id) VALUES
('Definir endpoints de produtos', TRUE, '2025-11-05', 1),
('Implementar autenticação JWT', FALSE, '2025-11-10', 1),
('Criar CRUD de clientes', FALSE, '2025-11-15', 1);
INSERT INTO tarefas (titulo, concluida, projeto_id) VALUES
('Criar layout da home page', TRUE, 2),
('Desenvolver página de contato', TRUE, 2);
INSERT INTO tarefas (titulo, concluida, data_limite, projeto_id) VALUES
('Desenhar telas no Figma', FALSE, '2026-01-30', 3),
('Configurar ambiente de desenvolvimento React Native', FALSE, '2026-02-05', 3);