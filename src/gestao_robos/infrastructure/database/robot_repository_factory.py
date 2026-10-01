from __future__ import annotations

import sqlite3

from gestao_robos.infrastructure.database.sqlite_robot_repository import (
    SQLiteRobotRepository,
)
from gestao_robos.repositories.robot_repository import RobotRepository


def create_sqlite_robot_repository(
    database_path: str,
) -> RobotRepository:
    """Cria um repositório SQLite."""
    connection = sqlite3.connect(database_path)

    return SQLiteRobotRepository(connection)