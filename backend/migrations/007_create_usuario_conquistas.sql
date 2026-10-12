CREATE TABLE IF NOT EXISTS usuario_conquistas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    conquista_id INT NOT NULL,
    desbloqueada_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_usuario_conquistas_ususario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_usuario_conquistas_conquista
        FOREIGN KEY (conquista_id) REFERENCES conquistas(id)
        ON DELETE CASCADE,
    
    CONSTRAINT uq_usuario_conquista
        UNIQUE (usuario_id, conquista_id)
);