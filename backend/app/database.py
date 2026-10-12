import mysql.connector
from mysql.connector import Error
from app.config import settings

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
        )
        return connection
    except Error as error:
        print(f"Erro ao conectar ao MySQL: {error}")
        raise