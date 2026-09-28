from datetime import datetime

from gestao_robos.domain.entities.execution import Execution


def create_execution(
    finished: datetime | None = None,
    active: str = "S",
) -> Execution:
    """Cria uma execução válida para os testes."""

    return Execution(
        id=409800,
        robot_id=33,
        execute="N",
        server="APLUJF4-andrew.martin",
        start=datetime(2026, 9, 28, 13, 51, 18),
        finished=finished,
        active=active,
        pid=0,
        limit_time=datetime(2026, 9, 29, 4, 51, 18),
        server_id=None,
    )


def test_execution_is_running_when_not_finished_and_active() -> None:
    execution = create_execution()

    assert execution.is_running is True
    assert execution.is_finished is False


def test_execution_is_finished_when_finished_exists() -> None:
    execution = create_execution(
        finished=datetime(2026, 9, 28, 13, 52, 56),
        active="N",
    )

    assert execution.is_running is False
    assert execution.is_finished is True
