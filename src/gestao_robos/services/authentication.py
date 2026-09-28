class AuthenticationService:
    """Responsável pela autenticação dos usuários."""

    def authenticate(self, username: str, password: str) -> bool:
        """Valida as credenciais do usuário.

        Esta implementação é apenas para desenvolvimento.
        """
        return username == "admin" and password == "123456"
