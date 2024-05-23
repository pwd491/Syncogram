import flet as ft

from ..database import SQLite

class Settings(ft.AlertDialog):
    """Class of settings."""
    def __init__(self, page: ft.Page, _) -> None:
        super().__init__()
        self.database: SQLite = SQLite()
        self.page: ft.Page = page

        """!!!"""
        self.options: list[int] = self.database.get_options()
        self.options: list[int] = self.options[1:] if self.options is not None else (0,0,0) # type: ignore

        self.c1 = ft.Checkbox(
            label=_("Sync my favorite messages"),
            value=bool(self.options[0]),
            disabled=False,
            tooltip=_("It will be available in the next updates")
        )
        self.c2 = ft.Checkbox(
            label=_("Sync my profile first name, last name and biography."),
            value=bool(self.options[1]),
            disabled=False
        )
        self.c3 = ft.Checkbox(
            label=_("Sync profile photos and videos."),
            value=bool(self.options[2]),
            disabled=False
        )
        """!!!"""

        x = [
            self.c1,
            self.c2,
            self.c3,
        ]
        x.sort(key=lambda x: x.disabled is True)

        self.column = ft.Container()
        self.column.content = ft.Column(x)
        self.column.content.scroll = ft.ScrollMode.AUTO
        self.column.height = 350

        self.wrapper = ft.Container()
        self.wrapper.content = self.column

        self.modal = True
        self.title = ft.Row([
            ft.Icon(ft.icons.SETTINGS),
            ft.Text(_("Settings"))
        ])
        self.content = self.wrapper
        self.actions = [
            ft.TextButton(_("Cancel"), on_click=self.close),
            ft.FilledButton(_("Save"), on_click=self.save),
        ]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    async def close(self, e) -> None:
        """Close dialog."""
        self.open = False
        self.page.dialog.clean()
        self.update()

    async def save(self, e) -> None:
        """Save options for primary user."""
        self.database.set_options(
            int(self.c1.value), # type: ignore
            int(self.c2.value), # type: ignore
            int(self.c3.value)
        )
        self.page.pubsub.send_all("update")
        self.page.dialog.clean()
        self.open = False
        self.update()