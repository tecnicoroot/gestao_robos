
from gestao_robos.infrastructure.database.config import load_database_settings
from gestao_robos.infrastructure.database.connection import DatabaseConnection
from gestao_robos.infrastructure.database.mysql_robot_repository import (
    MySQLRobotRepository,
)


def test_find_all_robots() -> None:
    settings = load_database_settings()

    database = DatabaseConnection(settings)
    repository = MySQLRobotRepository(database)

    robots = repository.find_all()

    assert robots
    assert all(robot.id is not None for robot in robots)

def test_find_robot_by_id() -> None:
    settings = load_database_settings()

    database = DatabaseConnection(settings)
    repository = MySQLRobotRepository(database)

    robot = repository.find_by_id(51)

    assert robot is not None
    assert robot.id == 51
    assert robot.nome == "HUHB - Guias - Classificação Paciente Paleativos"