from datetime import time
from typing import Any, cast

from gestao_robos.domain.entities.robot import Robot
from gestao_robos.infrastructure.database.connection import DatabaseConnection
from gestao_robos.repositories.robot_repository import RobotRepository

type RobotRow = dict[str, Any]
type MySQLParameter = int | str | time | None


class MySQLRobotRepository(RobotRepository):
    """Implementa a persistência de robôs no MySQL."""

    def __init__(self, database: DatabaseConnection) -> None:
        self.database = database

    def find_all(self) -> list[Robot]:
        """Retorna todos os robôs."""

        query = """
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
            ORDER BY nome
        """

        with self.database.connection() as connection:
            cursor = connection.cursor(dictionary=True)

            try:
                cursor.execute(query)
                rows = cast(
                    list[RobotRow],
                    cursor.fetchall(),
                )

                return [self._row_to_robot(row) for row in rows]
            finally:
                cursor.close()

    def find_by_id(self, robot_id: int) -> Robot | None:
        """Busca um robô pelo ID."""

       
        with self.database.connection() as connection:
            cursor = connection.cursor(dictionary=True)

            try:
                row = cursor.fetchone()

                if row is None:
                    return None

                return self._row_to_robot(
                    cast(RobotRow, row),
                )

            finally:
                cursor.close()

    def save(self, robot: Robot) -> Robot:
        """Cria ou atualiza um robô."""

        if robot.id is None:
            return self._insert(robot)

        self._update(robot)

        return robot

    def delete(self, robot_id: int) -> None:
        """Remove um robô."""

        query = """
            DELETE FROM robos
            WHERE id = %s
        """

        with self.database.connection() as connection:
            cursor = connection.cursor()

            try:
                cursor.execute(query, (robot_id,))
                connection.commit()
            finally:
                cursor.close()

    def _insert(self, robot: Robot) -> Robot:
        """Insere um novo robô."""

        query = """
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
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )
        """

        parameters = self._robot_parameters(robot)

        with self.database.connection() as connection:
            cursor = connection.cursor()

            try:
                cursor.execute(query, parameters)
                connection.commit()

                robot.id = cursor.lastrowid

                return robot
            finally:
                cursor.close()

    def _update(self, robot: Robot) -> None:
        """Atualiza um robô existente."""

        query = """
            UPDATE robos
            SET
                nome = %s,
                descricao = %s,
                ativo = %s,
                intervalo = %s,
                acao = %s,
                tela = %s,
                path_executavel = %s,
                limite_tempo = %s,
                arquivo_ativacao = %s,
                nome_executavel = %s,
                pasta_trabalho = %s,
                repositorio_planilhas = %s,
                notificados = %s,
                pgm_ativado1 = %s,
                pgm_ativado2 = %s,
                robo_sequencia = %s,
                usuario_robo = %s,
                robo_teste = %s,
                horario_ativacao = %s,
                codigo_setor = %s,
                biblioteca = %s
            WHERE id = %s
        """

        parameters = (
            *self._robot_parameters(robot),
            robot.id,
        )

        with self.database.connection() as connection:
            cursor = connection.cursor()

            try:
                cursor.execute(query, parameters)
                connection.commit()
            finally:
                cursor.close()

    @staticmethod
    def _robot_parameters(robot: Robot) -> tuple[MySQLParameter, ...]:
        """Converte Robot para os parâmetros do SQL."""

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
            robot.horario_ativacao,
            robot.codigo_setor,
            robot.biblioteca,
        )

    @staticmethod
    def _get_int(
        row: dict[str, object],
        column: str,
    ) -> int:
        """Obtém um valor inteiro de uma linha do banco."""

        value = row[column]

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            return int(value)

        raise TypeError(f"Valor inválido para {column}: {value!r}")

    @staticmethod
    def _get_str(
        row: dict[str, object],
        column: str,
    ) -> str:
        """Obtém uma string de uma linha do banco."""

        value = row[column]

        if value is None:
            return ""

        if isinstance(value, str):
            return value

        raise TypeError(f"Valor inválido para {column}: {value!r}")

    @staticmethod
    def _get_time(
        row: dict[str, object],
        column: str,
    ) -> time:
        """Obtém um horário de uma linha do banco."""

        value = row[column]

        if isinstance(value, time):
            return value

        raise TypeError(f"Valor inválido para {column}: {value!r}")

    @classmethod
    def _row_to_robot(cls, row: RobotRow) -> Robot:
        """Converte uma linha do banco em Robot."""

        return Robot(
            id=cls._get_int(row, "id"),
            nome=cls._get_str(row, "nome"),
            descricao=cls._get_str(row, "descricao"),
            ativo=bool(cls._get_int(row, "ativo")),
            intervalo=cls._get_int(row, "intervalo"),
            acao=cls._get_str(row, "acao"),
            tela=cls._get_str(row, "tela"),
            path_executavel=cls._get_str(
                row,
                "path_executavel",
            ),
            limite_tempo=cls._get_int(
                row,
                "limite_tempo",
            ),
            arquivo_ativacao=cls._get_str(
                row,
                "arquivo_ativacao",
            ),
            nome_executavel=cls._get_str(
                row,
                "nome_executavel",
            ),
            pasta_trabalho=cls._get_str(
                row,
                "pasta_trabalho",
            ),
            repositorio_planilhas=cls._get_str(
                row,
                "repositorio_planilhas",
            ),
            notificados=cls._get_str(
                row,
                "notificados",
            ),
            pgm_ativado1=cls._get_str(
                row,
                "pgm_ativado1",
            ),
            pgm_ativado2=cls._get_str(
                row,
                "pgm_ativado2",
            ),
            robo_sequencia=cls._get_int(
                row,
                "robo_sequencia",
            ),
            usuario_robo=cls._get_str(
                row,
                "usuario_robo",
            ),
            robo_teste=cls._get_int(
                row,
                "robo_teste",
            ),
            horario_ativacao=cls._get_time(
                row,
                "horario_ativacao",
            ),
            codigo_setor=cls._get_int(
                row,
                "codigo_setor",
            ),
            biblioteca=cls._get_str(
                row,
                "biblioteca",
            ),
        )
