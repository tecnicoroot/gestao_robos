from __future__ import annotations

import sqlite3
from datetime import time

from gestao_robos.domain.entities.robot import Robot
from gestao_robos.infrastructure.database.sqlite_robot_repository import (
    SQLiteRobotRepository,
)


def seed_database(connection: sqlite3.Connection) -> None:
    """Popula o SQLite com dados fictícios para desenvolvimento."""
    repository = SQLiteRobotRepository(connection)

    if repository.find_all():
        return

    robots = [
        Robot(
            id=None,
            nome="Robô Financeiro",
            descricao="Processamento automático do setor financeiro.",
            ativo=True,
            intervalo=180,
            acao="A",
            tela="N",
            path_executavel=r"C:\robos\financeiro",
            limite_tempo=480,
            arquivo_ativacao="",
            nome_executavel="financeiro.exe",
            pasta_trabalho=r"C:\robos\financeiro\dados",
            repositorio_planilhas=r"C:\robos\financeiro\planilhas",
            notificados="financeiro@empresa.com",
            pgm_ativado1="",
            pgm_ativado2="",
            robo_sequencia=None,
            usuario_robo="financeiro",
            robo_teste=0,
            horario_ativacao=None,
            codigo_setor=5,
            biblioteca="",
        ),
        Robot(
            id=None,
            nome="Robô Cadastro",
            descricao="Atualização automática dos cadastros.",
            ativo=False,
            intervalo=300,
            acao="U",
            tela="S",
            path_executavel=r"C:\robos\cadastro",
            limite_tempo=300,
            arquivo_ativacao=r"C:\robos\cadastro\config.ini",
            nome_executavel="cadastro.exe",
            pasta_trabalho=r"C:\robos\cadastro\dados",
            repositorio_planilhas=r"C:\robos\cadastro\planilhas",
            notificados="cadastro@empresa.com",
            pgm_ativado1="javaw.exe",
            pgm_ativado2="",
            robo_sequencia=None,
            usuario_robo="cadastro",
            robo_teste=0,
            horario_ativacao=None,
            codigo_setor=6,
            biblioteca="",
        ),
        Robot(
            id=None,
            nome="Robô Contas Médicas",
            descricao="Processamento de contas médicas.",
            ativo=True,
            intervalo=120,
            acao="H",
            tela="N",
            path_executavel=r"C:\robos\contas_medicas",
            limite_tempo=600,
            arquivo_ativacao="",
            nome_executavel="contas_medicas.exe",
            pasta_trabalho=r"C:\robos\contas_medicas\dados",
            repositorio_planilhas=r"C:\robos\contas_medicas\planilhas",
            notificados="contas@empresa.com;gestao@empresa.com",
            pgm_ativado1="",
            pgm_ativado2="",
            robo_sequencia=None,
            usuario_robo="contas_medicas",
            robo_teste=0,
            horario_ativacao=time(8, 30),
            codigo_setor=4,
            biblioteca="",
        ),
        Robot(
            id=None,
            nome=(
                "Robô com nome extremamente longo para testar "
                "o comportamento visual da tabela"
            ),
            descricao=(
                "Descrição propositalmente extensa para verificar "
                "quebra, truncamento e rolagem da interface."
            ),
            ativo=False,
            intervalo=600,
            acao="A",
            tela="S",
            path_executavel=(
                r"C:\robos\diretorio_muito_longo\\"
                r"subdiretorio\executaveis"
            ),
            limite_tempo=900,
            arquivo_ativacao=r"C:\robos\config\ativacao.ini",
            nome_executavel="robo_teste_interface.exe",
            pasta_trabalho=r"C:\robos\dados\trabalho",
            repositorio_planilhas=r"C:\robos\dados\planilhas",
            notificados="teste@empresa.com",
            pgm_ativado1="programa1.exe",
            pgm_ativado2="programa2.exe",
            robo_sequencia=None,
            usuario_robo="usuario_teste",
            robo_teste=1,
            horario_ativacao=time(23, 45),
            codigo_setor=1,
            biblioteca="",
        ),
        Robot(
            id=None,
            nome="Robô Exclusão Bloqueada",
            descricao="Usado para testar a exclusão de robô ativo.",
            ativo=True,
            intervalo=60,
            acao="A",
            tela="N",
            path_executavel=r"C:\robos\exclusao",
            limite_tempo=180,
            arquivo_ativacao="",
            nome_executavel="exclusao.exe",
            pasta_trabalho=r"C:\robos\exclusao\dados",
            repositorio_planilhas="",
            notificados="teste@empresa.com",
            pgm_ativado1="",
            pgm_ativado2="",
            robo_sequencia=None,
            usuario_robo="teste",
            robo_teste=1,
            horario_ativacao=None,
            codigo_setor=8,
            biblioteca="",
        ),
        Robot(
            id=None,
            nome="Robô Agendamento",
            descricao="Robô para execução programada.",
            ativo=False,
            intervalo=900,
            acao="H",
            tela="N",
            path_executavel=r"C:\robos\agendamento",
            limite_tempo=1200,
            arquivo_ativacao="",
            nome_executavel="agendamento.exe",
            pasta_trabalho=r"C:\robos\agendamento\dados",
            repositorio_planilhas=r"C:\robos\agendamento\planilhas",
            notificados="agenda@empresa.com",
            pgm_ativado1="",
            pgm_ativado2="",
            robo_sequencia=None,
            usuario_robo="agendamento",
            robo_teste=0,
            horario_ativacao=time(7, 0),
            codigo_setor=9,
            biblioteca="",
        ),
    ]

    for robot in robots:
        repository.save(robot)