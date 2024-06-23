import asyncio
from datetime import datetime

from telethon import errors
from telethon.tl.functions import users, photos
from telethon.tl import types

from ..components import Task
from ..telegram import UserClient
from ..utils import logging
from .decorators import autoconnect

logger = logging()

@logger.catch()
@autoconnect
async def sync_profile_avatars(ui: Task, **kwargs) -> None:
    """
    The algorithm for synchronizing profile photo, fallback photo and video 
    avatars to the recipient's essence.
    """
    ui.default()
    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    try:
        avatars = await sender.get_profile_photos("me")
    except (errors.MaxIdInvalidError, errors.UserIdInvalidError) as error:
        logger.critical(error)
        ui.unsuccess(error)
        return


    try:
        user: types.users.UserFull = await sender(
            users.GetFullUserRequest('me')
        )
        fallback = user.full_user.fallback_photo
    except (errors.TimedOutError, errors.UserIdInvalidError) as error:
        logger.warning(error)

    ui.progress_counters.visible = True
    ui.total = avatars.total

    timeout = 3 if avatars.total < 45 else 5
    image_extension = ".jpeg"
    video_extension = ".mp4"

    photo: types.Photo
    for i, photo in enumerate(reversed(avatars), 1):
        await asyncio.sleep(timeout)
        try:
            blob = await sender.download_media(photo, bytes)
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.cooldown(flood)
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()
            blob = await sender.download_media(photo, bytes)

        name = "Syncogram_" + datetime.strftime(
            photo.date, "%Y_%m_%d_%H_%M_%S"
        )
        try:
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
        except (
            errors.FilePartsInvalidError,
            errors.ImageProcessFailedError,
            errors.PhotoCropSizeSmallError,
            errors.PhotoExtInvalidError,
            errors.StickerMimeInvalidError,
            errors.VideoFileInvalidError
        ) as error:
            logger.error(error)
            logger.info(photo.stringify())

        ui.value = i

    if fallback:
        try:
            blob = await sender.download_media(fallback, bytes)
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.cooldown(flood)
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()
            blob = await sender.download_media(fallback, bytes)

        name = "Syncogram_" + datetime.strftime(
            photo.date, "%Y_%m_%d_%H_%M_%S"
        )
        try:
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
        except (
            errors.FilePartsInvalidError,
            errors.ImageProcessFailedError,
            errors.PhotoCropSizeSmallError,
            errors.PhotoExtInvalidError,
            errors.StickerMimeInvalidError,
            errors.VideoFileInvalidError
        ) as error:
            logger.error(error)
            logger.info(photo.stringify())

    ui.success()
