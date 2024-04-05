import flet as ft

class CustomTask(ft.Container):
    def __init__(self):
        super().__init__()

        self.wrapper = ft.Column([
            ft.Text("Sync my favorite messages."),
            ft.Divider(color="white"),
            ft.ProgressBar(width=500, value=0),
        ])

        self.content = ft.Row([self.wrapper])
        self.height = 100
        self.bgcolor = ft.colors.BLACK12
        self.border_radius = ft.BorderRadius(10,10,10,10)
        # self.border = ft.border.all(0.5, ft.colors.ORANGE)
        self.padding = 20
