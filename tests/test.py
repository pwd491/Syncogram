import flet as ft

class UserBar(ft.Column):
    def __init__(self):
        super().__init__(
            controls = [ft.Container(width=250,expand=True,bgcolor='red')],
        )

class MainContainer(ft.Column):
    def __init__(self):
        super().__init__(
            controls = [ft.Container(expand=True, bgcolor='red')],
            expand=True,
        )

class UIManager(ft.Row):
    def __init__(self):
        super().__init__(
            controls = [UserBar(), MainContainer()],
            expand=True,
        )

def main(page: ft.Page):
    page.add(UIManager())
    page.update()

ft.app(target=main)