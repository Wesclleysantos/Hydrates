CREATE TABLE IF NOT EXISTS metas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    quantidade_ml INT NOT NULL,
    data_meta DATE NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_metas_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_meta_usuario_data
        UNIQUE (usuario_id, data_meta),

    CONSTRAINT chk_meta_positiva
        CHECK (quantidade_ml > 0)
);