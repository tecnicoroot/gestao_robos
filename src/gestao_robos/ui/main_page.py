from collections.abc import Callable

import flet as ft

from gestao_robos.core.theme import AppTheme
from gestao_robos.ui.dashboard_page import DashboardPage
from gestao_robos.ui.executions_page import ExecutionsPage
from gestao_robos.ui.robots_page import RobotsPage


class MainPage:
    """Tela principal da aplicação."""

    def __init__(
        self,
        page: ft.Page,
        username: str,
        on_logout: Callable[[], None],
    ) -> None:
        self.page = page
        self.username = username
        self.on_logout = on_logout

        self.content_area = ft.Container(
            expand=True,
        )
        self.selected_page = "dashboard"
        self.navigation_items: dict[str, ft.Container] = {}
        self.navigation_hover: dict[str, bool] = {}
        self.page_title = ft.Text(
            "Dashboard",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=AppTheme.TEXT_PRIMARY,
        )

    def _get_page_title(self) -> str:
        """Retorna o título da página selecionada."""

        titles = {
            "dashboard": "Dashboard",
            "robots": "Robôs",
            "executions": "Execuções",
        }

        return titles.get(
            self.selected_page,
            "Dashboard",
        )

    def build(self) -> ft.Control:
        """Constrói a tela principal."""

        return ft.Row(
            expand=True,
            spacing=0,
            controls=[
                self._build_sidebar(),
                ft.VerticalDivider(
                    width=1,
                    thickness=1,
                ),
                self._build_content(),
            ],
        )

    def _build_sidebar(self) -> ft.Control:
        """Cria a barra lateral."""

        return ft.Container(
            width=AppTheme.SIDEBAR_WIDTH,
            bgcolor=AppTheme.SURFACE,
            padding=16,
            content=ft.Column(
                spacing=8,
                controls=[
                    self._build_sidebar_header(),
                    ft.Container(height=16),
                    self._build_navigation(),
                    ft.Container(expand=True),
                    self._build_user_area(),
                ],
            ),
        )

    def _build_sidebar_header(self) -> ft.Control:
        """Cria o cabeçalho da barra lateral."""

        return ft.Row(
            spacing=12,
            controls=[
                ft.Container(
                    width=42,
                    height=42,
                    border_radius=21,
                    bgcolor=AppTheme.PRIMARY_CONTAINER,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        ft.Icons.SMART_TOY_OUTLINED,
                        color=AppTheme.PRIMARY,
                        size=24,
                    ),
                ),
                ft.Text(
                    "Gestão de Robôs",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=AppTheme.TEXT_PRIMARY,
                ),
            ],
        )

    def _build_navigation(self) -> ft.Control:
        """Cria os itens de navegação."""

        return ft.Column(
            spacing=4,
            controls=[
                self._build_navigation_item(
                    icon=ft.Icons.DASHBOARD_OUTLINED,
                    label="Dashboard",
                    page_key="dashboard",
                ),
                self._build_navigation_item(
                    icon=ft.Icons.SMART_TOY_OUTLINED,
                    label="Robôs",
                    page_key="robots",
                ),
                self._build_navigation_item(
                    icon=ft.Icons.PLAY_CIRCLE_OUTLINE,
                    label="Execuções",
                    page_key="executions",
                ),
            ],
        )

    def _build_navigation_item(
        self,
        icon: ft.IconData,
        label: str,
        page_key: str,
    ) -> ft.Container:
        """Cria um item de navegação."""

        selected = self.selected_page == page_key

        icon_control = ft.Icon(
            icon,
            size=20,
            color=(
                AppTheme.PRIMARY
                if selected
                else AppTheme.TEXT_SECONDARY
            ),
        )

        text_control = ft.Text(
            label,
            size=14,
            weight=(
                ft.FontWeight.W_600
                if selected
                else ft.FontWeight.NORMAL
            ),
            color=(
                AppTheme.PRIMARY
                if selected
                else AppTheme.TEXT_PRIMARY
            ),
        )

        item = ft.Container(
            height=44,
            border_radius=8,
            bgcolor=(
                AppTheme.PRIMARY_CONTAINER
                if selected
                else None
            ),
            padding=ft.Padding.symmetric(horizontal=12),
            ink=True,
            ink_color=AppTheme.PRIMARY_CONTAINER,
            on_hover=lambda e: self._navigation_hover(
                page_key,
                e.data == "true",
            ),
            on_click=lambda e: self._select_page(page_key),
            content=ft.Row(
                spacing=12,
                controls=[
                    icon_control,
                    text_control,
                ],
            ),
        )

        self.navigation_items[page_key] = item

        return item

    def _navigation_hover(
        self,
        page_key: str,
        hovering: bool,
    ) -> None:
        """Atualiza o estado visual do hover."""

        if page_key == self.selected_page:
            return

        item = self.navigation_items.get(page_key)

        if item is None:
            return

        item.bgcolor = (
            AppTheme.BACKGROUND
            if hovering
            else None
        )

        self.page.update()
    
    def _build_user_area(self) -> ft.Control:
        """Cria a área do usuário."""

        return ft.Column(
            spacing=8,
            controls=[
                ft.Divider(
                    height=1,
                    color=AppTheme.BORDER,
                ),
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(
                            width=36,
                            height=36,
                            border_radius=18,
                            bgcolor=AppTheme.PRIMARY_CONTAINER,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text(
                                self.username[:1].upper(),
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.PRIMARY,
                            ),
                        ),
                        ft.Column(
                            spacing=2,
                            expand=True,
                            controls=[
                                ft.Text(
                                    self.username,
                                    size=13,
                                    weight=ft.FontWeight.W_600,
                                    color=AppTheme.TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    "Usuário",
                                    size=11,
                                    color=AppTheme.TEXT_SECONDARY,
                                ),
                            ],
                        ),
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT,
                            tooltip="Sair",
                            icon_color=AppTheme.TEXT_SECONDARY,
                            on_click=self._logout,
                        ),
                    ],
                ),
            ],
        )

    def _build_content(self) -> ft.Control:
        """Cria a área principal de conteúdo."""

        self.content_area.content = self._build_selected_page()

        return ft.Container(
            expand=True,
            bgcolor=AppTheme.BACKGROUND,
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    self._build_header(),
                    self.content_area,
                ],
            ),
        )

    def _build_header(self) -> ft.Control:
        """Cria o cabeçalho da área de conteúdo."""

        return ft.Container(
            height=AppTheme.HEADER_HEIGHT,
            bgcolor=AppTheme.SURFACE,
            padding=ft.Padding.symmetric(horizontal=24),
            content=ft.Row(
                controls=[
                    self.page_title,
                    ft.Container(expand=True),
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(
                                ft.Icons.PERSON_OUTLINE,
                                size=18,
                                color=AppTheme.TEXT_SECONDARY,
                            ),
                            ft.Text(
                                self.username,
                                size=13,
                                color=AppTheme.TEXT_SECONDARY,
                            ),
                        ],
                    ),
                ],
            ),
        )
    
    def _select_page(self, page_key: str) -> None:
        """Seleciona uma página da aplicação."""

        if page_key == self.selected_page:
            return

        self.selected_page = page_key

        self._update_navigation()

        self.page_title.value = self._get_page_title()

        self.content_area.content = self._build_selected_page()

        self.page.update()

    def _build_selected_page(self) -> ft.Control:
        """Constrói o conteúdo da página selecionada."""

        if self.selected_page == "robots":
            return RobotsPage().build()

        if self.selected_page == "executions":
            return ExecutionsPage().build()

        return DashboardPage(
            username=self.username,
        ).build()

    def _update_navigation(self) -> None:
        """Atualiza o estado visual dos itens de navegação."""

        for page_key, item in self.navigation_items.items():
            selected = page_key == self.selected_page

            item.bgcolor = (
                AppTheme.PRIMARY_CONTAINER
                if selected
                else None
            )

            row = item.content

            if not isinstance(row, ft.Row):
                continue

            icon = row.controls[0]
            label = row.controls[1]

            if isinstance(icon, ft.Icon):
                icon.color = (
                    AppTheme.PRIMARY
                    if selected
                    else AppTheme.TEXT_SECONDARY
                )

            if isinstance(label, ft.Text):
                label.color = (
                    AppTheme.PRIMARY
                    if selected
                    else AppTheme.TEXT_PRIMARY
                )

                label.weight = (
                    ft.FontWeight.W_600
                    if selected
                    else ft.FontWeight.NORMAL
                )

    def _build_dashboard(self) -> ft.Control:
        """Cria o conteúdo inicial do dashboard."""

        return ft.Container(
            expand=True,
            padding=24,
            content=ft.Column(
                spacing=24,
                controls=[
                    ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text(
                                "Visão geral",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                "Acompanhe seus robôs e execuções.",
                                size=14,
                                color=AppTheme.TEXT_SECONDARY,
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=16,
                        controls=[
                            self._build_stat_card(
                                title="Robôs",
                                value="0",
                                icon=ft.Icons.SMART_TOY_OUTLINED,
                            ),
                            self._build_stat_card(
                                title="Robôs ativos",
                                value="0",
                                icon=ft.Icons.POWER_SETTINGS_NEW,
                            ),
                            self._build_stat_card(
                                title="Execuções",
                                value="0",
                                icon=ft.Icons.PLAY_CIRCLE_OUTLINE,
                            ),
                        ],
                    ),
                    ft.Container(
                        padding=24,
                        bgcolor=AppTheme.SURFACE,
                        border_radius=12,
                        content=ft.Column(
                            spacing=8,
                            controls=[
                                ft.Text(
                                    "Bem-vindo ao Gestão de Robôs",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=AppTheme.TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    "Utilize o menu lateral para "
                                    "gerenciar seus robôs.",
                                    size=14,
                                    color=AppTheme.TEXT_SECONDARY,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _build_stat_card(
        self,
        title: str,
        value: str,
        icon: ft.IconData,
    ) -> ft.Control:
        """Cria um card de estatística."""

        return ft.Container(
            expand=True,
            padding=20,
            bgcolor=AppTheme.SURFACE,
            border_radius=12,
            content=ft.Row(
                spacing=16,
                controls=[
                    ft.Container(
                        width=44,
                        height=44,
                        border_radius=10,
                        bgcolor=AppTheme.PRIMARY_CONTAINER,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            icon,
                            size=22,
                            color=AppTheme.PRIMARY,
                        ),
                    ),
                    ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text(
                                title,
                                size=13,
                                color=AppTheme.TEXT_SECONDARY,
                            ),
                            ft.Text(
                                value,
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                        ],
                    ),
                ],
            ),
        )

    def _logout(self, e: ft.Event[ft.IconButton]) -> None:
        """Realiza o logout do usuário."""

        self.on_logout()