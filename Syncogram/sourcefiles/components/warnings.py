import flet as ft

from ..utils import config
from ..utils import logging
from ..utils import get_local_appication_version
from ..utils import get_remote_application_version

logger = logging()

class MinimumAccountsRequired(ft.Row):
    """Display animations warning min 2 accounts."""

    def __init__(self, _) -> None:
        super().__init__()
        self.sticker = ft.Lottie()
        # self.sticker.src = "stickers/sticker.json"
        self.sticker.src = "https://raw.githubusercontent.com/pwd491/Syncogram/dev/Syncogram/assets/stickers/sticker.json"
        self.sticker.repeat = True
        self.sticker.animate = True
        self.sticker.filter_quality = ft.FilterQuality.HIGH
        self.sticker.width = 200
        self.sticker_text = ft.Text()
        self.sticker_text.value = _("To get started, log in to at least 2 accounts")

        self.controls = [
            ft.Column([
                self.sticker,
                self.sticker_text
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ]
        self.alignment = ft.MainAxisAlignment.CENTER


class CancelAllTasks(ft.AlertDialog):
    """Cancel dialog to abort all tasks."""

    def __init__(self, page: ft.Page, event, _) -> None:
        super().__init__()
        self.page = page
        self.event = event
        self._ = _
        self.title = ft.Row([
            ft.Icon(ft.icons.WARNING),
            ft.Text(self._("Are you sure you want to cancel the current tasks?"))
        ])
        self.warning = ft.Text(
            self._("Attention, all synchronized information will not be reset, in order to start over, delete the information manually.")
        )
        self.warning.width = 150

        self.content = self.warning
        self.agree = ft.TextButton(self._("Yes"), on_click=self.__submit)
        self.disagree = ft.TextButton(self._("No"), on_click=self.__close)
        self.on_dismiss = self.__close

        self.actions = [self.agree, self.disagree]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    def __submit(self, e) -> None:
        self.open = False
        self.event.set()
        self.event.clear()
        self.page.dialog.clean()
        self.update()

    def __close(self, e) -> None:
        self.open = False
        self.event.clear()
        self.page.dialog.clean()
        self.update()

    async def __call__(self) -> None:
        await self.event.wait()

class UpdateApplicationAlert(ft.SnackBar):
    """This Class is object of dropdown alert. Display new available version."""

    def __init__(self, page: ft.Page, _) -> None:
        self.__version__ = get_local_appication_version()
        logger.info(f"Local Application version: [{self.__version__}]")
        self.__newest__ = get_remote_application_version()
        logger.info(f"Remote Application version: [{self.__newest__}]")

        self.icon = ft.Icon()
        self.icon.name = ft.icons.BROWSER_UPDATED
        self.text = ft.Text()
        self.text.value = _("The latest version is available. {} → {}").format(
            self.__version__,
            self.__newest__
        )
        self.text.color = ft.colors.WHITE
        self.button = ft.FilledButton(_("Download"))
        self.button.url = config()["GIT"]["RELEASES"]

        self.label = ft.Row([self.icon, self.text])

        self.content = ft.Row([self.label, self.button])
        self.content.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        super().__init__(self.content)
        self.duration = 10000
        self.bgcolor = ft.colors.BLACK87

        if self.__version__ != self.__newest__:
            page.snack_bar = self
            page.snack_bar.open = True
        page.update()

class RestartApplicationAlert(ft.SnackBar):
    def __init__(self, page: ft.Page, _) -> None:
        self.page = page
        self.content = ft.Text()
        self.content.value = _("Please, restart the application.")
        self.content.color = ft.colors.WHITE
        super().__init__(self.content)
        self.duration = 2000
        self.bgcolor = ft.colors.BLACK87

    def will_unmount(self):
        self.page.dialog.clean()
        self.page.update()
