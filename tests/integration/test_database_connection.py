from gestao_robos.infrastructure.database.config import load_database_settings
from gestao_robos.infrastructure.database.connection import DatabaseConnection


def test_database_connection() -> None:
    
    settings = load_database_settings()

    database = DatabaseConnection(settings)

    with database.connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

    assert result is not None