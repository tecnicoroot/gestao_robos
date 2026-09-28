import flet as ft

from gestao_robos.services.robot_service import RobotService


class RobotsPage:
    """Página de gerenciamento dos robôs."""

    def __init__(self, robot_service: RobotService) -> None:
        self.robot_service = robot_service

    def build(self) -> ft.Control:
        robots = self.robot_service.list_robots()

        return ft.Column(
            controls=[
                ft.Text(
                    f"Robôs cadastrados: {len(robots)}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
        )