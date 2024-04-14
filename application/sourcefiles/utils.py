import base64
from json import loads
from urllib3 import request
from io import BytesIO
from typing import Literal

import flet as ft
import qrcode

from screeninfo import get_monitors


def screensize() -> tuple[int, int] | tuple[Literal[1920], Literal[1080]]:
    """
    Returns the primary resolution of the monitor, 
    otherwise Full HD is used by default.
    """
    for monitor in get_monitors():
        if monitor.is_primary:
            return (monitor.width, monitor.height)
    return (1920, 1080)

def clr_on_secondary_container(platform_brightness, theme_mode,):
    if platform_brightness == "dark" and theme_mode == "system":
        return ft.colors.with_opacity(0.2, ft.colors.ON_SECONDARY_CONTAINER,)
    return ft.colors.with_opacity(0.5, ft.colors.ON_SECONDARY_CONTAINER,)

def clr_secondary_container(platform_brightness, theme_mode,):
    if platform_brightness == "dark" and theme_mode == "system":
        return ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER,)
    return ft.colors.with_opacity(1, ft.colors.SECONDARY_CONTAINER,)

def generate_qrcode(url):
    buffered = BytesIO()
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )
    QRcode.clear()
    QRcode.add_data(url)
    QRcode.make()
    img = QRcode.make_image(back_color=(40,47,54), fill_color=(255,255,255))
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

async def check_newest_version(page: ft.Page, __version__) -> None:
    __newest__ = loads(
        request(
            "GET", 
            "https://raw.githubusercontent.com/pwd491/Syncogram/dev/config.json"
            ).data
        )["APP"]["VERSION"]
    if __version__ != __newest__:
        icon = ft.Icon()
        icon.name = ft.icons.BROWSER_UPDATED
        text = ft.Text()
        text.value = "The latest version is available. {} → {}".format(
            __version__,
            __newest__
        )
        text.color = ft.colors.WHITE

        upper = ft.Row([icon, text])

        btn = ft.FilledButton("Download")
        wrapper = ft.Row([upper, btn])
        wrapper.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        snack = ft.SnackBar(wrapper)
        snack.duration = 10000
        snack.bgcolor = ft.colors.BLACK87
        page.snack_bar = snack
        page.snack_bar.open = True
        await page.update_async()