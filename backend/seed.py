from pathlib import Path
from app.database import get_connection

SEED_FILE = Path(__file__).parent / "seed.sql"

def main():
    connection = get_connection()

    try:
        sql = SEED_FILE.read_text(encoding="utf-8")
        cursor = connection.cursor()

        try:
            for statement in sql.split(";"):
                statement = statement.strip()

                if statement:
                    cursor.execute(statement)

            connection.commit()
            print("Dados iniciais inseridos com sucesso!")

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()

    finally:
        connection.close()

if __name__ == "__main__":
    main()