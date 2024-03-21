from screeninfo import get_monitors
import flet as ft

SCREENWIDTH = 1920
SCREENHEIGHT = 1080

for monitor in get_monitors():
    if monitor.is_primary:
        SCREENWIDTH: int = monitor.width
        SCREENHEIGHT: int = monitor.height
        break


def application(page: ft.Page):
    page.title = "Telegram Migrator"
    page.window_width = SCREENWIDTH * 0.5
    page.window_height = SCREENHEIGHT * 0.7
    page.window_top = SCREENHEIGHT / 8
    page.window_left = (SCREENWIDTH * 0.5) / 2
    page.update()

ft.app(target=application)