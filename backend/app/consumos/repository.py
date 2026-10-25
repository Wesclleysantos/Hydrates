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


def resumir_consumos_diario_por_bebida(
    usuario_id: int,
    data_inicio,
    data_fim,
    bebida_id: int | None = None,
):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        filtro_bebida = ""
        parametros = [usuario_id, usuario_id]

        if bebida_id is not None:
            filtro_bebida = " AND c.bebida_id = %s"
            parametros.append(bebida_id)

        parametros.extend([data_inicio, data_fim])
        cursor.execute(
            f"""
            SELECT
                DATE(c.consumido_em) AS data_consumo,
                b.id AS bebida_id,
                b.nome AS bebida,
                COALESCE(SUM(c.quantidade_ml), 0) AS quantidade_ml,
                COALESCE(SUM(c.hidratacao_ml), 0) AS hidratacao_ml,
                COUNT(c.id) AS registros
            FROM consumos c
            INNER JOIN bebidas b ON b.id = c.bebida_id
            WHERE c.usuario_id = %s
              AND (b.usuario_id IS NULL OR b.usuario_id = %s)
              {filtro_bebida}
              AND c.consumido_em >= %s
              AND c.consumido_em < DATE_ADD(%s, INTERVAL 1 DAY)
            GROUP BY DATE(c.consumido_em), b.id, b.nome
            ORDER BY data_consumo, b.nome
            """,
            tuple(parametros),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()