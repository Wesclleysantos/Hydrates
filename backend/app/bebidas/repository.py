from app.database import get_connection

def listar_bebidas():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, nome, fator_hidratacao, activo, criado_em
            FROM bebidas
            WHERE activo = TRUE
            ORDER BY nome
            """
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

def criar_bebida(nome: str, fator_hidratacao: float):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO bebidas (nome, fator_hidratacao)
            VALUES (%s, %s)
            """,
            (nome, fator_hidratacao),
        )

        connection.commit()

        return cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

def buscar_por_nome(nome: str):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, nome
            FROM bebidas
            WHERE LOWER(nome) = LOWER(%s)
            LIMIT 1
            """,
            (nome,),
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()