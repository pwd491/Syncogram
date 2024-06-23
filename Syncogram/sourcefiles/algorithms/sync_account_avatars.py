import asyncio
from datetime import datetime

from telethon import errors
from telethon.tl.functions import users, photos
from telethon.tl import types

from .decorators import autoconnect
from ..components import Task
from ..telegram import UserClient
from ..utils import logging

logger = logging()

@logger.catch()
@autoconnect
async def sync_profile_avatars(ui: Task, **kwargs):
    """
    The algorithm for synchronizing profile photo and video avatars to 
    the recipient's essence.
    """
    ui.default()
    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    image_extension = ".jpeg"
    video_extension = ".mp4"
    photo: types.Photo
    try:
        avatars = await sender.get_profile_photos("me")
        user: types.users.UserFull = await sender(
            users.GetFullUserRequest('me')
        )
        fallback = user.full_user.fallback_photo

        ui.progress_counters.visible = True
        ui.total = avatars.total
        for i, photo in enumerate(reversed(avatars), 1):
            await asyncio.sleep(3)
            blob = await sender.download_media(photo, bytes)
            name = "Syncogram_" + datetime.strftime(
                photo.date, "%Y_%m_%d_%H_%M_%S"
            )

            await recepient(
                photos.UploadProfilePhotoRequest(
                    file=await recepient.upload_file(
                        blob,
                        file_name=name + image_extension
                    ) if not photo.video_sizes else None,
                    video=await recepient.upload_file(
                        blob,
                        file_name=name + video_extension
                    ) if photo.video_sizes else None
                )
            )
            ui.value = i

        if fallback:
            blob = await sender.download_media(fallback, bytes)
            name = "Syncogram_" + datetime.strftime(
                photo.date, "%Y_%m_%d_%H_%M_%S"
            )

            await recepient(
                photos.UploadProfilePhotoRequest(
                    fallback=True,
                    file=await recepient.upload_file(
                        blob,
                        file_name=name + image_extension
                    ) if not fallback.video_sizes else None,
                    video=await recepient.upload_file(
                        blob,
                        file_name=name + video_extension
                    ) if fallback.video_sizes else None
                )
            )
    except Exception as e:
        logger.error(e)
        ui.unsuccess(e)
        return
    ui.success()