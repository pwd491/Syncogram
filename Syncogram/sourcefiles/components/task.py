"""Custom task container for view in mainscreen."""
import flet as ft

class CustomTask(ft.Container):
    """The task container."""
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = ft.Text()
        self.title.value = title
        self.title.expand = True
        self.title.expand_loose = True

        self.progress = ft.ProgressBar()
        self.progress.value = 0

        self.value = ft.Text()
        self.value.value = 0
        self.total = ft.Text()
        self.total.value = 0

        self.progress_counters = ft.Row()
        self.progress_counters.controls = [self.value, self.total]
        self.progress_counters.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.progress_counters.visible = False

        self.header = ft.Row()
        self.header.controls = [self.title, ft.Icon(ft.icons.UPDATE, color=ft.colors.ORANGE_500)]
        self.header.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.header.vertical_alignment = ft.CrossAxisAlignment.START

        self.wrapper = ft.Column([
            self.header,
            ft.Divider(opacity=0),
            self.progress_counters,
            self.progress
        ])

        self.content = self.wrapper
        self.bgcolor = ft.colors.BLACK12
        self.border_radius = ft.BorderRadius(10,10,10,10)
        self.border = ft.border.all(0.5, ft.colors.ORANGE)
        self.padding = 20

    def success(self):
        """Theme mode when task was end succesfully."""
        self.progress.value = 1
        self.header.controls.pop(-1)
        self.header.controls.append(ft.Icon(ft.icons.TASK_ALT, color=ft.colors.GREEN))
        self.border = ft.border.all(0.5, ft.colors.GREEN)
        self.update()

    def unsuccess(self, exception):
        """Theme mode when task was end unsuccesfully."""
        self.progress.value = 0
        self.header.controls.pop(-1)
        self.header.controls.append(ft.Icon(ft.icons.ERROR, color=ft.colors.RED, tooltip=str(exception)))
        self.border = ft.border.all(0.5, ft.colors.RED)
        self.update()
