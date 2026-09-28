from collections.abc import Callable

import flet as ft

from gestao_robos.core.theme import AppTheme


class LoginPage:
    """Tela de autenticação da aplicação."""

    def __init__(
        self,
        page: ft.Page,
        on_login: Callable[[str, str], bool],
    ) -> None:
        self.page = page
        self.on_login = on_login

        self.username = ft.TextField(
            label="Usuário",
            hint_text="Digite seu usuário",
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            width=AppTheme.INPUT_WIDTH,
            height=AppTheme.INPUT_HEIGHT,
            autofocus=True,
            border_radius=8,
            border_color=AppTheme.BORDER,
            focused_border_color=AppTheme.PRIMARY,
            filled=True,
            fill_color=AppTheme.BACKGROUND,
        )

        self.password = ft.TextField(
            label="Senha",
            hint_text="Digite sua senha",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            width=AppTheme.INPUT_WIDTH,
            height=AppTheme.INPUT_HEIGHT,
            password=True,
            can_reveal_password=True,
            border_radius=8,
            border_color=AppTheme.BORDER,
            focused_border_color=AppTheme.PRIMARY,
            filled=True,
            fill_color=AppTheme.BACKGROUND,
            on_submit=self._submit_password,
        )

        self.error_message = ft.Text(
            color=AppTheme.ERROR,
            size=13,
            visible=False,
            width=AppTheme.INPUT_WIDTH,
            text_align=ft.TextAlign.CENTER,
        )

        self.login_button = ft.Button(
            content="Entrar",
            width=AppTheme.INPUT_WIDTH,
            height=AppTheme.BUTTON_HEIGHT,
            on_click=self._login,
        )

    def _submit_password(self, e: ft.Event[ft.TextField]) -> None:
        """Processa o envio do formulário pelo campo de senha."""
        self._perform_login()

    def _login(self, e: ft.Event[ft.Button]) -> None:
        """Processa o clique no botão de login."""
        self._perform_login()

    def _perform_login(self) -> None:
        """Valida as credenciais e realiza o login."""

        username = self.username.value.strip()
        password = self.password.value

        self.error_message.visible = False

        if not username or not password:
            self._show_error("Informe usuário e senha.")
            return

        authenticated = self.on_login(
            username,
            password,
        )

        if not authenticated:
            self._show_error("Usuário ou senha inválidos.")
            return

        self.page.update()

    def _show_error(self, message: str) -> None:
        """Exibe uma mensagem de erro no formulário."""
        self.error_message.value = message
        self.error_message.visible = True
        self.page.update()

    def _build_header(self) -> ft.Control:
        """Cria o cabeçalho do card de login."""

        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Container(
                    width=72,
                    height=72,
                    border_radius=36,
                    bgcolor=AppTheme.PRIMARY_CONTAINER,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        ft.Icons.SMART_TOY_OUTLINED,
                        size=38,
                        color=AppTheme.PRIMARY,
                    ),
                ),
                ft.Container(height=4),
                ft.Text(
                    "Gestão de Robôs",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=AppTheme.TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Acesse sua conta para continuar",
                    size=14,
                    color=AppTheme.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        )

    def _build_form(self) -> ft.Control:
        """Cria o formulário de autenticação."""

        return ft.Column(
            spacing=14,
            controls=[
                self.username,
                self.password,
                ft.Container(
                    width=AppTheme.INPUT_WIDTH,
                    height=20,
                    alignment=ft.Alignment.CENTER,
                    content=self.error_message,
                ),
                self.login_button,
            ],
        )

    def _build_login_card(self) -> ft.Control:
        """Cria o card principal de autenticação."""

        return ft.Container(
            width=AppTheme.LOGIN_CARD_WIDTH,
            padding=AppTheme.LOGIN_CARD_PADDING,
            bgcolor=AppTheme.SURFACE,
            border_radius=16,
            shadow=ft.BoxShadow(
                blur_radius=24,
                spread_radius=1,
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=24,
                controls=[
                    self._build_header(),
                    self._build_form(),
                ],
            ),
        )

    def build(self) -> ft.Control:
        """Constrói a tela de login completa."""

        return ft.Container(
            expand=True,
            bgcolor=AppTheme.BACKGROUND,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self._build_login_card(),
                    ft.Container(height=16),
                    ft.Text(
                        "Gestão de Robôs",
                        size=12,
                        color=AppTheme.TEXT_SECONDARY,
                    ),
                ],
            ),
        )
