from dataclasses import dataclass
from datetime import datetime


@dataclass
class Execution:
    """Representa uma execução registrada na tabela `fila`."""

    id: int | None
    robot_id: int
    execute: str
    server: str
    start: datetime
    finished: datetime | None
    active: str
    pid: int | None
    limit_time: datetime
    server_id: int | None

    @property
    def is_running(self) -> bool:
        """Indica se a execução ainda está em andamento."""

        return self.finished is None and self.active == "S"

    @property
    def is_finished(self) -> bool:
        """Indica se a execução foi finalizada."""

        return self.finished is not None
