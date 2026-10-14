from app.database import get_connection

def buscar_por_email(email: str):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, nome, email, senha_hash, peso, idade, pontos, criado_em
            FROM usuarios
            WHERE email = %s 
            """,
            (email,),
        )

        usuario = cursor.fetchone()
        return usuario

    finally:
        cursor.close()
        connection.close()

def criar_usuario(
        nome: str,
        email: str,
        senha_hash: str,
        peso: float | None = None,
        idade: int | None = None,
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, senha_hash, peso, idade)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nome, email, senha_hash, peso, idade),
        )

        connection.commit()
        return cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

