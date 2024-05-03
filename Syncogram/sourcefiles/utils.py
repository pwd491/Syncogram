import os
import base64
import json
import random
import string
from json import loads
from requests import request
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


def generate_username():
    """Generate random username."""
    letters = string.ascii_letters + string.digits
    return \
        ''.join(random.choice(letters) for _ in range(random.randint(5, 32)))
    

if __name__ == '__main__':
    generate_username()

def config():
    dir = os.path.dirname(os.path.dirname(__file__))
    cfg = os.path.join(dir, "config.json")

    if os.path.isfile(cfg):
        with open(cfg, "r", encoding="utf-8") as cfg:
            return json.load(cfg)
        
def get_remote_application_version():
    return \
    loads(
        request(
            "GET", 
            config()["GIT"]["REMOTE_CONFIG_URL"],
            timeout=15
        ).text
    )["APP"]["VERSION"]

def get_local_appication_version():
    return config()["APP"]["VERSION"]

def get_local_database_version():
    return config()["DATABASE"]["VERSION"]

def get_remote_database_version():
    return \
    loads(
        request(
            "GET", 
            config()["GIT"]["REMOTE_CONFIG_URL"],
            timeout=15
        ).text
    )["DATABASE"]["VERSION"]


def check_db_version(__version__) -> tuple | None:
    remote_app_version = get_remote_application_version()
    local_app_version = get_local_appication_version()
    remote_db_version = get_remote_database_version()
    local_db_version = __version__

    if local_db_version != remote_db_version and \
          local_app_version == remote_app_version:
        return (True, remote_db_version)


def newest_version(page: ft.Page, _) -> None:
    __version__ = get_local_appication_version()
    __newest__ = get_remote_application_version()
    if __version__ != __newest__:
        icon = ft.Icon()
        icon.name = ft.icons.BROWSER_UPDATED
        text = ft.Text()
        text.value = _("The latest version is available. {} → {}").format(
            __version__,
            __newest__
        )
        text.color = ft.colors.WHITE

        upper = ft.Row([icon, text])

        btn = ft.FilledButton(_("Download"))
        btn.url = config()["GIT"]["RELEASES"]
        wrapper = ft.Row([upper, btn])
        wrapper.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        snack = ft.SnackBar(wrapper)
        snack.duration = 10000
        snack.bgcolor = ft.colors.BLACK87
        page.snack_bar = snack
        page.snack_bar.open = True
        page.update()