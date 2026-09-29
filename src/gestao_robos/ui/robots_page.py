import flet as ft

from gestao_robos.domain.entities.robot import Robot
from gestao_robos.services.robot_service import RobotService


class RobotsPage:
    """Página de gerenciamento dos robôs."""

    def __init__(self, robot_service: RobotService) -> None:
        self.robot_service = robot_service

        self.robots: list[Robot] = []
        self.selected_robot: Robot | None = None
        self.details_container = ft.Container()
        self.editing_robot = False

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

        self.name_field = ft.TextField(
            label="Nome",
            hint_text="Nome do robô",
            expand=True,
        )

        self.user_field = ft.TextField(
            label="Usuário",
            hint_text="Usuário responsável",
            expand=True,
        )

        self.description_field = ft.TextField(
            label="Descrição",
            hint_text="Descrição do robô",
            multiline=True,
            min_lines=2,
            max_lines=4,
        )

        self.interval_field = ft.TextField(
            label="Intervalo",
            hint_text="Minutos",
            expand=True,
        )

        self.time_limit_field = ft.TextField(
            label="Limite de tempo",
            hint_text="Minutos",
            expand=True,
        )

        self.executable_name_field = ft.TextField(
            label="Nome do executável",
            hint_text="Ex.: meu_robo.exe",
        )

        self.executable_path_field = ft.TextField(
            label="Path do executável",
            hint_text="Caminho do executável",
        )

        self.form_error_text = ft.Text(
            color=ft.Colors.RED_700,
            size=13,
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
                ft.Container(
                    content=self.details_container,
                    padding=ft.Padding(
                        top=16,
                        right=0,
                        bottom=0,
                        left=0,
                    ),
                ),
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
        self.selected_robot = None
        self.details_container.content = None
        self.details_container.update()
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
                        column_spacing=20,
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

    
    def _build_row(self, robot: Robot) -> ft.DataRow:
        """Constrói uma linha da tabela."""
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
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Detalhes do robô",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                            ),
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
                    ),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Nome",
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                    ),
                                    ft.Text(robot.nome),
                                ],
                                expand=True,
                            ),
                        ] ,  
                    ),
                    ft.Row(
                        controls=[
                            ft.Column(
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
                                expand=True,
                            ),
                            ft.Column(
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
                                expand=True,
                            ),
                        ],
                        spacing=24,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Descrição",
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                            ft.Text(robot.descricao or "-"),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Executável",
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                    ),
                                    ft.Text(
                                        robot.nome_executavel or "-",
                                    ),
                                ],
                                expand=True,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Usuário",
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                    ),
                                    ft.Text(
                                        robot.usuario_robo or "-",
                                    ),
                                ],
                                expand=True,
                            ),
                        ],
                    ),
                ],
                spacing=12,
            ),
            padding=20,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_300,
            ),
            border_radius=8,
        )

    def _on_robot_selected(
        self,
        robot: Robot,
    ) -> None:
        """Seleciona um robô e exibe seus detalhes."""
        self.selected_robot = robot
        self.details_container.content = self._build_details(robot)
        self.details_container.update()

   

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


    def _close_details(self, e: ft.Event[ft.IconButton]) -> None:
        """Fecha o painel de detalhes."""
        self.selected_robot = None
        self.details_container.content = None
        self.details_container.update()

    def _build_robot_form(
        self,
        editing: bool = False,
    ) -> ft.Control:
        """Constrói o formulário de cadastro do robô."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Editar robô" if editing else "Novo robô",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                tooltip="Fechar",
                                on_click=self._close_form,
                            ),
                        ],
                    ),
                    ft.Divider(),
                    ft.Text(
                        "Identificação",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Row(
                        controls=[
                            self.name_field,
                            self.user_field,
                        ],
                    ),
                    self.description_field,
                    ft.Text(
                        "Execução",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Row(
                        controls=[
                            self.interval_field,
                            self.time_limit_field,
                        ],
                    ),
                    self.executable_name_field,
                    self.executable_path_field,
                    self.form_error_text,
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
                    ),
                ]
            )
        )

    def _save_new_robot(
        self,
        e: ft.Event[ft.Button],
        ) -> None:
            """Cria ou atualiza um robô."""
            self.form_error_text.value = ""

            name = self.name_field.value.strip()

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

            if self.editing_robot:
                self._update_existing_robot(
                    name=name,
                    description=self.description_field.value.strip(),
                    interval=interval,
                    time_limit=time_limit,
                )
                return

            self._create_new_robot(
                name=name,
                description=self.description_field.value.strip(),
                interval=interval,
                time_limit=time_limit,
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
        self.details_container.update()


    def _close_form(
        self,
        e: ft.Event[ft.IconButton] | ft.Event[ft.Button],
    ) -> None:
        """Fecha o formulário de cadastro."""
        self.details_container.content = None
        self.details_container.update()

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
        """Limpa os campos do formulário de novo robô."""
        self.name_field.value = ""
        self.user_field.value = ""
        self.description_field.value = ""
        self.interval_field.value = ""
        self.time_limit_field.value = ""
        self.executable_name_field.value = ""
        self.executable_path_field.value = ""
        self.form_error_text.value = ""

    def _open_edit_robot(
    self,
    e: ft.Event[ft.Button],
) -> None:
        """Abre o formulário para editar o robô selecionado."""
        if self.selected_robot is None:
            return

        self.editing_robot = True
        robot = self.selected_robot

        self.name_field.value = robot.nome
        self.user_field.value = robot.usuario_robo
        self.description_field.value = robot.descricao
        self.interval_field.value = str(robot.intervalo)
        self.time_limit_field.value = str(robot.limite_tempo)
        self.executable_name_field.value = robot.nome_executavel
        self.executable_path_field.value = robot.path_executavel
        self.form_error_text.value = ""

        self.details_container.content = self._build_robot_form(
            editing=True,
        )
        self.details_container.update()


    def _create_new_robot(
        self,
        name: str,
        description: str,
        interval: int,
        time_limit: int,
    ) -> None:
        """Cria um novo robô."""
        robot = Robot(
            id=None,
            nome=name,
            descricao=description,
            ativo=False,
            intervalo=interval,
            acao="",
            tela="",
            path_executavel=self.executable_path_field.value.strip(),
            limite_tempo=time_limit,
            arquivo_ativacao="",
            nome_executavel=self.executable_name_field.value.strip(),
            pasta_trabalho="",
            repositorio_planilhas="",
            notificados="",
            pgm_ativado1="",
            pgm_ativado2="",
            robo_sequencia=None,
            usuario_robo=self.user_field.value.strip(),
            robo_teste=0,
            horario_ativacao=None,
            codigo_setor=0,
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

        self.table_container.update()
        self.count_text.update()
        self.details_container.update()

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

        self.table_container.update()
        self.details_container.update()

    def _update_existing_robot(
        self,
        name: str,
        description: str,
        interval: int,
        time_limit: int,
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
            nome_executavel=self.executable_name_field.value,
            path_executavel=self.executable_path_field.value,
            usuario_robo=self.user_field.value,
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

        self.table_container.update()
        self.count_text.update()
        self.details_container.update()

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
                        f"Tem certeza que deseja excluir "
                        f'"{robot.nome}"?',
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
        )

        self.details_container.update()

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
        self.details_container.update()

    def _confirm_delete_robot(
        self,
        e: ft.Event[ft.Button],
    ) -> None:
        """Exclui o robô após confirmação."""
        if self.selected_robot is None:
            return

        robot_id = self.selected_robot.id

        if robot_id is None:
            return

        self.robot_service.delete_robot(robot_id)

        self.robots = [
            robot
            for robot in self.robots
            if robot.id != robot_id
        ]

        self.selected_robot = None

        self._update_count(self.robots)
        self._render_table(self.robots)

        self.details_container.content = None

        self.table_container.update()
        self.count_text.update()
        self.details_container.update()