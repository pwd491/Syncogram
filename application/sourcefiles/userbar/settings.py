from ..database import SQLite
import flet as ft

class SettingsDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page):
        self.page: ft.Page = page
        self.database = SQLite()
        """Подумай над этим блоком"""
        self.options = self.database.get_options()
        self.options = self.options if not None else (0, 0, 0)

        self.c1 = ft.Checkbox(label="Sync my favorite messages", value=False)
        self.c2 = ft.Checkbox(
            label="Save the sequence of pinned messages", value=False, disabled=True
        )
        """Подумай над этим блоком"""
        self.column = ft.Container()
        self.column.content = ft.Column([self.c1, self.c2])
        self.column.height = 350

        self.wrapper = ft.Container()
        self.wrapper.content = self.column

        super().__init__(
            modal=True,
            title=ft.Row([ft.Icon("SETTINGS"), ft.Text("Settings")]),
            content=self.wrapper,
            actions=[
                ft.TextButton("Cancel", on_click=self.close),
                ft.TextButton("Save", on_click=self.save),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def close(self, e):
        self.open = False
        self.update()

    def save(self, e):
        self.database.set_options(int(self.c1.value), int(self.c2.value))
        self.open = False
        self.update()