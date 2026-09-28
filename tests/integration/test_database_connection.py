from pathlib import Path

from gestao_robos.infrastructure.database.config import load_database_settings
from gestao_robos.infrastructure.database.connection import DatabaseConnection


def test_database_connection() -> None:
    key_path = Path(r"C:\martin\am.key")
    config_path = Path(r"C:\martin\am.cfg")

    settings = load_database_settings(
        key_path=key_path,
        config_path=config_path,
    )

    database = DatabaseConnection(settings)

    with database.connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

    assert result is not None