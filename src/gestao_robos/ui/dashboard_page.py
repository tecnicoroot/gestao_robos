import flet as ft

from gestao_robos.core.theme import AppTheme


class DashboardPage:
    """Conteúdo da página inicial do dashboard."""

    def __init__(self, username: str) -> None:
        self.username = username

    def build(self) -> ft.Control:
        """Constrói o dashboard."""

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
                                    f"Bem-vindo, {self.username}",
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