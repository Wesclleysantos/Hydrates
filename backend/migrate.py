from pathlib import Path
from app.database import get_connection

MIGRATIONS_DIR = Path(__file__).parent / "migrations"

def create_migrations_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome_arquivo VARCHAR(255) NOT NULL UNIQUE,
            aplicada_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    cursor.close()

def get_applied_migrations(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT nome_arquivo FROM migrations")
    applied = {row[0] for row in cursor.fetchall()}

    cursor.close()
    return applied

def apply_migration(connection, migration_file):
    sql = migration_file.read_text(encoding="utf-8")
    cursor = connection.cursor()

    try:
        for statement in sql.split(";"):
            statement = statement.strip()

            if statement:
                cursor.execute(statement)

        cursor.execute(
            "INSERT INTO migrations (nome_arquivo) VALUES (%s)",
            (migration_file.name,),
        )

        connection.commit()
        print(f"Migração aplicada: {migration_file.name}")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

def main():
    connection = get_connection()

    try:
        create_migrations_table(connection)
        applied = get_applied_migrations(connection)
        migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

        for migration_file in migration_files:
            if migration_file.name in applied:
                print(f"Já aplicada: {migration_file.name}")
                continue

            apply_migration(connection, migration_file)
        print("Processo de migrações finalizado!")

    finally:
        connection.close()

if __name__ == "__main__":
    main()