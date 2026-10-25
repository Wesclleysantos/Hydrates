from app.database import get_connection

def listar_bebidas(usuario_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, usuario_id, nome, fator_hidratacao, activo, criado_em
            FROM bebidas
            WHERE activo = TRUE
              AND (usuario_id IS NULL OR usuario_id = %s)
            ORDER BY nome
            """,
            (usuario_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def criar_bebida(
    usuario_id: int,
    nome: str,
    fator_hidratacao: float,
):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO bebidas (usuario_id, nome, fator_hidratacao)
            VALUES (%s, %s, %s)
            """,
            (usuario_id, nome, fator_hidratacao),
        )
        connection.commit()
        return cursor.lastrowid
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

def buscar_por_nome(
    nome: str,
    usuario_id: int,
    excluir_bebida_id: int | None = None,
):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        consulta = """
            SELECT id, nome
            FROM bebidas
            WHERE usuario_id = %s
              AND LOWER(nome) = LOWER(%s)
        """
        parametros = [usuario_id, nome]

        if excluir_bebida_id is not None:
            consulta += " AND id <> %s"
            parametros.append(excluir_bebida_id)

        consulta += " LIMIT 1"
        cursor.execute(consulta, tuple(parametros))
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

def buscar_por_id(bebida_id: int, usuario_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, usuario_id, nome, fator_hidratacao, activo
            FROM bebidas
            WHERE id = %s
              AND (usuario_id IS NULL OR usuario_id = %s)
            LIMIT 1
            """,
            (bebida_id, usuario_id),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

def buscar_bebida_do_usuario(bebida_id: int, usuario_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, usuario_id, nome, fator_hidratacao, activo
            FROM bebidas
            WHERE id = %s
              AND usuario_id = %s
            LIMIT 1
            """,
            (bebida_id, usuario_id),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

def atualizar_bebida_do_usuario(
    bebida_id: int,
    usuario_id: int,
    nome: str,
    fator_hidratacao: float,
):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE bebidas
            SET nome = %s,
                fator_hidratacao = %s
            WHERE id = %s
              AND usuario_id = %s
            """,
            (nome, fator_hidratacao, bebida_id, usuario_id),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
