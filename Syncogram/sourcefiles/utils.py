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
from loguru import logger
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_H
from flet import Page

def logging():
    """Configured and returned logger object."""
    directory = get_logs_dir()
    file = os.path.join(directory, "syncogram.log")
    logger.remove()
    logger.add(file)
    return logger

def get_work_dir() -> str:
    """Getting application work directory."""
    match sys.platform:
        case "win32":
            directory = os.path.join("AppData", "Local")
        case _:
            directory = os.path.join(".local", "share")
    return os.path.join(os.path.expanduser("~"), directory, "Syncogram")

def get_logs_dir() -> str:
    """Getting application logs directory."""
    directory = get_work_dir()
    return os.path.join(directory, "logs")

logger = logging()

@logger.catch()
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

@logger.catch()
def generate_username():
    """Generate random username."""
    letters = string.ascii_letters + string.digits
    return \
        ''.join(random.choice(letters) for _ in range(random.randint(5, 32)))

@logger.catch()
def config():
    """Search and open config.json file into reposotiry."""
    folder = os.path.dirname(os.path.dirname(__file__))
    cfg = os.path.join(folder, "config.json")

    if os.path.isfile(cfg):
        with open(cfg, "r", encoding="utf-8") as cfg:
            return json.load(cfg)
    return None

@logger.catch()
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

@logger.catch()
def get_local_appication_version():
    """Get local application version."""
    return config()["APP"]["VERSION"]

@logger.catch()
def get_local_database_version():
    """Get local database version."""
    return config()["DATABASE"]["VERSION"]

@logger.catch()
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

@logger.catch()
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

@logger.catch()
def get_locale(__file__, page: Page) -> gettext.gettext:
    """Getting system locale. (Bad way to get for darwin)"""
    domain = "base"
    path_to_locales = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "locales")
    )
    logger.info(f"The path to the localization files: {path_to_locales}")
    ru = gettext.translation(domain, path_to_locales, ["ru"], fallback=True)
    en = gettext.translation(domain, path_to_locales, ["en"], fallback=True)
    language = page.client_storage.get("language")

    if language is not None:
        if language == "ru":
            ru.install()
            return ru.gettext
        elif language == "en":
            en.install()
            return en.gettext

    logger.info(f"System platform: {sys.platform}")
    match sys.platform:
        case "darwin":
            if os.popen("defaults read -g AppleLanguages")\
                .read().strip().split('"')[1] in ["ru-RU"]:
                ru.install()
                _ = ru.gettext
                page.client_storage.set("language", "ru")
                logger.info("Set Russian language.")
            else:
                en.install()
                _ = en.gettext
                page.client_storage.set("language", "en")
                logger.info("Set English language.")
        case _:
            if getlocale()[0] in ["Russian_Russia", "ru_RU"]:
                ru.install()
                _ = ru.gettext
                page.client_storage.set("language", "ru")
                logger.info("Set Russian language.")
            else:
                en.install()
                _ = en.gettext
                page.client_storage.set("language", "en")
                logger.info("Set English language.")
    return _
