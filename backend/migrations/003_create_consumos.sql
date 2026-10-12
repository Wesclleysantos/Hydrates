CREATE TABLE IF NOT EXISTS consumos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    bebida_id INT NOT NULL,
    quantidade_ml DECIMAL(8, 2) NOT NULL,
    hidratacao_ml DECIMAL(8, 2) NOT NULL,
    consumido_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_consumos_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_consumos_bebida
        FOREIGN KEY (bebida_id) REFERENCES bebidas(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_quantidade_positiva
        CHECK (quantidade_ml > 0),

    CONSTRAINT chk_hidratacao_nao_negativa
        CHECK (hidratacao_ml >=0)
);