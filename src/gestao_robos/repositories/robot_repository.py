from abc import ABC, abstractmethod

from gestao_robos.domain.entities.robot import Robot


class RobotRepository(ABC):
    """Define as operações de persistência de robôs."""

    @abstractmethod
    def find_all(self) -> list[Robot]:
        """Retorna todos os robôs cadastrados."""

    @abstractmethod
    def find_by_id(self, robot_id: int) -> Robot | None:
        """Busca um robô pelo ID."""

    @abstractmethod
    def save(self, robot: Robot) -> Robot:
        """Cria ou atualiza um robô."""

    @abstractmethod
    def delete(self, robot_id: int) -> None:
        """Remove um robô pelo ID."""
