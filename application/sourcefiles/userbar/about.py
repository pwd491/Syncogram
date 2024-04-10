import flet as ft

from ..config import APP_NAME
from ..config import APP_VERSION
from ..config import APP_REPOSITORY_GIT_PULL

class AboutApplication(ft.Text):
    def __init__(self) -> None:
        super().__init__()
        self.value = f"If you found a bug, you can send feedback.\n{APP_NAME} v{APP_VERSION}"
        self.size = 9
        self.opacity = .5
        self.text_align = ft.TextAlign.CENTER


class FeedBack(ft.TextButton):
    def __init__(self) -> None:
        super().__init__()
        self.url = APP_REPOSITORY_GIT_PULL
        self.style = ft.ButtonStyle()
        self.content = ft.Text()
        self.content.value = "Send feedback"
        self.content.size = 11
        self.content.text_align = ft.TextAlign.CENTER
        self.width = 200
