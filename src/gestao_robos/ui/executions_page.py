import flet as ft

from gestao_robos.core.theme import AppTheme


class ExecutionsPage:
    """Página de acompanhamento das execuções."""

    def build(self) -> ft.Control:
        """Constrói a página de execuções."""

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
                                "Execuções",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                "Acompanhe o histórico de execuções.",
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
                                    ft.Icons.PLAY_CIRCLE_OUTLINE,
                                    size=48,
                                    color=AppTheme.PRIMARY,
                                ),
                                ft.Text(
                                    "Nenhuma execução registrada",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=AppTheme.TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    "O histórico de execuções será exibido aqui.",
                                    size=14,
                                    color=AppTheme.TEXT_SECONDARY,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )
