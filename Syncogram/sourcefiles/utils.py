import os
import sys
import json
import random
import string
import base64
import gettext
from locale import getlocale
from json import loads
from io import BytesIO

from requests import request
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_H


def generate_qrcode(url):
    """Generate QRCode by Telegram URL."""
    buffered = BytesIO()
    qrcode = QRCode(error_correction=ERROR_CORRECT_H)
    qrcode.clear()
    qrcode.add_data(url)
    qrcode.make()
    img = qrcode.make_image(back_color=(40,47,54), fill_color=(255,255,255))
    img.save(buffered, format="png")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def generate_username():
    """Generate random username."""
    letters = string.ascii_letters + string.digits
    return \
        ''.join(random.choice(letters) for _ in range(random.randint(5, 32)))

def config():
    """Search and open config.json file into reposotiry."""
    folder = os.path.dirname(os.path.dirname(__file__))
    cfg = os.path.join(folder, "config.json")

    if os.path.isfile(cfg):
        with open(cfg, "r", encoding="utf-8") as cfg:
            return json.load(cfg)
    return None

def get_remote_application_version():
    """Send GET request to remote config file."""
    return \
    loads(
        request(
            "GET", 
            config()["GIT"]["REMOTE_CONFIG_URL"],
            timeout=15
        ).text
    )["APP"]["VERSION"]

def get_local_appication_version():
    """Get local application version."""
    return config()["APP"]["VERSION"]

def get_local_database_version():
    """Get local database version."""
    return config()["DATABASE"]["VERSION"]

def get_remote_database_version():
    """Send GET request to remote config file."""
    return \
    loads(
        request(
            "GET", 
            config()["GIT"]["REMOTE_CONFIG_URL"],
            timeout=15
        ).text
    )["DATABASE"]["VERSION"]


def check_db_version(__version__) -> tuple | None:
    """Determines whether the application needs to be updated."""
    remote_app_version = get_remote_application_version()
    local_app_version = get_local_appication_version()
    remote_db_version = get_remote_database_version()
    local_db_version = __version__

    if local_db_version != remote_db_version and \
          local_app_version == remote_app_version:
        return (True, remote_db_version)
    return None

def get_locale(__file__) -> gettext.gettext:
    """Getting system locale. (Bad way to get for darwin)"""
    domain = "base"
    path_to_locales = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "locales")
    )
    ru = gettext.translation(domain, path_to_locales, ["ru"], fallback=True)
    en = gettext.translation(domain, path_to_locales, ["en"], fallback=True)

    match sys.platform:
        case "darwin":
            if os.popen("defaults read -g AppleLanguages")\
                .read().strip().split('"')[1] in ["ru-RU"]:
                ru.install()
                _ = ru.gettext
        case _:
            if getlocale()[0] in ["Russian_Russia", "ru_RU"]:
                ru.install()
                _ = ru.gettext
            else:
                en.install()
                _ = en.gettext
    return _
