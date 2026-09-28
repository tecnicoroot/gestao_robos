from pathlib import Path

from gestao_robos.infrastructure.database.settings import (
    DatabaseSettings,
    MysqlSettings,
    SshSettings,
)
from gestao_robos.infrastructure.security.credentials import CredentialLoader


def load_database_settings(
    key_path: Path,
    config_path: Path,
) -> DatabaseSettings:
    """Carrega as credenciais e monta as configurações do banco."""

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