from collections.abc import Generator
from contextlib import contextmanager

import pymysql
from pymysql.connections import Connection

from gestao_robos.infrastructure.database.settings import (
    DatabaseSettings,
)


class DatabaseConnection:
    """Gerencia conexões com o banco MySQL."""

    def __init__(self, settings: DatabaseSettings) -> None:
        self.settings = settings

    @contextmanager
    def connection(self) -> Generator[Connection]:
        """Abre uma conexão com o banco e garante seu fechamento."""
        connection = pymysql.connect(
            host=self.settings.mysql.host,
            port=self.settings.mysql.port,
            database=self.settings.mysql.database,
            user=self.settings.mysql.username,
            password=self.settings.mysql.password,
        )

        try:
            yield connection
        finally:
            connection.close()