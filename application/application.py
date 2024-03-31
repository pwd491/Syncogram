from tests.utils import screensize
from sourcefiles.sqlite import SQLite
from sourcefiles import navbar
import flet as ft

SCREENWIDTH, SCREENHEIGHT = screensize()


def application(page: ft.Page):
    page.title = "Telegram Migrator"
    page.window_width = page.window_min_width = SCREENWIDTH * 0.5
    page.window_height = page.window_min_height = SCREENHEIGHT * 0.7
    page.window_top = SCREENHEIGHT / 8
    page.window_left = (SCREENWIDTH * 0.5) / 2
    # page.theme_mode = ft.ThemeMode.LIGHT

    sqlite = SQLite()
    result = sqlite.execute_all()

    col2 = ft.Container(
        ft.Column(),
        expand=True,
        border_radius=ft.BorderRadius(10, 10, 10, 10),
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER),
    )

    page.add(
        ft.Row(
            [
                navbar(page),
                col2,
            ],
            expand=True,
        )
    )

    page.update()


if __name__ == "__main__":
    ft.app(target=application)
