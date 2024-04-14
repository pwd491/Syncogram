import base64
from json import loads
from urllib3 import request
from io import BytesIO
from typing import Literal

import flet as ft
import qrcode


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
        