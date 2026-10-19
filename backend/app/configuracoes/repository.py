from app.database import get_connection

def buscar_configuracoes(usuario_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                usuario_id,
                lembretes_ativos,
                intervalo_lembrete_minutos,
                horario_inicio,
                horario_fim,
                criado_em,
                atualizado_em
            FROM configuracoes
            WHERE usuario_id = %s
            LIMIT 1
            """,
            (usuario_id,),
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()

def salvar_configuracoes(
    usuario_id: int,
    lembretes_ativos: bool,
    intervalo_lembrete_minutos: int,
    horario_inicio: str | None,
    horario_fim: str | None,
):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            INSERT INTO configuracoes (
                usuario_id,
                lembretes_ativos,
                intervalo_lembrete_minutos,
                horario_inicio,
                horario_fim
            )
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                lembretes_ativos = VALUES(lembretes_ativos),
                intervalo_lembrete_minutos = VALUES(intervalo_lembrete_minutos),
                horario_inicio = VALUES(horario_inicio),
                horario_fim = VALUES(horario_fim)
            """,
            (
                usuario_id,
                lembretes_ativos,
                intervalo_lembrete_minutos,
                horario_inicio,
                horario_fim,
            ),
        )

        connection.commit()

        cursor.execute(
            """
            SELECT
                id,
                usuario_id,
                lembretes_ativos,
                intervalo_lembrete_minutos,
                horario_inicio,
                horario_fim,
                criado_em,
                atualizado_em
            FROM configuracoes
            WHERE usuario_id = %s
            LIMIT 1
            """,
            (usuario_id,),
        )

        return cursor.fetchone()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
