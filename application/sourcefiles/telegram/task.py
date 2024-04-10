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
        self.bgcolor = ft.colors.BLACK12
        self.border_radius = ft.BorderRadius(10,10,10,10)
        self.border = ft.border.all(0.5, ft.colors.ORANGE)
        self.padding = 20
    
    async def success(self):
        self.progress.value = 1
        self.header.controls.pop(-1)
        self.header.controls.append(ft.Icon(ft.icons.TASK_ALT, color=ft.colors.GREEN))
        self.border = ft.border.all(0.5, ft.colors.GREEN)
        await self.update_async()


    async def unsuccess(self, exception):
        self.progress.value = 0
        self.header.controls.pop(-1)
        self.header.controls.append(ft.Icon(ft.icons.ERROR, color=ft.colors.RED, tooltip=str(exception)))
        self.border = ft.border.all(0.5, ft.colors.RED)
        return await self.update_async()