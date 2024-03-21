from ctypes import windll
import flet as ft



screensize = windll.user32.GetSystemMetrics(0), \
    windll.user32.GetSystemMetrics(1)


def application(page: ft.Page):
    page.title = "Telegram Migrator"
    page.window_width = screensize[0] * 0.5
    page.window_height = screensize[1] * 0.7
    page.window_top = screensize[1] / 6
    page.window_left = (screensize[0] * 0.5) / 2
    page.update()

ft.app(target=application)