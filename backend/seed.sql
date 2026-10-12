INSERT IGNORE INTO bebidas (nome, fator_hidratacao)
VALUES
    ('Água', 1.00),
    ('Café', 0.80),
    ('Chá', 0.90),
    ('Suco', 0.90);

INSERT IGNORE INTO conquistas (nome, descricao, pontos, criterio)
VALUES
    ('Primeiro consumo', 'Registre sua orimeira bebida', 10, 'primeiro_consumo'),
    ('Meta atingida', 'Alcance sua meta diária de hidratação', 20, 'meta_atingida'),
    ('Sequência de 3 dias', 'Atinja sua meta por 3 dias consecutivos', 30, 'sequencia_3_dias'),
    ('Sequência de 7 dias', 'Atinja sua meta por 7 dias consecutivos', 50, 'sequencia_7_dias');