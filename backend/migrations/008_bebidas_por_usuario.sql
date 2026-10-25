ALTER TABLE bebidas
    ADD COLUMN usuario_id INT NULL AFTER id;

ALTER TABLE bebidas
    ADD INDEX idx_bebidas_usuario_id (usuario_id);

ALTER TABLE bebidas
    ADD CONSTRAINT fk_bebidas_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE;

ALTER TABLE bebidas
    ADD COLUMN escopo_usuario_id INT
        GENERATED ALWAYS AS (COALESCE(usuario_id, 0)) VIRTUAL;

ALTER TABLE bebidas
    DROP INDEX nome,
    ADD UNIQUE KEY uq_bebidas_escopo_nome (escopo_usuario_id, nome);