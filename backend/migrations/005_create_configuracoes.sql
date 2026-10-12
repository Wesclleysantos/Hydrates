CREATE TABLE IF NOT EXISTS configuracoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    lembretes_ativos BOOLEAN NOT NULL DEFAULT TRUE,
    intervalo_lembrete_minutos INT NOT NULL DEFAULT 60,
    horario_inicio TIME NULL,
    horario_fim TIME NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_configuracoes_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE,
    
    CONSTRAINT uq_configuracoes_usuario
        UNIQUE (usuario_id),

    CONSTRAINT chk_intervalo_lembrete
        CHECK (intervalo_lembrete_minutos > 0)
);