import flet as ft


from ..utils import config
# from ..config import APP_NAME
# from ..config import APP_VERSION
# from ..config import APP_REPOSITORY_GIT_PULL

cfg = config()

class AboutApplication(ft.Text):
    def __init__(self, _) -> None:
        super().__init__()
        self.value = _("""If you found a bug, you can send feedback.\n{} v{}""").format(cfg["APP"]["NAME"], cfg["APP"]["VERSION"])
        self.size = 9
        self.opacity = .5
        self.text_align = ft.TextAlign.CENTER


class FeedBack(ft.TextButton):
    def __init__(self, _) -> None:
        super().__init__()
        self.url = cfg["GIT"]["REPO_ISSUES"]
        self.style = ft.ButtonStyle()
        self.content = ft.Text()
        self.content.value = _("Send feedback")
        self.content.size = 11
        self.content.text_align = ft.TextAlign.CENTER
        self.width = 200
