"""Component to show snack alert dialog on the bottom of page."""
import flet as ft

from ..utils import config
from ..utils import get_local_appication_version
from ..utils import get_remote_application_version


class UpdateApplicationAlert(ft.SnackBar):
    """This Class is object of dropdown alert. Show new available version."""
    def __init__(self, page: ft.Page, _):
        self.__version__ = get_local_appication_version()
        self.__newest__ = get_remote_application_version()

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
