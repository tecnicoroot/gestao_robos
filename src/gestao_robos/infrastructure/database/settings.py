from dataclasses import dataclass


@dataclass(frozen=True)
class SshSettings:
    """Configurações da conexão SSH."""

    host: str
    port: int
    username: str
    password: str


@dataclass(frozen=True)
class MysqlSettings:
    """Configurações da conexão MySQL."""

    host: str
    port: int
    database: str
    username: str
    password: str


@dataclass(frozen=True)
class DatabaseSettings:
    """Configurações completas de acesso ao banco."""

    ssh: SshSettings
    mysql: MysqlSettings