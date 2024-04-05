import flet as ft

class CustomTask(ft.Container):
    def __init__(self):
        super().__init__()

        self.wrapper = ft.Column([
            ft.Text("Sync my favorite messages."),
            ft.Divider(opacity=0),
            ft.ProgressBar()
        ])

        self.content = self.wrapper
        self.height = 100
        self.bgcolor = ft.colors.BLACK12
        self.border_radius = ft.BorderRadius(10,10,10,10)
        # self.border = ft.border.all(0.5, ft.colors.GREEN_ACCENT)
        self.padding = 20
