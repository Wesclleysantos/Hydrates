from app.database import get_connection

def criar_consumo(
    usuario_id: int,
    bebida_id: int,
    quantidade_ml: int,
    hidratacao_ml: float,
):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO consumos (
                usuario_id,
                bebida_id,
                quantidade_ml,
                hidratacao_ml
            )
            VALUES (%s, %s, %s, %s)
            """,
            (usuario_id, bebida_id, quantidade_ml, hidratacao_ml),
        )
        connection.commit()
        return cursor.lastrowid
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

def listar_consumos(usuario_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                c.id,
                c.usuario_id,
                c.bebida_id,
                b.nome AS bebida,
                c.quantidade_ml,
                c.hidratacao_ml,
                c.consumido_em
            FROM consumos c
            INNER JOIN bebidas b ON b.id = c.bebida_id
            WHERE c.usuario_id = %s
            ORDER BY c.consumido_em DESC
            """,
            (usuario_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def resumir_consumos(usuario_id: int, data_inicio, data_fim):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                DATE(consumido_em) AS data_consumo,
                COALESCE(SUM(quantidade_ml), 0) AS quantidade_ml,
                COALESCE(SUM(hidratacao_ml), 0) AS hidratacao_ml,
                COUNT(*) AS registros
            FROM consumos
            WHERE usuario_id = %s
              AND consumido_em >= %s
              AND consumido_em < DATE_ADD(%s, INTERVAL 1 DAY)
            GROUP BY DATE(consumido_em)
            ORDER BY data_consumo
            """,
            (usuario_id, data_inicio, data_fim),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def usuario_tem_consumo(usuario_id: int) -> bool:
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1 FROM consumos WHERE usuario_id = %s
            )
            """,
            (usuario_id,),
        )
        resultado = cursor.fetchone()
        return bool(resultado[0])
    finally:
        cursor.close()
        connection.close()
        