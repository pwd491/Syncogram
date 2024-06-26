"""Custom task container for view in mainscreen."""
import flet as ft

from ..components import Timeleft

class Task(ft.Container):
    """The task container."""
    def __init__(self, title: str, description: str, _ = None) -> None:
        super().__init__()
        # self.timeleft = Timeleft(_)

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

        self.progress_counters: ft.Row = ft.Row()
        self.progress_counters.controls = [self.current_value, self.current_total]
        self.progress_counters.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.progress_counters.visible = True

        self.cooldown_ui: ft.Container = ft.Container()
        self.cooldown_text: ft.Text = ft.Text()
        self.cooldown_text.value = "cooldown".upper()
        self.cooldown_text.size = 11
        self.cooldown_text.weight = ft.FontWeight.BOLD

        self.cooldown_ui.content = self.cooldown_text
        self.cooldown_ui.padding = ft.Padding(3,2,3,2)
        self.cooldown_ui.border = ft.border.all(1, ft.colors.RED)
        self.cooldown_ui.visible = False

        self.missdata_ui: ft.Container = ft.Container()
        self.missdata_text: ft.Text = ft.Text()
        self.missdata_text.value = "miss data".upper()
        self.missdata_text.size = 11
        self.missdata_text.weight = ft.FontWeight.BOLD

        self.missdata_ui.content = self.missdata_text
        self.missdata_ui.padding = ft.Padding(3,2,3,2)
        self.missdata_ui.border = ft.border.all(1, ft.colors.ORANGE_ACCENT)
        self.missdata_ui.visible = False

        self.header: ft.Row = ft.Row()
        self.header.controls = [
            self.title, self.missdata_ui, self.cooldown_ui, self.icon
        ]
        self.header.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.header.vertical_alignment = ft.CrossAxisAlignment.START

        self.detailed_button: ft.Container = ft.Container()
        self.detailed_button.content = ft.Row()
        self.detailed_button.expand = True
        self.detailed_button.bgcolor = ft.colors.with_opacity(
            0, ft.colors.WHITE
        )
        self.detailed_button.border_radius = ft.BorderRadius(5,5,5,5)
        self.detailed_button.height = 30
        self.detailed_button_text = ft.Container(
            ft.Text(_("Detailed"), size=12),
            padding=ft.Padding(4,0,0,0)
        )
        self.detailed_button_icon = ft.Icon(
               ft.icons.KEYBOARD_ARROW_DOWN, ft.colors.WHITE, 16
        )
        self.detailed_button_icon_wrapper = ft.Container(
            self.detailed_button_icon,
            padding=ft.Padding(0,0,1,0)
        )
        self.detailed_button.content.controls = [
            self.detailed_button_text,
            self.detailed_button_icon_wrapper
        ]
        self.detailed_button.content.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.detailed_button.on_click = self.__on_click
        self.detailed_button.on_hover = self.__on_hover
        self.detailed_button.on_long_press = self.__on_long_press

        self.detailed: ft.Row = ft.Row()
        self.detailed.controls = [self.detailed_button]

        self.extensive: ft.Column = ft.Column()
        self.extensive.controls = []
        self.extensive.visible = False

        self.wrapper: ft.Column = ft.Column([
            self.header,
            self.description,
            # ft.Divider(opacity=0),
            # self.timeleft,
            self.progress_counters,
            self.progress,
            self.detailed,
            self.extensive,
        ])

        self.content: ft.Column = self.wrapper
        self.bgcolor: ft.colors = ft.colors.BLACK12
        self.border_radius: ft.BorderRadius = ft.BorderRadius(10,10,10,10)
        self.border: ft.border = ft.border.all(.5)
        self.padding: ft.Padding = ft.Padding(20,20,20,20)

        self.default()

    def default(self) -> None:
        """Theme mode when task was init."""
        self.border = ft.border.all(.5, ft.colors.ORANGE)
        self.icon.name = ft.icons.UPDATE
        self.icon.color = ft.colors.ORANGE_500

    def success(self) -> None:
        """Theme mode when task was end succesfully."""
        self.progress.value = 1
        self.icon.name = ft.icons.TASK_ALT
        self.icon.color = ft.colors.GREEN
        self.border = ft.border.all(.5, ft.colors.GREEN)
        self.update()

    def unsuccess(self, exception) -> None:
        """Theme mode when task was end unsuccesfully."""
        self.progress.value = 0
        self.icon.name = ft.icons.ERROR
        self.icon.color = ft.colors.RED
        self.icon.tooltip = str(exception)
        self.border = ft.border.all(.5, ft.colors.RED)
        self.update()

    def cooldown(self, exception) -> None:
        """Theme mode when task on timeout."""
        self.cooldown_ui.visible = True
        self.icon.name = ft.icons.TIMER_10_SELECT
        self.icon.color = ft.colors.RED
        self.icon.tooltip = str(exception)
        self.cooldown_ui.tooltip = str(exception)
        self.border = ft.border.all(.5, ft.colors.RED)
        self.update()

    def uncooldown(self) -> None:
        """Reset timeout."""
        self.cooldown_ui.visible = False
        self.default()
        self.update()

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

    def __on_click(self, e: ft.TapEvent):
        if self.extensive.visible:
            self.extensive.visible = False
            self.detailed_button_icon.name = ft.icons.KEYBOARD_ARROW_DOWN
        else:
            self.extensive.visible = True
            self.detailed_button_icon.name = ft.icons.KEYBOARD_ARROW_UP
        self.detailed_button_icon.update()
        self.extensive.update()

    def __on_hover(self, e: ft.HoverEvent):
        if e.data == "true":
            self.detailed_button.bgcolor = ft.colors.with_opacity(
                .1, ft.colors.BLUE_200
            )
        else:
            self.detailed_button.bgcolor = ft.colors.with_opacity(
                .0, ft.colors.BLUE_200
            )
        self.detailed_button.update()

    def __on_long_press(self, e: ft.LongPressStartEvent):
        pass

    def message(self, message: str) -> None:
        """A message about the results."""
        self.extensive.controls.extend([
            ft.Text(value=message, selectable=True, size=12),
            ft.Divider()
        ])
        self.extensive.update()

    def callback(self):
        """Callback"""
        self.update()
