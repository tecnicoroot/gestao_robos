import flet as ft

from gestao_robos.domain.entities.robot import Robot
from gestao_robos.services.robot_service import RobotService


class RobotsPage:
    """Página de gerenciamento dos robôs."""

    def __init__(self, robot_service: RobotService) -> None:
        self.robot_service = robot_service

        self.robots: list[Robot] = []

        self.search_field = ft.TextField(
            hint_text="Pesquisar por nome, descrição ou executável...",
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            on_change=self._on_search_change,
        )

        self.count_text = ft.Text(
            size=14,
            color=ft.Colors.GREY_600,
        )

        self.table_container = ft.Container(
            expand=True,
        )

    def build(self) -> ft.Control:
        """Constrói a página de robôs."""
        self.robots = self.robot_service.list_robots()

        self._update_count(self.robots)
        self._render_table(self.robots)

        return ft.Column(
            controls=[
                self._build_header(),
                ft.Divider(height=1),
                self._build_search_bar(),
                self.table_container,
            ],
            expand=True,
            spacing=0,
        )

    def _build_header(self) -> ft.Control:
        """Constrói o cabeçalho da página."""
        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            "Robôs",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Gerenciamento dos robôs cadastrados.",
                            size=14,
                            color=ft.Colors.GREY_600,
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
                ft.Button(
                    content="Novo Robô",
                    icon=ft.Icons.ADD,
                    disabled=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def _build_search_bar(self) -> ft.Control:
        """Constrói a barra de pesquisa."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.search_field,
                    self.count_text,
                ],
                spacing=16,
            ),
            padding=ft.Padding(
                top=16,
                right=0,
                bottom=16,
                left=0,
            ),
        )

    def _on_search_change(
        self,
        e: ft.Event[ft.TextField],
    ) -> None:
        """Filtra os robôs conforme o texto pesquisado."""
        search_text = (e.control.value or "").strip().lower()

        if not search_text:
            filtered_robots = self.robots
        else:
            filtered_robots = [
                robot
                for robot in self.robots
                if self._matches_search(robot, search_text)
            ]

        self._update_count(filtered_robots)
        self._render_table(filtered_robots)
        self.table_container.update()
        self.count_text.update()

    @staticmethod
    def _matches_search(
        robot: Robot,
        search_text: str,
    ) -> bool:
        """Verifica se o robô corresponde à pesquisa."""
        searchable_fields = (
            robot.nome,
            robot.descricao,
            robot.nome_executavel,
            robot.usuario_robo,
        )

        return any(
            search_text in field.lower()
            for field in searchable_fields
        )

    def _update_count(self, robots: list[Robot]) -> None:
        """Atualiza o contador exibido na tela."""
        total = len(self.robots)
        displayed = len(robots)

        if displayed == total:
            self.count_text.value = f"{total} robôs"
        else:
            self.count_text.value = (
                f"{displayed} de {total} robôs"
            )

    def _render_table(self, robots: list[Robot]) -> None:
        """Renderiza a tabela de robôs."""
        rows = [
            self._build_row(robot)
            for robot in robots
        ]

        self.table_container.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(label="ID"),
                            ft.DataColumn(label="Nome"),
                            ft.DataColumn(label="Status"),
                            ft.DataColumn(label="Intervalo"),
                            ft.DataColumn(label="Executável"),
                            ft.DataColumn(label="Usuário"),
                        ],
                        rows=rows,
                        column_spacing=24,
                        heading_row_height=48,
                        data_row_min_height=56,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
            border=ft.Border.all(
                1,
                ft.Colors.GREY_300,
            ),
            
            border_radius=8,
            padding=8,
            expand=True,
        )

    @staticmethod
    def _build_row(robot: Robot) -> ft.DataRow:
        """Constrói uma linha da tabela."""
        status = RobotsPage._build_status(robot)

        return ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Text(str(robot.id)),
                ),
                ft.DataCell(
                    ft.Text(
                        robot.nome,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ),
                ft.DataCell(status),
                ft.DataCell(
                    ft.Text(
                        f"{robot.intervalo} min",
                    ),
                ),
                ft.DataCell(
                    ft.Text(
                        robot.nome_executavel,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ),
                ft.DataCell(
                    ft.Text(robot.usuario_robo),
                ),
            ],
        )

    @staticmethod
    def _build_status(robot: Robot) -> ft.Control:
        """Constrói o indicador visual de status."""
        if robot.ativo:
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.CIRCLE,
                            size=10,
                            color=ft.Colors.GREEN,
                        ),
                        ft.Text("Ativo"),
                    ],
                    spacing=6,
                ),
            )

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CIRCLE,
                        size=10,
                        color=ft.Colors.GREY_500,
                    ),
                    ft.Text("Inativo"),
                ],
                spacing=6,
            ),
        )