import sqlite3

from gestao_robos.infrastructure.database.sqlite_robot_repository import (
    SQLiteRobotRepository,
)
from gestao_robos.infrastructure.database.sqlite_seed import seed_database


def test_seed_database() -> None:
    connection = sqlite3.connect(":memory:")

    seed_database(connection)

    repository = SQLiteRobotRepository(connection)
    robots = repository.find_all()

    assert len(robots) == 6
    assert robots[0].nome == "Robô Financeiro"
    assert robots[0].ativo is True
    assert robots[2].horario_ativacao is not None