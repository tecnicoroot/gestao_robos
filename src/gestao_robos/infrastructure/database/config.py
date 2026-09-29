import os
from pathlib import Path

from dotenv import load_dotenv

from gestao_robos.infrastructure.database.settings import (
    DatabaseSettings,
    MysqlSettings,
    SshSettings,
)
from gestao_robos.infrastructure.security.credentials import CredentialLoader

load_dotenv()


def _get_required_env(name: str) -> str:
    """Retorna uma variável de ambiente obrigatória."""
    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"A variável de ambiente '{name}' não foi configurada."
        )

    return value


def load_database_settings() -> DatabaseSettings:
    """Carrega as credenciais e monta as configurações do banco."""

    key_path = Path(_get_required_env("GESTAO_ROBOS_KEY_PATH"))
    config_path = Path(_get_required_env("GESTAO_ROBOS_CONFIG_PATH"))

    credentials = CredentialLoader(
        key_path=key_path,
        config_path=config_path,
    ).load()

    if len(credentials) <= 17:
        raise ValueError(
            "Arquivo de configuração não contém as credenciais esperadas."
        )

    ssh_password = credentials[16]
    mysql_password = credentials[17]

    return DatabaseSettings(
        ssh=SshSettings(
            host="dbmysqlnx",
            port=22,
            username="root",
            password=ssh_password,
        ),
        mysql=MysqlSettings(
            host="127.0.0.1",
            port=3306,
            database="bdrpajf",
            username="rpaujf",
            password=mysql_password,
        ),
    )