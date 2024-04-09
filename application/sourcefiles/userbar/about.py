from configparser import ConfigParser

import flet as ft

config = ConfigParser()
config.read("config.ini")

class AboutApplication(ft.Text):
    def __init__(self) -> None:
        super().__init__()
        self.version: str = config.get("APP", "APP_VERSION")

        self.value = f"If you found a bug, you can send feedback.\nSyncogram v{self.version}"
        self.size = 9
        self.opacity = .5
        self.text_align = ft.TextAlign.CENTER


class FeedBack(ft.TextButton):
    def __init__(self) -> None:
        super().__init__()
        self.url = config.get("REPO", "LINK_PULL_REQUEST")
        self.style = ft.ButtonStyle()
        self.content = ft.Text()
        self.content.value = "Send feedback"
        self.content.size = 11
        self.content.text_align = ft.TextAlign.CENTER
        self.width = 200
