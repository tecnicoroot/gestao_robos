from gestao_robos.domain.entities.robot import Robot
from gestao_robos.repositories.robot_repository import RobotRepository


class RobotService:
    """Contém as operações de negócio relacionadas aos robôs."""

    def __init__(self, repository: RobotRepository) -> None:
        self.repository = repository

    def list_robots(self) -> list[Robot]:
        """Retorna todos os robôs cadastrados."""
        return self.repository.find_all()

    def get_robot(self, robot_id: int) -> Robot | None:
        """Retorna um robô pelo ID."""
        return self.repository.find_by_id(robot_id)

    def create_robot(self, robot: Robot) -> Robot:
        """Cria um novo robô."""
        if robot.id is not None:
            raise ValueError("Um novo robô não deve possuir ID.")

        return self.repository.save(robot)

    def update_robot(
        self,
        robot_id: int,
        nome: str,
        descricao: str,
    ) -> Robot:
        """Atualiza os dados básicos de um robô."""
        robot = self.repository.find_by_id(robot_id)

        if robot is None:
            raise ValueError(f"Robô {robot_id} não encontrado.")

        robot.update(nome, descricao)
        return self.repository.save(robot)

    def activate_robot(self, robot_id: int) -> Robot:
        """Ativa um robô."""
        robot = self._get_required_robot(robot_id)
        robot.activate()
        return self.repository.save(robot)

    def deactivate_robot(self, robot_id: int) -> Robot:
        """Desativa um robô."""
        robot = self._get_required_robot(robot_id)
        robot.deactivate()
        return self.repository.save(robot)

    def delete_robot(self, robot_id: int) -> None:
        """Remove um robô."""
        robot = self._get_required_robot(robot_id)

        if robot.ativo:
            raise ValueError(
                "Não é permitido excluir um robô ativo."
            )

        self.repository.delete(robot_id)

    def _get_required_robot(self, robot_id: int) -> Robot:
        robot = self.repository.find_by_id(robot_id)

        if robot is None:
            raise ValueError(f"Robô {robot_id} não encontrado.")

        return robot