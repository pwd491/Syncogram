import flet as ft

from ..components import MinimumAccountsRequired
from ..components import StartAllTasksButton
from ..components import Settings
from ..database import SQLite
from .manager import Manager


class Taskbar(ft.Container):
    """The taskbar container side."""
    def __init__(self, page: ft.Page, _) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.database: SQLite = SQLite()
        self.database.check_update()
        self._: str = _

        self.manager = Manager(self.page, _)
        self.start_button = StartAllTasksButton(
            self.page,
            self.manager.get_coroutines_with_ui,
            self._
        )

        self.settings = Settings(self.page, self._)
        self.required = MinimumAccountsRequired(self._)

        self.wrapper_side_column = ft.Column([])
        self.wrapper_side_column.alignment = ft.MainAxisAlignment.START
        self.wrapper_side_column.scroll = ft.ScrollMode.AUTO
        self.wrapper_side_column.expand = True

        self.wrapper_side = ft.Container()
        self.wrapper_side.content = ft.Row([self.wrapper_side_column])
        self.wrapper_side.content.vertical_alignment = ft.CrossAxisAlignment.START
        self.wrapper_side.expand = True

        self.wrapper_footer = ft.Container()
        self.wrapper_footer.content = ft.Row([self.start_button])
        self.wrapper_footer.content.alignment = ft.MainAxisAlignment.END
        self.wrapper_footer.height = 50
        self.wrapper_footer.border_radius = ft.BorderRadius(10,10,10,10)
        self.wrapper_footer.bgcolor = ft.colors.BLACK12

        self.wrapper = ft.Column([])
        self.content = self.wrapper
        self.expand = True
        self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER)
        self.border_radius = ft.BorderRadius(10, 10, 10, 10)
        self.padding = ft.Padding(20, 40, 20, 20)
        self._update()

    def _update(self):
        self.wrapper.controls.clear()
        if len(self.database.get_users()) >= 2:
            self.wrapper_side_column.controls.clear()
            self.wrapper_side_column.controls.extend(
                self.manager.get_ui_tasks()
            )
            self.wrapper.controls.append(self.wrapper_side)
            self.wrapper.controls.append(self.wrapper_footer)
            return
        self.wrapper.controls.append(self.required)
        self.wrapper.alignment = ft.MainAxisAlignment.CENTER


    def callback(self) -> None:
        """Callback."""
        self.manager.callback()
        self._update()
        self.update()
