import flet as ft

class CustomTask(ft.Container):
    def __init__(self) -> None:
        super().__init__()
        self.wait_status: ft.Border = ft.border.all(0.5, ft.colors.ORANGE)
        self.success_status: ft.Border = ft.border.all(0.5, ft.colors.GREEN)

        self.title = ft.Text()
        self.title.value = "Sync my favorite messages."

        self.progress = ft.ProgressBar()
        self.progress.value = 0

        self.wrapper = ft.Column([
            self.title,
            ft.Divider(opacity=0),
            self.progress
        ])

        self.content = self.wrapper
        self.height = 100
        self.bgcolor = ft.colors.BLACK12
        self.border_radius = ft.BorderRadius(10,10,10,10)
        self.border = self.wait_status
        self.padding = 20

    @property
    async def value(self) -> None | int | float:
        return self.progress.value