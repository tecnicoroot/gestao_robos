from pathlib import Path

from cryptography.fernet import Fernet


class CredentialLoader:
    """Carrega e descriptografa as credenciais da aplicação."""

    def __init__(
        self,
        key_path: Path,
        config_path: Path,
    ) -> None:
        self.key_path = key_path
        self.config_path = config_path

    def load(self) -> list[str]:
        """Descriptografa o arquivo e retorna os valores configurados."""
        key = self.key_path.read_bytes()
        encrypted_data = self.config_path.read_bytes()

        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)

        return decrypted_data.decode().split(";")