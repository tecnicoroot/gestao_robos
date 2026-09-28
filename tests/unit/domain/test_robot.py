from datetime import time

import pytest

from gestao_robos.domain.entities.robot import Robot


def create_robot() -> Robot:
    """Cria um robô válido para os testes."""

    return Robot(
        id=None,
        nome="Robô Financeiro",
        descricao="Processa informações financeiras.",
        ativo=False,
        intervalo=60,
        acao="A",
        tela="N",
        path_executavel=r"C:\robos",
        limite_tempo=120,
        arquivo_ativacao="",
        nome_executavel="financeiro.exe",
        pasta_trabalho=r"C:\robos\dados",
        repositorio_planilhas=r"C:\robos\dados",
        notificados="teste@example.com",
        pgm_ativado1="javaw.exe",
        pgm_ativado2="",
        robo_sequencia=0,
        usuario_robo="USUARIO.ROBO",
        robo_teste=0,
        horario_ativacao=time(0, 0, 0),
        codigo_setor=1,
        biblioteca="",
    )


def test_robot_is_created_inactive() -> None:
    robot = create_robot()

    assert robot.nome == "Robô Financeiro"
    assert robot.ativo is False


def test_robot_can_be_activated() -> None:
    robot = create_robot()

    robot.activate()

    assert robot.ativo is True


def test_robot_can_be_deactivated() -> None:
    robot = create_robot()

    robot.activate()
    robot.deactivate()

    assert robot.ativo is False


def test_robot_can_be_updated() -> None:
    robot = create_robot()

    robot.update(
        nome="Robô Contábil",
        descricao="Processa informações contábeis.",
    )

    assert robot.nome == "Robô Contábil"
    assert robot.descricao == "Processa informações contábeis."


def test_robot_requires_name() -> None:
    with pytest.raises(
        ValueError,
        match="O nome do robô é obrigatório.",
    ):
        Robot(
            id=None,
            nome="",
            descricao="",
            ativo=False,
            intervalo=60,
            acao="A",
            tela="N",
            path_executavel="",
            limite_tempo=60,
            arquivo_ativacao="",
            nome_executavel="",
            pasta_trabalho="",
            repositorio_planilhas="",
            notificados="",
            pgm_ativado1="",
            pgm_ativado2="",
            robo_sequencia=0,
            usuario_robo="",
            robo_teste=0,
            horario_ativacao=time(0, 0, 0),
            codigo_setor=0,
            biblioteca="",
        )
