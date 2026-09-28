from collections.abc import Generator
from contextlib import contextmanager

import pymysql
from pymysql.connections import Connection
from sshtunnel import SSHTunnelForwarder  # type: ignore[import-untyped]

from gestao_robos.infrastructure.database.settings import DatabaseSettings


class DatabaseConnection:
    """Gerencia conexões MySQL através de um túnel SSH."""

    def __init__(self, settings: DatabaseSettings) -> None:
        self.settings = settings

    @contextmanager
    def connection(self) -> Generator[Connection]:
        """Abre uma conexão MySQL através de um túnel SSH."""

        ssh = self.settings.ssh
        mysql = self.settings.mysql

        with SSHTunnelForwarder(
            (ssh.host, ssh.port),
            ssh_username=ssh.username,
            ssh_password=ssh.password,
            remote_bind_address=(mysql.host, mysql.port),
        ) as tunnel:
            connection = pymysql.connect(
                host="127.0.0.1",
                port=tunnel.local_bind_port,
                database=mysql.database,
                user=mysql.username,
                password=mysql.password,
            )

            try:
                yield connection
            finally:
                connection.close()