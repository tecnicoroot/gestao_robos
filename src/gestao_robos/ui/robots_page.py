import flet as ft

from gestao_robos.core.theme import AppTheme


class RobotsPage:
    """Página de gerenciamento dos robôs."""

    def build(self) -> ft.Control:
        """Constrói a página de robôs."""

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
                                "Robôs",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                "Gerencie os robôs cadastrados.",
                                size=14,
                                color=AppTheme.TEXT_SECONDARY,
                            ),
                        ],
                    ),
                    ft.Container(
                        expand=True,
                        bgcolor=AppTheme.SURFACE,
                        border_radius=12,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                            controls=[
                                ft.Icon(
                                    ft.Icons.SMART_TOY_OUTLINED,
                                    size=48,
                                    color=AppTheme.PRIMARY,
                                ),
                                ft.Text(
                                    "Nenhum robô cadastrado",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=AppTheme.TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    "O gerenciamento dos robôs será implementado aqui.",
                                    size=14,
                                    color=AppTheme.TEXT_SECONDARY,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )
