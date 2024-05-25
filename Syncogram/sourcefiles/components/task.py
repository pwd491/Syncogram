"""Custom task container for view in mainscreen."""
import flet as ft

class Task(ft.Container):
    """The task container."""
    def __init__(self, title: str = None, description: str = None) -> None:
        super().__init__()
        self.title: ft.Text = ft.Text()
        self.title.value = title
        self.title.expand = True
        self.title.selectable = True
        self.title.expand_loose = True

        self.icon: ft.Icon = ft.Icon()
        self.icon.name = ft.icons.UPDATE

        self.description: ft.Text = ft.Text()
        self.description.value = description
        self.description.size = 11
        self.description.color = ft.colors.BLUE_GREY
        self.description.selectable = True

        self.progress: ft.ProgressBar = ft.ProgressBar()
        self.progress.value = 0

        self.current_value: ft.Text = ft.Text()
        self.current_value.value = 0
        self.current_total: ft.Text = ft.Text()
        self.current_total.value = 0

        self.progress_counters = ft.Row()
        self.progress_counters.controls = [self.current_value, self.current_total]
        self.progress_counters.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.progress_counters.visible = False

        self.header: ft.Row = ft.Row()
        self.header.controls = [self.title, self.icon]
        self.header.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.header.vertical_alignment = ft.CrossAxisAlignment.START

        self.wrapper: ft.Column = ft.Column([
            self.header,
            self.description,
            ft.Divider(opacity=0),
            self.progress_counters,
            self.progress
        ])

        self.content: ft.Column = self.wrapper
        self.bgcolor: ft.colors = ft.colors.BLACK12
        self.border_radius: ft.BorderRadius = ft.BorderRadius(10,10,10,10)
        self.border: ft.border = ft.border.all(.5)
        self.padding: ft.Padding = ft.Padding(20,20,20,20)

        self.default()

    def success(self):
        """Theme mode when task was end succesfully."""
        self.progress.value = 1
        self.icon.name = ft.icons.TASK_ALT
        self.icon.color = ft.colors.GREEN
        self.border = ft.border.all(.5, ft.colors.GREEN)
        self.update()

    def unsuccess(self, exception):
        """Theme mode when task was end unsuccesfully."""
        self.progress.value = 0
        self.icon.name = ft.icons.ERROR
        self.icon.color = ft.colors.RED
        self.icon.tooltip = str(exception)
        self.border = ft.border.all(.5, ft.colors.RED)
        self.update()

    def default(self):
        """Theme mode when task was init."""
        self.border = ft.border.all(.5, ft.colors.ORANGE)
        self.icon.color = ft.colors.ORANGE_500

    @property
    def total(self) -> int:
        """Get current total value of progress bar."""
        return self.current_total.value

    @total.setter
    def total(self, count: int) -> None:
        self.current_total.value = count
        self.update()

    @property
    def value(self) -> int:
        """Get current value of progress bar."""
        return self.current_value.value

    @value.setter
    def value(self, value: int) -> None:
        self.current_value.value = value
        self.progress.value = value / self.current_total.value
        self.update()

    def callback(self):
        """Callback"""
        self.update()
