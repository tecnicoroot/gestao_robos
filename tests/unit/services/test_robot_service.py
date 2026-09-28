from datetime import time

import pytest

from gestao_robos.domain.entities.robot import Robot
from gestao_robos.repositories.robot_repository import RobotRepository
from gestao_robos.services.robot_service import RobotService


class FakeRobotRepository(RobotRepository):
    """Repositório em memória para testes."""

    def __init__(self) -> None:
        self.robots: list[Robot] = [
            self._create_robot(
                robot_id=51,
                nome="Robô de teste",
                ativo=True,
            ),
            self._create_robot(
                robot_id=52,
                nome="Robô inativo",
                ativo=False,
            ),
        ]

    def find_all(self) -> list[Robot]:
        return self.robots

    def find_by_id(self, robot_id: int) -> Robot | None:
        return next(
            (robot for robot in self.robots if robot.id == robot_id),
            None,
        )

    def save(self, robot: Robot) -> Robot:
        if robot.id is None:
            robot.id = self._next_id()
            self.robots.append(robot)
            return robot

        existing = self.find_by_id(robot.id)

        if existing is None:
            self.robots.append(robot)
        else:
            index = self.robots.index(existing)
            self.robots[index] = robot

        return robot

    def delete(self, robot_id: int) -> None:
        self.robots = [
            robot for robot in self.robots if robot.id != robot_id
        ]

    def _next_id(self) -> int:
        return max(
            (robot.id or 0 for robot in self.robots),
            default=0,
        ) + 1

    @staticmethod
    def _create_robot(
        robot_id: int | None,
        nome: str,
        ativo: bool,
    ) -> Robot:
        return Robot(
            id=robot_id,
            nome=nome,
            descricao="Descrição do robô",
            ativo=ativo,
            intervalo=60,
            acao="A",
            tela="N",
            path_executavel=r"C:\robos",
            limite_tempo=60,
            arquivo_ativacao="",
            nome_executavel="teste.exe",
            pasta_trabalho=r"C:\robos",
            repositorio_planilhas="",
            notificados="",
            pgm_ativado1="",
            pgm_ativado2="",
            robo_sequencia=None,
            usuario_robo="TESTE",
            robo_teste=1,
            horario_ativacao=time(8, 0),
            codigo_setor=1,
            biblioteca="",
        )


def create_service() -> tuple[RobotService, FakeRobotRepository]:
    """Cria o serviço e o repositório de teste."""
    repository = FakeRobotRepository()
    service = RobotService(repository)
    return service, repository


def test_list_robots() -> None:
    service, _ = create_service()

    robots = service.list_robots()

    assert len(robots) == 2
    assert robots[0].id == 51
    assert robots[1].id == 52


def test_get_robot() -> None:
    service, _ = create_service()

    robot = service.get_robot(51)

    assert robot is not None
    assert robot.id == 51
    assert robot.nome == "Robô de teste"


def test_get_robot_returns_none_when_not_found() -> None:
    service, _ = create_service()

    robot = service.get_robot(999)

    assert robot is None


def test_create_robot() -> None:
    service, repository = create_service()

    robot = FakeRobotRepository._create_robot(
        robot_id=None,
        nome="Novo robô",
        ativo=False,
    )

    created_robot = service.create_robot(robot)

    assert created_robot.id is not None
    assert created_robot.nome == "Novo robô"
    assert repository.find_by_id(created_robot.id) is created_robot


def test_create_robot_rejects_robot_with_id() -> None:
    service, _ = create_service()

    robot = FakeRobotRepository._create_robot(
        robot_id=100,
        nome="Novo robô",
        ativo=False,
    )

    with pytest.raises(
        ValueError,
        match="Um novo robô não deve possuir ID",
    ):
        service.create_robot(robot)


def test_update_robot() -> None:
    service, repository = create_service()

    updated_robot = service.update_robot(
        robot_id=51,
        nome="Robô atualizado",
        descricao="Nova descrição",
    )

    assert updated_robot.id == 51
    assert updated_robot.nome == "Robô atualizado"
    assert updated_robot.descricao == "Nova descrição"

    stored_robot = repository.find_by_id(51)

    assert stored_robot is not None
    assert stored_robot.nome == "Robô atualizado"
    assert stored_robot.descricao == "Nova descrição"


def test_update_robot_raises_when_not_found() -> None:
    service, _ = create_service()

    with pytest.raises(
        ValueError,
        match="Robô 999 não encontrado",
    ):
        service.update_robot(
            robot_id=999,
            nome="Robô",
            descricao="Descrição",
        )


def test_update_robot_rejects_empty_name() -> None:
    service, _ = create_service()

    with pytest.raises(
        ValueError,
        match="O nome do robô é obrigatório",
    ):
        service.update_robot(
            robot_id=51,
            nome="   ",
            descricao="Descrição",
        )


def test_activate_robot() -> None:
    service, repository = create_service()

    robot = service.activate_robot(52)

    assert robot.id == 52
    assert robot.ativo is True

    stored_robot = repository.find_by_id(52)

    assert stored_robot is not None
    assert stored_robot.ativo is True


def test_activate_robot_raises_when_not_found() -> None:
    service, _ = create_service()

    with pytest.raises(
        ValueError,
        match="Robô 999 não encontrado",
    ):
        service.activate_robot(999)


def test_deactivate_robot() -> None:
    service, repository = create_service()

    robot = service.deactivate_robot(51)

    assert robot.id == 51
    assert robot.ativo is False

    stored_robot = repository.find_by_id(51)

    assert stored_robot is not None
    assert stored_robot.ativo is False


def test_deactivate_robot_raises_when_not_found() -> None:
    service, _ = create_service()

    with pytest.raises(
        ValueError,
        match="Robô 999 não encontrado",
    ):
        service.deactivate_robot(999)


def test_delete_robot() -> None:
    service, repository = create_service()

    service.delete_robot(52)

    assert repository.find_by_id(52) is None


def test_delete_robot_raises_when_not_found() -> None:
    service, _ = create_service()

    with pytest.raises(
        ValueError,
        match="Robô 999 não encontrado",
    ):
        service.delete_robot(999)


def test_delete_active_robot_raises() -> None:
    service, _ = create_service()

    with pytest.raises(
        ValueError,
        match="Não é permitido excluir um robô ativo",
    ):
        service.delete_robot(51)