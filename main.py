import flet as ft

from gestao_robos.core.app import App


def main(page: ft.Page) -> None:
    app = App(page)
    app.start()


if __name__ == "__main__":
    ft.run(main)
