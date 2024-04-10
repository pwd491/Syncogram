import flet as ft

class CustomTask(ft.Container):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = ft.Text()
        self.title.value = title
        self.title.width = 450

        self.progress = ft.ProgressBar()
        self.progress.value = 0

        self.header = ft.Row()
        self.header.controls = [self.title, ft.Icon(ft.icons.UPDATE, color=ft.colors.ORANGE_500)]
        self.header.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        self.wrapper = ft.Column([
            self.header,
            ft.Divider(opacity=0),
            self.progress
        ])

        self.content = self.wrapper
        # self.height = 100
        self.bgcolor = ft.colors.BLACK12
        self.border_radius = ft.BorderRadius(10,10,10,10)
        self.border = ft.border.all(0.5, ft.colors.ORANGE)
        self.padding = 20

    @property
    async def value(self) -> None | int | float:
        return self.progress.value