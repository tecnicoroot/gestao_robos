import flet as ft

from gestao_robos.core.theme import AppTheme
from gestao_robos.services.authentication import AuthenticationService
from gestao_robos.ui.login_page import LoginPage
from gestao_robos.ui.main_page import MainPage


class App:
    """Controla o fluxo principal da aplicação."""

    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.authentication = AuthenticationService()
        self.current_user: str | None = None

        self._configure_page()

    def _configure_page(self) -> None:
        self.page.title = "Gestão de Robôs"

        self.page.window.width = 1000
        self.page.window.height = 700

        self.page.window.min_width = 800
        self.page.window.min_height = 500

        AppTheme.configure(self.page)

    def start(self) -> None:
        """Inicia a aplicação exibindo a tela de login."""
        self.show_login()

    def show_login(self) -> None:
        """Exibe a tela de login."""

        self.current_user = None

        login_page = LoginPage(
            page=self.page,
            on_login=self._authenticate,
        )

        self.page.clean()
        self.page.add(login_page.build())
        self.page.update()

    def _authenticate(
        self,
        username: str,
        password: str,
    ) -> bool:
        """Autentica o usuário."""

        authenticated = self.authentication.authenticate(
            username,
            password,
        )

        if not authenticated:
            return False

        self.current_user = username

        self.show_main()

        return True

    def show_main(self) -> None:
        """Exibe a tela principal."""

        if self.current_user is None:
            self.show_login()
            return

        main_page = MainPage(
            page=self.page,
            username=self.current_user,
            on_logout=self.show_login,
        )

        self.page.clean()
        self.page.add(main_page.build())
        self.page.update()