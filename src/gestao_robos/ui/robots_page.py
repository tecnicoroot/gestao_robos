
from datetime import datetime, time

import flet as ft

from gestao_robos.domain.entities.robot import Robot
from gestao_robos.services.robot_service import RobotService


class RobotsPage:
    """Página de gerenciamento dos robôs."""

    def __init__(self,
        page: ft.Page,
        robot_service: RobotService,
    ) -> None:
        self.page = page
        self.robot_service = robot_service
        self.robots: list[Robot] = []
        self.selected_robot: Robot | None = None
        self.robot_pending_delete: Robot | None = None
        self.editing_robot = False

        self.details_container = ft.Container(
            expand=True,
        )

        self.content_container = ft.Container(
            expand=True,
        )

        self.table_container = ft.Container(
            expand=True,
        )

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

        self.name_field = ft.TextField(
            label="Nome",
            hint_text="Nome do robô",
        )

        self.user_field = ft.TextField(
            label="Usuário",
            hint_text="Usuário responsável",
        )

        self.description_field = ft.TextField(
            label="Descrição",
            hint_text="Descrição do robô",
            multiline=True,
            min_lines=3,
            max_lines=5,
        )

        self.interval_field = ft.TextField(
            label="Intervalo",
            hint_text="Em segundos",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        self.time_limit_field = ft.TextField(
            label="Limite de tempo",
            hint_text="Em segundos",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        self.executable_name_field = ft.TextField(
            label="Nome do executável",
            hint_text="Ex.: meu_robo.exe",
        )

        self.executable_path_field = ft.TextField(
            label="Path do executável",
            hint_text=r"Ex.: Y:\prd\robos",
        )

        self.action_field = ft.Dropdown(
            label="Ação",
            options=[
                ft.DropdownOption(
                    key="A",
                    text="Automático",
                ),
                ft.DropdownOption(
                    key="H",
                    text="Horário",
                ),
                ft.DropdownOption(
                    key="U",
                    text="Usuário",
                ),
            ],
        )

        self.screen_field = ft.Dropdown(
            label="Tela",
            options=[
                ft.DropdownOption(
                    key="N",
                    text="Não",
                ),
                ft.DropdownOption(
                    key="S",
                    text="Sim",
                ),
            ],
        )

        self.activation_file_field = ft.TextField(
            label="Arquivo de ativação",
            hint_text="Caminho do arquivo de configuração",
        )

        self.working_directory_field = ft.TextField(
            label="Pasta de trabalho",
            hint_text="Diretório de trabalho do robô",
        )

        self.spreadsheet_repository_field = ft.TextField(
            label="Repositório de planilhas",
            hint_text="Diretório do repositório",
        )

        self.notifications_field = ft.TextField(
            label="Notificados",
            hint_text="E-mails separados por ponto e vírgula",
            multiline=True,
            min_lines=2,
            max_lines=4,
        )

        self.program_1_field = ft.TextField(
            label="Programa ativado 1",
            hint_text="Ex.: javaw.exe",
        )

        self.program_2_field = ft.TextField(
            label="Programa ativado 2",
            hint_text="Nome do segundo programa",
        )

        self.activation_time_field = ft.TextField(
            label="Horário de ativação",
            hint_text="HH:MM",
        )

        self.sector_field = ft.Dropdown(
            label="Setor",
            options=[
                ft.DropdownOption(key="1", text="HUHB"),
                ft.DropdownOption(key="2", text="Liberação"),
                ft.DropdownOption(key="3", text="Controladoria"),
                ft.DropdownOption(key="4", text="Contas Médicas"),
                ft.DropdownOption(key="5", text="Financeiro"),
                ft.DropdownOption(key="6", text="Cadastro"),
                ft.DropdownOption(key="7", text="EVB"),
                ft.DropdownOption(key="8", text="DSS"),
                ft.DropdownOption(key="9", text="Direx"),
            ],
        )

        self.form_error_text = ft.Text(
            color=ft.Colors.RED_700,
            size=13,
        )

        self.message_bar = ft.SnackBar(
            content=ft.Text(""),
        )

        self.table_error_text = ft.Text(
                    "",
                    size=13,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.RED_700,
        )
        
        self.table_error_container = ft.Container(
            content=self.table_error_text,
            bgcolor=ft.Colors.RED_50,
            border=ft.Border.all(
                1,
                ft.Colors.RED_200,
            ),
            border_radius=8,
            padding=12,
            visible=False,
        )

        self.delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Excluir robô"),
            content=ft.Text(
                "Tem certeza que deseja excluir este robô?"
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=self._close_delete_dialog,
                ),
                ft.Button(
                    "Excluir",
                    icon=ft.Icons.DELETE,
                    on_click=self._confirm_delete_robot,
                ),
            ],
        )
                

    def build(self) -> ft.Control:
        """Constrói a página de robôs."""
        self.robots = self.robot_service.list_robots()

        self._update_count(self.robots)
        self._render_table(self.robots)

        self.content_container.content = self.table_container

        return ft.Column(
            controls=[
                self._build_header(),
                ft.Divider(height=1),
                self._build_search_bar(),
                self.content_container,
            ],
            expand=True,
            spacing=0,
        )

    def _build_header(self) -> ft.Control:
        """Constrói o cabeçalho da página."""
        return ft.Container(
            padding=ft.Padding(
                top=0,
                right=0,
                bottom=8,
                left=0,
            ),
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Gerenciamento dos robôs cadastrados.",
                                size=24,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Button(
                        content="Novo Robô",
                        icon=ft.Icons.ADD,
                        on_click=self._open_new_robot,
                    ),
                ],
                spacing=16,
            ),
        )

    def _build_search_bar(self) -> ft.Control:
        """Constrói a barra de pesquisa."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.search_field,
                    ft.Container(
                        width=100,
                        alignment=ft.Alignment.CENTER_RIGHT,
                        content=self.count_text,
                    ),
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

        self.selected_robot = None
        self.editing_robot = False

        self._update_count(filtered_robots)
        self._render_table(filtered_robots)

        self.content_container.content = self.table_container

        self.content_container.update()
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
            self.count_text.value = f"{displayed} de {total} robôs"

    def _render_table(self, robots: list[Robot]) -> None:
        """Renderiza a tabela de robôs."""
        rows = [
            self._build_row(robot)
            for robot in robots
        ]

        self.table_container.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.table_error_container,
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(label="ID"),
                            ft.DataColumn(label="Nome"),
                            ft.DataColumn(label="Status"),
                            ft.DataColumn(label="Intervalo"),
                            ft.DataColumn(label="Executável"),
                            ft.DataColumn(label="Usuário"),
                            ft.DataColumn(label="Ações"),
                        ],
                        rows=rows,
                        column_spacing=20,
                        heading_row_height=48,
                        data_row_min_height=56,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            border=ft.Border.all(
                1,
                ft.Colors.GREY_300,
            ),
            border_radius=8,
            padding=8,
            expand=True,
        )

    def _build_row(self, robot: Robot) -> ft.DataRow:
        """Constrói uma linha da tabela."""

        edit_button = ft.IconButton(
            icon=ft.Icons.EDIT,
            tooltip="Editar robô",
            on_click=lambda e: self._open_edit_robot(e, robot),
        )

        delete_button = ft.IconButton(
            icon=ft.Icons.DELETE,
            tooltip="Excluir robô",
            on_click=lambda e: self._delete_robot(
                e,
                robot,
            ),
        )

        return ft.DataRow(
            cells=[
                self._build_cell(
                    ft.Text(str(robot.id)),
                    robot,
                ),
                self._build_cell(
                    ft.Text(
                        robot.nome,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    robot,
                ),
                self._build_cell(
                    self._build_status(robot),
                    robot,
                ),
                self._build_cell(
                    ft.Text(
                        f"{robot.intervalo} min",
                    ),
                    robot,
                ),
                self._build_cell(
                    ft.Text(
                        robot.nome_executavel,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    robot,
                ),
                self._build_cell(
                    ft.Text(robot.usuario_robo),
                    robot,
                ),
                ft.DataCell(
                    ft.Row(
                        controls=[
                            edit_button,
                            delete_button,
                        ],
                        spacing=0,
                    ),
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

    def _build_details(self, robot: Robot) -> ft.Control:
        """Constrói o painel de detalhes do robô selecionado."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.ResponsiveRow(
                        spacing=12,
                        run_spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    "Detalhes do robô",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                col={
                                    "xs": 12,
                                    "md": 4,
                                },
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Text(
                                            f"ID: {robot.id}",
                                            color=ft.Colors.GREY_600,
                                        ),
                                        ft.Button(
                                            content="Editar",
                                            icon=ft.Icons.EDIT,
                                            on_click=self._open_edit_robot,
                                        ),
                                        ft.Button(
                                            content="Excluir",
                                            icon=ft.Icons.DELETE,
                                            on_click=self._request_delete_robot,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.CLOSE,
                                            tooltip="Fechar detalhes",
                                            on_click=self._close_details,
                                        ),
                                    ],
                                    spacing=8,
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                                col={
                                    "xs": 12,
                                    "md": 8,
                                },
                            ),
                        ],
                    ),
                    ft.Divider(),
                    ft.ResponsiveRow(
                        spacing=16,
                        run_spacing=16,
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Nome",
                                            size=12,
                                            color=ft.Colors.GREY_600,
                                        ),
                                        ft.Text(
                                            robot.nome,
                                            max_lines=3,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                                col={
                                    "xs": 12,
                                    "md": 6,
                                },
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Status",
                                            size=12,
                                            color=ft.Colors.GREY_600,
                                        ),
                                        self._build_status(robot),
                                        ft.Button(
                                            content=(
                                                "Desativar"
                                                if robot.ativo
                                                else "Ativar"
                                            ),
                                            icon=(
                                                ft.Icons.PAUSE
                                                if robot.ativo
                                                else ft.Icons.PLAY_ARROW
                                            ),
                                            on_click=self._toggle_robot_status,
                                        ),
                                    ],
                                    spacing=6,
                                ),
                                col={
                                    "xs": 12,
                                    "md": 3,
                                },
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Intervalo",
                                            size=12,
                                            color=ft.Colors.GREY_600,
                                        ),
                                        ft.Text(
                                            f"{robot.intervalo} minutos",
                                        ),
                                    ],
                                    spacing=4,
                                ),
                                col={
                                    "xs": 12,
                                    "md": 3,
                                },
                            ),
                        ],
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Descrição",
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                            ft.Text(
                                robot.descricao or "-",
                            ),
                        ],
                        spacing=4,
                    ),
                    ft.ResponsiveRow(
                        spacing=16,
                        run_spacing=16,
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Executável",
                                            size=12,
                                            color=ft.Colors.GREY_600,
                                        ),
                                        ft.Text(
                                            robot.nome_executavel or "-",
                                            max_lines=2,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                                col={
                                    "xs": 12,
                                    "md": 6,
                                },
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Usuário",
                                            size=12,
                                            color=ft.Colors.GREY_600,
                                        ),
                                        ft.Text(
                                            robot.usuario_robo or "-",
                                            max_lines=2,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                                col={
                                    "xs": 12,
                                    "md": 6,
                                },
                            ),
                        ],
                    ),
                ],
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_300,
            ),
            border_radius=8,
            expand=True,
        )

    def _on_robot_selected(
        self,
        robot: Robot,
    ) -> None:
        """Seleciona um robô e exibe seus detalhes."""
        self.selected_robot = robot
        self.editing_robot = False

        self.details_container.content = self._build_details(robot)
        self.content_container.content = self.details_container

        self.content_container.update()

    def _on_cell_tap(
        self,
        e: ft.Event[ft.DataCell],
        robot: Robot,
    ) -> None:
        """Seleciona o robô ao clicar em uma célula."""
        self._on_robot_selected(robot)

    def _build_cell(
        self,
        content: ft.Control,
        robot: Robot,
    ) -> ft.DataCell:
        """Constrói uma célula clicável."""

        def on_tap(
            e: ft.Event[ft.DataCell],
        ) -> None:
            self._on_cell_tap(e, robot)

        return ft.DataCell(
            content=content,
            on_tap=on_tap,
        )

    def _close_details(
        self,
        e: ft.Event[ft.IconButton],
    ) -> None:
        """Fecha o painel de detalhes."""
        self.selected_robot = None
        self.details_container.content = None
        self.editing_robot = False

        self.content_container.content = self.table_container

        self.content_container.update()

    def _build_robot_form(
        self,
        editing: bool = False,
    ) -> ft.Control:
        form_content = ft.Column(
            controls=[
                # Identificação
                ft.Text(
                    "Identificação",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[
                        ft.Container(
                            content=self.name_field,
                            col={"xs": 12, "md": 6},
                        ),
                        ft.Container(
                            content=self.user_field,
                            col={"xs": 12, "md": 6},
                        ),
                    ],
                ),
                self.description_field,

                ft.Divider(height=8),

                # Execução
                ft.Text(
                    "Execução",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[
                        ft.Container(
                            content=self.action_field,
                            col={"xs": 12, "md": 4},
                        ),
                        ft.Container(
                            content=self.screen_field,
                            col={"xs": 12, "md": 4},
                        ),
                        ft.Container(
                            content=self.interval_field,
                            col={"xs": 12, "md": 4},
                        ),
                    ],
                ),
                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[
                        ft.Container(
                            content=self.time_limit_field,
                            col={"xs": 12, "md": 4},
                        ),
                        ft.Container(
                            content=self.executable_name_field,
                            col={"xs": 12, "md": 8},
                        ),
                    ],
                ),
                self.executable_path_field,

                ft.Divider(height=8),

                # Arquivos
                ft.Text(
                    "Arquivos",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                self.activation_file_field,
                self.working_directory_field,
                self.spreadsheet_repository_field,

                ft.Divider(height=8),

                # Notificações
                ft.Text(
                    "Notificações",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                self.notifications_field,
                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[
                        ft.Container(
                            content=self.program_1_field,
                            col={"xs": 12, "md": 6},
                        ),
                        ft.Container(
                            content=self.program_2_field,
                            col={"xs": 12, "md": 6},
                        ),
                    ],
                ),

                ft.Divider(height=8),

                # Agendamento
                ft.Text(
                    "Agendamento",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[
                        ft.Container(
                            content=self.activation_time_field,
                            col={"xs": 12, "md": 6},
                        ),
                        ft.Container(
                            content=self.sector_field,
                            col={"xs": 12, "md": 6},
                        ),
                    ],
                ),

                self.form_error_text,
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Editar robô"
                                        if editing
                                        else "Novo robô",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        (
                                            "Atualize os dados do robô."
                                            if editing
                                            else "Cadastre um novo robô."
                                        ),
                                        size=13,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                tooltip="Fechar",
                                on_click=self._close_form,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(),
                    form_content,
                    ft.Row(
                        controls=[
                            ft.Button(
                                content="Cancelar",
                                on_click=self._close_form,
                            ),
                            ft.Button(
                                content="Salvar",
                                icon=ft.Icons.SAVE,
                                on_click=self._save_new_robot,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=8,
                        wrap=True,
                    ),
                ],
                spacing=12,
                expand=True,
            ),
            expand=True,
        )
    
    def _save_new_robot(
        self,
        e: ft.Event[ft.Button],
    ) -> None:
        """Cria ou atualiza um robô."""
        self.form_error_text.value = ""

        name = (self.name_field.value or "").strip()

        if not name:
            self.form_error_text.value = (
                "O nome do robô é obrigatório."
            )
            self.form_error_text.update()
            return

        interval = self._parse_int_field(
            self.interval_field,
            "Intervalo",
        )

        if interval is None:
            return

        time_limit = self._parse_int_field(
            self.time_limit_field,
            "Limite de tempo",
        )

        if time_limit is None:
            return

        try:
            activation_time = self._parse_activation_time()
            sector = self._parse_sector()
        except ValueError as error:
            self.form_error_text.value = str(error)
            self.form_error_text.update()
            return

        if self.editing_robot:
            self._update_existing_robot(
                name=name,
                description=(
                    self.description_field.value or ""
                ).strip(),
                interval=interval,
                time_limit=time_limit,
                activation_time=activation_time,
                sector=sector,
            )
            return

        self._create_new_robot(
            name=name,
            description=(
                self.description_field.value or ""
            ).strip(),
            interval=interval,
            time_limit=time_limit,
            activation_time=activation_time,
            sector=sector,
        )    

    def _open_new_robot(
        self,
        e: ft.Event[ft.Button],
    ) -> None:
        """Abre o formulário para cadastrar um novo robô."""
        self.selected_robot = None
        self.editing_robot = False
        self._reset_robot_form()

        self.details_container.content = self._build_robot_form()

        self.content_container.content = self.details_container
        self.content_container.update()

    def _close_form(
        self,
        e: ft.Event[ft.IconButton] | ft.Event[ft.Button],
    ) -> None:
        """Fecha o formulário de cadastro."""
        self.details_container.content = None
        self.editing_robot = False

        self.content_container.content = self.table_container
        self.content_container.update()

    def _parse_int_field(
        self,
        field: ft.TextField,
        label: str,
    ) -> int | None:
        """Converte o valor de um campo para inteiro."""
        value = (field.value or "").strip()

        try:
            return int(value)
        except ValueError:
            self.form_error_text.value = (
                f"O campo '{label}' deve ser um número inteiro."
            )
            self.form_error_text.update()
            return None

    def _reset_robot_form(self) -> None:
        self.name_field.value = ""
        self.user_field.value = ""
        self.description_field.value = ""
        self.interval_field.value = ""
        self.time_limit_field.value = ""
        self.executable_name_field.value = ""
        self.executable_path_field.value = ""

        self.action_field.value = "A"
        self.screen_field.value = "N"

        self.activation_file_field.value = ""
        self.working_directory_field.value = ""
        self.spreadsheet_repository_field.value = ""

        self.notifications_field.value = ""
        self.program_1_field.value = ""
        self.program_2_field.value = ""

        self.activation_time_field.value = ""
        self.sector_field.value = None

        self.form_error_text.value = ""

    def _open_edit_robot(
        self,
        e: ft.Event[ft.Button],
        robot: Robot | None = None,
    ) -> None:
        """Abre o formulário para editar o robô selecionado."""
        if robot is None:
            robot = self.selected_robot

        if robot is None:
            return

        self.selected_robot = robot
        self.editing_robot = True

        self.name_field.value = robot.nome
        self.user_field.value = robot.usuario_robo
        self.description_field.value = robot.descricao
        self.interval_field.value = str(robot.intervalo)
        self.time_limit_field.value = str(robot.limite_tempo)
        self.executable_name_field.value = robot.nome_executavel
        self.executable_path_field.value = robot.path_executavel
        self.action_field.value = robot.acao
        self.screen_field.value = robot.tela

        self.activation_file_field.value = robot.arquivo_ativacao
        self.working_directory_field.value = robot.pasta_trabalho
        self.spreadsheet_repository_field.value = robot.repositorio_planilhas

        self.notifications_field.value = robot.notificados
        self.program_1_field.value = robot.pgm_ativado1
        self.program_2_field.value = robot.pgm_ativado2

        self.activation_time_field.value = (
            robot.horario_ativacao.strftime("%H:%M")
            if robot.horario_ativacao is not None
            else ""
        )

        self.sector_field.value = str(robot.codigo_setor)
        self.form_error_text.value = ""

        self.details_container.content = self._build_robot_form(
            editing=True,
        )

        self.content_container.content = self.details_container
        self.content_container.update()

    def _create_new_robot(
        self,
        name: str,
        description: str,
        interval: int,
        time_limit: int,
        activation_time: time | None,
        sector: int,
    ) -> None:
        """Cria um novo robô."""
        robot = Robot(
            id=None,
            nome=name,
            descricao=description,
            ativo=False,
            intervalo=interval,
            acao=self.action_field.value or "A",
            tela=self.screen_field.value or "N",
            path_executavel=(
                self.executable_path_field.value or ""
            ).strip(),
            limite_tempo=time_limit,
            arquivo_ativacao=(
                self.activation_file_field.value or ""
            ).strip(),
            nome_executavel=(
                self.executable_name_field.value or ""
            ).strip(),
            pasta_trabalho=(
                self.working_directory_field.value or ""
            ).strip(),
            repositorio_planilhas=(
                self.spreadsheet_repository_field.value or ""
            ).strip(),
            notificados=(
                self.notifications_field.value or ""
            ).strip(),
            pgm_ativado1=(
                self.program_1_field.value or ""
            ).strip(),
            pgm_ativado2=(
                self.program_2_field.value or ""
            ).strip(),
            robo_sequencia=None,
            usuario_robo=(
                self.user_field.value or ""
            ).strip(),
            robo_teste=0,
            horario_ativacao=activation_time,
            codigo_setor=sector,
            biblioteca="",
        )

        created_robot = self.robot_service.create_robot(robot)

        self.robots.append(created_robot)

        self._update_count(self.robots)
        self._render_table(self.robots)

        self.selected_robot = created_robot
        self.editing_robot = False

        self.details_container.content = self._build_details(
            created_robot,
        )
        self.content_container.content = self.details_container

        self.content_container.update()
        self.count_text.update()
   
    def _toggle_robot_status(
        self,
        e: ft.Event[ft.Button],
    ) -> None:
        """Ativa ou desativa o robô selecionado."""
        if self.selected_robot is None:
            return

        robot_id = self.selected_robot.id

        if robot_id is None:
            return

        if self.selected_robot.ativo:
            updated_robot = self.robot_service.deactivate_robot(
                robot_id,
            )
        else:
            updated_robot = self.robot_service.activate_robot(
                robot_id,
            )

        for index, robot in enumerate(self.robots):
            if robot.id == updated_robot.id:
                self.robots[index] = updated_robot
                break

        self.selected_robot = updated_robot

        self._render_table(self.robots)

        self.details_container.content = self._build_details(
            updated_robot,
        )
        self.content_container.content = self.details_container

        self.content_container.update()

    def _update_existing_robot(
        self,
        name: str,
        description: str,
        interval: int,
        time_limit: int,
        activation_time: time | None,
        sector: int,
    ) -> None:
        """Atualiza o robô que está sendo editado."""
        if self.selected_robot is None:
            return

        robot_id = self.selected_robot.id

        if robot_id is None:
            self.form_error_text.value = (
                "Não foi possível identificar o robô."
            )
            self.form_error_text.update()
            return

        updated_robot = self.robot_service.update_robot(
            robot_id=robot_id,
            nome=name,
            descricao=description,
            intervalo=interval,
            limite_tempo=time_limit,
            nome_executavel=(
                self.executable_name_field.value or ""
            ).strip(),
            path_executavel=(
                self.executable_path_field.value or ""
            ).strip(),
            usuario_robo=(
                self.user_field.value or ""
            ).strip(),
            acao=self.action_field.value or "A",
            tela=self.screen_field.value or "N",
            arquivo_ativacao=(
                self.activation_file_field.value or ""
            ).strip(),
            pasta_trabalho=(
                self.working_directory_field.value or ""
            ).strip(),
            repositorio_planilhas=(
                self.spreadsheet_repository_field.value or ""
            ).strip(),
            notificados=(
                self.notifications_field.value or ""
            ).strip(),
            pgm_ativado1=(
                self.program_1_field.value or ""
            ).strip(),
            pgm_ativado2=(
                self.program_2_field.value or ""
            ).strip(),
            horario_ativacao=activation_time,
            codigo_setor=sector,
        )

        for index, robot in enumerate(self.robots):
            if robot.id == updated_robot.id:
                self.robots[index] = updated_robot
                break

        self.selected_robot = updated_robot
        self.editing_robot = False

        self._update_count(self.robots)
        self._render_table(self.robots)

        self.details_container.content = self._build_details(
            updated_robot,
        )
        self.content_container.content = self.details_container

        self.content_container.update()
        self.count_text.update()
    
    def _request_delete_robot(
        self,
        e: ft.Event[ft.Button],
    ) -> None:
        """Solicita confirmação antes de excluir o robô."""
        if self.selected_robot is None:
            return

        if self.selected_robot.ativo:
            self.form_error_text.value = (
                "Não é permitido excluir um robô ativo. "
                "Desative o robô antes de excluí-lo."
            )
            self.form_error_text.update()
            return

        robot = self.selected_robot

        self.details_container.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Excluir robô",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        f'Tem certeza que deseja excluir "{robot.nome}"?'
                    ),
                    ft.Text(
                        "Essa operação não poderá ser desfeita.",
                        color=ft.Colors.RED_700,
                    ),
                    ft.Row(
                        controls=[
                            ft.Button(
                                content="Cancelar",
                                on_click=self._cancel_delete,
                            ),
                            ft.Button(
                                content="Excluir",
                                icon=ft.Icons.DELETE,
                                on_click=self._confirm_delete_robot,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=8,
                        wrap=True,
                    ),
                ],
                spacing=16,
            ),
            padding=20,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_300,
            ),
            border_radius=8,
            expand=True,
        )

        self.content_container.content = self.details_container
        self.content_container.update()

    def _cancel_delete(
        self,
        e: ft.Event[ft.Button],
    ) -> None:
        """Cancela a exclusão e retorna aos detalhes."""
        if self.selected_robot is None:
            return

        self.details_container.content = self._build_details(
            self.selected_robot,
        )
        self.content_container.content = self.details_container

        self.content_container.update()

       
    def _parse_activation_time(self) -> time | None:
        """Converte o horário informado no formulário."""
        value = (self.activation_time_field.value or "").strip()

        if not value:
            return None

        try:
            return datetime.strptime(
                value,
                "%H:%M",
            ).time()
        except ValueError as error:
            raise ValueError(
                "O horário de ativação deve estar no formato HH:MM."
            ) from error

    def _parse_sector(self) -> int:
        """Converte o setor selecionado para seu código."""
        value = self.sector_field.value

        if not value:
            raise ValueError(
                "O setor do robô deve ser informado."
            )

        try:
            return int(value)
        except ValueError as error:
            raise ValueError(
                "O setor selecionado é inválido."
            ) from error

    def _delete_robot(
        self,
        e: ft.Event[ft.IconButton],
        robot: Robot,
    ) -> None:
        """Solicita confirmação antes de excluir o robô."""
        self.robot_pending_delete = robot

        self.delete_dialog.content = ft.Text(
            f'Tem certeza que deseja excluir o robô "{robot.nome}"?'
        )

        self.delete_dialog.open = True
        self.page.update()

    def _close_delete_dialog(
        self,
        e: ft.Event[ft.TextButton],
    ) -> None:
        """Fecha o diálogo de exclusão."""
        self.delete_dialog.open = False
        self.robot_pending_delete = None
        self.page.update()
    
    def _confirm_delete_robot(
        self,
        e: ft.Event[ft.Button],
    ) -> None:
        """Confirma a exclusão do robô."""
        robot = self.robot_pending_delete

        if robot is None:
            return

        self.table_error_text.value = ""
        self.table_error_container.visible = False

        try:
            self.robot_service.delete_robot(
                robot.id or 0,
            )
        except ValueError as error:
            self.table_error_text.value = str(error)
            self.table_error_container.visible = True

            self.delete_dialog.open = False
            self.robot_pending_delete = None

            self.content_container.update()
            self.page.update()
            return

        self.robots = [
            item
            for item in self.robots
            if item.id != robot.id
        ]

        if self.selected_robot is not None and self.selected_robot.id == robot.id:
                self.selected_robot = None
                self.details_container.content = None
                self.content_container.content = self.table_container

        self.robot_pending_delete = None
        self.delete_dialog.open = False

        self._update_count(self.robots)
        self._render_table(self.robots)

        self.content_container.update()
        self.count_text.update()
        self.page.update()