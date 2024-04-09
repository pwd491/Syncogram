from types import NoneType
from ..database import SQLite
import flet as ft

class SettingsDialog(ft.AlertDialog):
    def __init__(self, update_mainwin) -> None:
        super().__init__()
        self.database = SQLite()
        self.update_mainwin = update_mainwin

        """!!!"""
        self.options: list[int] = self.database.get_options()
        self.options: list[int] = self.options[1:] if self.options is not None else (0,0,0) # type: ignore

        self.c1 = ft.Checkbox(
            label="Sync my favorite messages",
            value=bool(self.options[0]),
            disabled=True
        )
        self.c2 = ft.Checkbox(
            label="Save the sequence of pinned messages",
            value=bool(self.options[1]),
            disabled=True
        )
        self.c3 = ft.Checkbox(
            label="Sync my profile first name and second name.",
            value=bool(self.options[2]),
            disabled=False
        )
        """!!!"""

        x = []


        self.column = ft.Container()
        self.column.content = ft.Column([self.c3, self.c1, self.c2])
        self.column.height = 350

        self.wrapper = ft.Container()
        self.wrapper.content = self.column


        self.modal = True
        self.title = ft.Row([ft.Icon("SETTINGS"), ft.Text("Settings")])
        self.content = self.wrapper
        self.actions = [
            ft.TextButton("Cancel", on_click=self.close),
            ft.FilledButton("Save", on_click=self.save),
        ]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    async def close(self, e) -> None:
        self.open = False
        await self.update_async()

    async def save(self, e) -> None:
        self.database.set_options(int(self.c1.value), int(self.c2.value), int(self.c3.value)) # type: ignore
        await self.update_mainwin()
        self.open = False
        await self.update_async()
