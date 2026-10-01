import sqlite3
from pathlib import Path

from gestao_robos.infrastructure.database.sqlite_seed import seed_database


def main() -> None:
    """Cria o banco SQLite de desenvolvimento."""
    database_path = Path("data/gestao_robos_dev.db")

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(database_path)

    try:
        seed_database(connection)
    finally:
        connection.close()

    print(f"Banco SQLite criado em: {database_path}")


if __name__ == "__main__":
    main()