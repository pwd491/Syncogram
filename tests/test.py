import flet as ft

class Alert(ft.AlertDialog):
    def __init__(self, page: ft.Page, *args):
        self.func = func

        super().__init__(
            modal=True,
            title=ft.Text("Authentication via Telegram"),
            # content=self.wrapper,
            actions=[
                ft.TextButton("Ok", on_click=self.close)
            ],
        )

    def close(self, e):
        self.func()
        self.open = False

    


class Section(ft.Container):
    def __init__(self, page: ft.Page, *args) -> None:
        self.page: ft.Page = page
        self.button = ft.TextButton("Button", on_click=self.open)
        self.section = ft.Column([ft.Text('Section'), self.button])
        self.alert = Alert(self.page, self.add_string)
        super().__init__(
            self.section,
            expand=True,
            bgcolor = ft.colors.SECONDARY_CONTAINER,
            border_radius = ft.BorderRadius(10, 10, 10, 10),
            padding=20
        )
    
    def add_string(self):
        self.section.controls.append(ft.Text("Some string"))
        self.update()

    def open(self, e):
        self.page.dialog = self.alert
        self.alert.open = True
        self.page.update()

def main(page: ft.Page):
    x = ft.Row([Section(page)])
    page.add(x)

ft.app(target=main)