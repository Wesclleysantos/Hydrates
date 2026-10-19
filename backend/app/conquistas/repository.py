from app.database import get_connection

def listar_conquistas_ativas():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, nome, descricao, pontos, criterio, ativa, criado_em
            FROM conquistas
            WHERE ativa = TRUE
            ORDER BY pontos ASC
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def listar_conquistas_usuario(usuario_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                uc.id,
                uc.usuario_id,
                c.id AS conquista_id,
                c.nome,
                c.descricao,
                c.pontos,
                c.criterio,
                uc.desbloqueada_em
            FROM usuario_conquistas uc
            INNER JOIN conquistas c ON c.id = uc.conquista_id
            WHERE uc.usuario_id = %s
            ORDER BY uc.desbloqueada_em DESC
            """,
            (usuario_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def desbloquear_conquista(usuario_id: int, conquista_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT pontos
            FROM conquistas
            WHERE id = %s AND ativa = TRUE
            """,
            (conquista_id,),
        )
        conquista = cursor.fetchone()
        if not conquista:
            raise ValueError("Conquista não encontrada ou inativa.")

        pontos = int(conquista[0])
        cursor.execute(
            """
            INSERT IGNORE INTO usuario_conquistas (usuario_id, conquista_id)
            VALUES (%s, %s)
            """,
            (usuario_id, conquista_id),
        )

        if cursor.rowcount == 0:
            connection.commit()
            return None

        usuario_conquista_id = cursor.lastrowid
        cursor.execute(
            "UPDATE usuarios SET pontos = pontos + %s WHERE id = %s",
            (pontos, usuario_id),
        )

        connection.commit()
        return usuario_conquista_id
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
