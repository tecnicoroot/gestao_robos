import os
from collections.abc import Generator
from contextlib import contextmanager

import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


class DatabaseConnection:
    """Gerencia conexões com o banco MySQL."""

    def __init__(self) -> None:
        self.host = self._get_required_setting("DB_HOST")
        self.port = int(os.getenv("DB_PORT", "3306"))
        self.database = self._get_required_setting("DB_NAME")
        self.user = self._get_required_setting("DB_USER")
        self.password = self._get_required_setting("DB_PASSWORD")

    @staticmethod
    def _get_required_setting(name: str) -> str:
        """Obtém uma configuração obrigatória do ambiente."""

        value = os.getenv(name)

        if not value:
            raise RuntimeError(f"A variável de ambiente {name} não foi configurada.")

        return value

    def connect(
        self,
    ) -> MySQLConnectionAbstract | PooledMySQLConnection:
        """Abre uma conexão com o banco."""
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )

    @contextmanager
    def connection(
        self,
    ) -> Generator[MySQLConnectionAbstract | PooledMySQLConnection]:
        """Fornece uma conexão e garante seu fechamento."""
        connection = self.connect()

        try:
            yield connection
        finally:
            connection.close()
