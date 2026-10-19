from app.database import get_connection

def buscar_meta_do_dia(usuario_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                usuario_id,
                quantidade_ml,
                data_meta
            FROM metas
            WHERE usuario_id = %s
              AND data_meta = CURDATE()
            LIMIT 1
            """,
            (usuario_id,),
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()

def definir_meta_do_dia(usuario_id: int, quantidade_ml: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            INSERT INTO metas (
                usuario_id,
                quantidade_ml,
                data_meta
            )
            VALUES (%s, %s, CURDATE())
            ON DUPLICATE KEY UPDATE
                quantidade_ml = VALUES(quantidade_ml)
            """,
            (usuario_id, quantidade_ml),
        )

        connection.commit()

        cursor.execute(
            """
            SELECT
                id,
                usuario_id,
                quantidade_ml,
                data_meta
            FROM metas
            WHERE usuario_id = %s
              AND data_meta = CURDATE()
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

def calcular_consumo_do_dia(usuario_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                COALESCE(SUM(hidratacao_ml), 0) AS consumido_ml
            FROM consumos
            WHERE usuario_id = %s
              AND consumido_em >= CURDATE()
              AND consumido_em < DATE_ADD(CURDATE(), INTERVAL 1 DAY)
            """,
            (usuario_id,),
        )

        resultado = cursor.fetchone()
        return float(resultado["consumido_ml"])

    finally:
        cursor.close()
        connection.close()

def listar_dias_com_meta_atingida(usuario_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                m.data_meta,
                m.quantidade_ml AS meta_ml,
                COALESCE(SUM(c.hidratacao_ml), 0) AS consumido_ml
            FROM metas m
            LEFT JOIN consumos c
                ON c.usuario_id = m.usuario_id
                AND c.consumido_em >= m.data_meta
                AND c.consumido_em < DATE_ADD(
                    m.data_meta,
                    INTERVAL 1 DAY
                )
            WHERE m.usuario_id = %s
            GROUP BY
                m.id,
                m.data_meta,
                m.quantidade_ml
            HAVING consumido_ml >= meta_ml
            ORDER BY m.data_meta DESC
            """,
            (usuario_id,),
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()
