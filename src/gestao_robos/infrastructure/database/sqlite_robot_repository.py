from __future__ import annotations

import sqlite3
from datetime import time
from typing import Any

from gestao_robos.domain.entities.robot import Robot
from gestao_robos.repositories.robot_repository import RobotRepository


class SQLiteRobotRepository(RobotRepository):
    """Repositório de robôs usando SQLite."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    def find_all(self) -> list[Robot]:
        """Retorna todos os robôs."""
        cursor = self.connection.execute(
            """
            SELECT
                id,
                nome,
                descricao,
                ativo,
                intervalo,
                acao,
                tela,
                path_executavel,
                limite_tempo,
                arquivo_ativacao,
                nome_executavel,
                pasta_trabalho,
                repositorio_planilhas,
                notificados,
                pgm_ativado1,
                pgm_ativado2,
                robo_sequencia,
                usuario_robo,
                robo_teste,
                horario_ativacao,
                codigo_setor,
                biblioteca
            FROM robos
            ORDER BY id
            """
        )

        return [
            self._row_to_robot(row)
            for row in cursor.fetchall()
        ]

    def find_by_id(self, robot_id: int) -> Robot | None:
        """Busca um robô pelo ID."""
        cursor = self.connection.execute(
            """
            SELECT
                id,
                nome,
                descricao,
                ativo,
                intervalo,
                acao,
                tela,
                path_executavel,
                limite_tempo,
                arquivo_ativacao,
                nome_executavel,
                pasta_trabalho,
                repositorio_planilhas,
                notificados,
                pgm_ativado1,
                pgm_ativado2,
                robo_sequencia,
                usuario_robo,
                robo_teste,
                horario_ativacao,
                codigo_setor,
                biblioteca
            FROM robos
            WHERE id = ?
            """,
            (robot_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_robot(row)

    def save(self, robot: Robot) -> Robot:
        """Insere ou atualiza um robô."""
        if robot.id is None:
            return self._insert(robot)

        return self._update(robot)

    def delete(self, robot_id: int) -> None:
        """Exclui um robô."""
        self.connection.execute(
            """
            DELETE FROM robos
            WHERE id = ?
            """,
            (robot_id,),
        )
        self.connection.commit()

    def _insert(self, robot: Robot) -> Robot:
        cursor = self.connection.execute(
            """
            INSERT INTO robos (
                nome,
                descricao,
                ativo,
                intervalo,
                acao,
                tela,
                path_executavel,
                limite_tempo,
                arquivo_ativacao,
                nome_executavel,
                pasta_trabalho,
                repositorio_planilhas,
                notificados,
                pgm_ativado1,
                pgm_ativado2,
                robo_sequencia,
                usuario_robo,
                robo_teste,
                horario_ativacao,
                codigo_setor,
                biblioteca
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            self._robot_parameters(robot),
        )

        self.connection.commit()

        robot.id = cursor.lastrowid

        return robot

    def _update(self, robot: Robot) -> Robot:
        self.connection.execute(
            """
            UPDATE robos
            SET
                nome = ?,
                descricao = ?,
                ativo = ?,
                intervalo = ?,
                acao = ?,
                tela = ?,
                path_executavel = ?,
                limite_tempo = ?,
                arquivo_ativacao = ?,
                nome_executavel = ?,
                pasta_trabalho = ?,
                repositorio_planilhas = ?,
                notificados = ?,
                pgm_ativado1 = ?,
                pgm_ativado2 = ?,
                robo_sequencia = ?,
                usuario_robo = ?,
                robo_teste = ?,
                horario_ativacao = ?,
                codigo_setor = ?,
                biblioteca = ?
            WHERE id = ?
            """,
            (
                *self._robot_parameters(robot),
                robot.id,
            ),
        )

        self.connection.commit()

        return robot

    def _create_table(self) -> None:
        """Cria a tabela de robôs caso ainda não exista."""
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS robos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                ativo INTEGER NOT NULL,
                intervalo INTEGER NOT NULL,
                acao TEXT NOT NULL,
                tela TEXT NOT NULL,
                path_executavel TEXT NOT NULL,
                limite_tempo INTEGER NOT NULL,
                arquivo_ativacao TEXT NOT NULL,
                nome_executavel TEXT NOT NULL,
                pasta_trabalho TEXT NOT NULL,
                repositorio_planilhas TEXT NOT NULL,
                notificados TEXT NOT NULL,
                pgm_ativado1 TEXT NOT NULL,
                pgm_ativado2 TEXT NOT NULL,
                robo_sequencia INTEGER,
                usuario_robo TEXT NOT NULL,
                robo_teste INTEGER NOT NULL,
                horario_ativacao TEXT,
                codigo_setor INTEGER NOT NULL,
                biblioteca TEXT NOT NULL
            )
            """
        )

        self.connection.commit()

    @staticmethod
    def _robot_parameters(
        robot: Robot,
    ) -> tuple[int | str | None, ...]:
        """Converte Robot para parâmetros do SQLite."""
        horario_ativacao: str | None = None

        if robot.horario_ativacao is not None:
            horario_ativacao = robot.horario_ativacao.strftime(
                "%H:%M:%S"
            )

        return (
            robot.nome,
            robot.descricao,
            int(robot.ativo),
            robot.intervalo,
            robot.acao,
            robot.tela,
            robot.path_executavel,
            robot.limite_tempo,
            robot.arquivo_ativacao,
            robot.nome_executavel,
            robot.pasta_trabalho,
            robot.repositorio_planilhas,
            robot.notificados,
            robot.pgm_ativado1,
            robot.pgm_ativado2,
            robot.robo_sequencia,
            robot.usuario_robo,
            robot.robo_teste,
            horario_ativacao,
            robot.codigo_setor,
            robot.biblioteca,
        )

    @staticmethod
    def _row_to_robot(row: sqlite3.Row) -> Robot:
        """Converte uma linha SQLite em Robot."""
        horario_ativacao = SQLiteRobotRepository._parse_time(
            row["horario_ativacao"]
        )

        return Robot(
            id=int(row["id"]),
            nome=str(row["nome"]),
            descricao=str(row["descricao"]),
            ativo=bool(row["ativo"]),
            intervalo=int(row["intervalo"]),
            acao=str(row["acao"]),
            tela=str(row["tela"]),
            path_executavel=str(row["path_executavel"]),
            limite_tempo=int(row["limite_tempo"]),
            arquivo_ativacao=str(row["arquivo_ativacao"]),
            nome_executavel=str(row["nome_executavel"]),
            pasta_trabalho=str(row["pasta_trabalho"]),
            repositorio_planilhas=str(row["repositorio_planilhas"]),
            notificados=str(row["notificados"]),
            pgm_ativado1=str(row["pgm_ativado1"]),
            pgm_ativado2=str(row["pgm_ativado2"]),
            robo_sequencia=(
                int(row["robo_sequencia"])
                if row["robo_sequencia"] is not None
                else None
            ),
            usuario_robo=str(row["usuario_robo"]),
            robo_teste=int(row["robo_teste"]),
            horario_ativacao=horario_ativacao,
            codigo_setor=int(row["codigo_setor"]),
            biblioteca=str(row["biblioteca"]),
        )

    @staticmethod
    def _parse_time(value: Any) -> time | None:
        """Converte horário armazenado no SQLite."""
        if value is None:
            return None

        if isinstance(value, time):
            return value

        value = str(value)

        if not value:
            return None

        parts = value.split(":")

        if len(parts) < 2:
            raise ValueError(
                f"Horário inválido no SQLite: {value}"
            )

        return time(
            hour=int(parts[0]),
            minute=int(parts[1]),
            second=int(parts[2]) if len(parts) > 2 else 0,
        )