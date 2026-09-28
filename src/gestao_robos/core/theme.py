import flet as ft


class AppTheme:
    """Tema visual da aplicação."""

    PRIMARY = ft.Colors.BLUE
    PRIMARY_CONTAINER = ft.Colors.BLUE_50

    BACKGROUND = ft.Colors.GREY_50
    SURFACE = ft.Colors.WHITE

    TEXT_PRIMARY = ft.Colors.GREY_900
    TEXT_SECONDARY = ft.Colors.GREY_600

    ERROR = ft.Colors.RED_700

    BORDER = ft.Colors.GREY_300
    # Dimensões
    LOGIN_CARD_WIDTH = 440
    LOGIN_CARD_PADDING = 40

    INPUT_WIDTH = 360
    INPUT_HEIGHT = 56
    BUTTON_HEIGHT = 52

    # Dimensões - Aplicação
    SIDEBAR_WIDTH = 240
    HEADER_HEIGHT = 64

    @classmethod
    def configure(cls, page: ft.Page) -> None:
        """Configura o tema global da aplicação."""

        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=cls.PRIMARY,
                surface=cls.SURFACE,
                error=cls.ERROR,
            ),
        )

        page.bgcolor = cls.BACKGROUND
