

from gestao_robos.infrastructure.database.connection import (
    DatabaseConnection,
)


def test_database_connection() -> None:
    """Verifica se a aplicação consegue acessar o banco."""
    database = DatabaseConnection()

    with database.connection() as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

            assert result is not None
            assert result[0] == 1
        finally:
            cursor.close()