import flet as ft

class MainContainer(ft.Container):
    def __init__(self):
        super().__init__(
            content = ft.Column(),
            expand=True,
            bgcolor='yellow'
        )

class UserBar(ft.Container):
    def __init__(self):
        self.button = ft.TextButton()
        self.button.text = "Button"
        

        self.wrapper = None

        super().__init__(
            content = ft.Column([self.button],width=250,expand=True),
            bgcolor='red',
        )

def main(page: ft.Page):
    page.add(ft.Row([UserBar(), MainContainer()], expand=True))
    page.update()

ft.app(target=main)