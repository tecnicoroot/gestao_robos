from pathlib import Path

from gestao_robos.infrastructure.database.robot_repository_factory import (
    create_sqlite_robot_repository,
)


def test_create_sqlite_robot_repository(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "test.db"

    repository = create_sqlite_robot_repository(
        str(database_path),
    )

    assert repository.find_all() == []