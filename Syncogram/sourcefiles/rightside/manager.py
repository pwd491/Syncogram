from typing import Callable

from flet import Page

from ..components import Task
from ..database import SQLite
from ..utils import logging
from ..algorithms import algorithms

logger = logging()


class Manager:
    """The manager to control options UI and Coroutines."""
    @logger.catch()
    def __init__(self, page: Page, timeleft, _) -> None:
        self.database = SQLite()
        self.options = {
            "is_sync_fav": {
                "title": _("Synchronize my favorite messages between accounts."),
                "description": _(
                    "Sync messages in your favorite chat with the correct sequence, re-replies to messages and pinned messages. The program can synchronize up to 100 messages per clock cycle."
                ),
                "function": algorithms.sync_favorite_messages,
                "status": False,
                "ui": Task,
            },
            "is_sync_profile_name": {
                "title": _(
                    "Synchronize the first name, last name, biography and birthday of the profile."
                ),
                "description": _(
                    "Synchronization of the first name, last name, profile description and birthday. If you do not specify the data, it will be overwritten as empty fields."
                ),
                "function": algorithms.sync_profile_first_name_and_second_name,
                "status": False,
                "ui": Task,
            },
            "is_sync_profile_avatars": {
                "title": _("Synchronize account photos and videos avatars."),
                "description": _(
                    "Sync photo and video avatars in the correct sequence. If there are a lot of media files, the program sets an average limit between requests to the servers in order to circumvent the restrictions."
                ),
                "function": algorithms.sync_profile_avatars,
                "status": False,
                "ui": Task,
            },
            "is_sync_public_channels_and_groups": {
                "title": _("Synchronize public channels and groups."),
                "description": _(
                    "Synchronizes public channels ang groups. If the channel or groups was archived or pinned, the program will save these parameters."
                ),
                "function": algorithms.sync_public_channels_and_groups,
                "status": False,
                "ui": Task,
            },
            "is_sync_privacy": {
                "title": _("Synchronize privacy settings."),
                "description": _(
                    "Synchronizes the privacy settings for the account. If the sync account does not have Telegram Premium, then the corresponding premium settings will not be synchronized."
                ),
                "function": algorithms.sync_privacy_settings,
                "status": False,
                "ui": Task,
            },
            "is_sync_secure": {
                "title": _("Synchronize secure settings."),
                "description": _(
                    "Synchronizes the secure settings for the account. It includes synchronization of sensitive content, TTL messages and account."
                ),
                "function": algorithms.sync_secure_settings,
                "status": False,
                "ui": Task,
            },
            "is_sync_stickers_emojis_gifs": {
                "title": _("Synchronize stickers, emojis and gifs."),
                "description": _(
                    "Synchronizes the stickers sets, emojis and saved gifs. It also enables automatic transfer of archived stickers or emojis, and faved stickers."
                ),
                "function": algorithms.sync_stickers_emojis_gifs,
                "status": False,
                "ui": Task,
            },
            "is_sync_bots": {
                "title": _("Synchronize bots."),
                "description": _(
                    "Synchronizes the list of bots. Attention, this function does not transfer the message history."
                ),
                "function": algorithms.sync_bots,
                "status": False,
                "ui": Task,
            },
        }
        self.callback()

    @logger.catch()
    def update_options_dict(self) -> None:
        """Get options dict and update <self.options>."""
        for key, value in self.database.get_options_as_dict().items():
            if key in self.options:
                self.options[key]["status"] = value
                self.options[key]["ui"] = Task(
                    self.options[key]["title"],
                    self.options[key]["description"],
                )

    @logger.catch()
    def get_ui_tasks(self) -> list[Task]:
        """Return UI list of will be execute tasks."""
        lst: list[Task] = []
        for option in self.options.values():
            if option["status"]:
                lst.append(option["ui"])
        return lst

    @logger.catch()
    def get_coroutines(self) -> list[Callable[[Task], None]]:
        """Return coroutines with UI objects.."""
        lst: list[Callable[[Task], None]] = []
        for option in self.options.values():
            if option["status"]:
                lst.append(option["function"](option["ui"]))
        return lst

    def callback(self):
        """Callback"""
        self.update_options_dict()
