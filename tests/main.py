import asyncio
import datetime
import random
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.patched import MessageService
from telethon.types import Message, TypeInputFile, Photo
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.photos import (
    UploadProfilePhotoRequest,
    UpdateProfilePhotoRequest,
)
from telethon.errors import MultiError
from functools import partial
from environments import API_HASH, API_ID, R_SESSION, S_SESSION

sender = TelegramClient(StringSession(S_SESSION), API_ID, API_HASH)
recepient = TelegramClient(StringSession(R_SESSION), API_ID, API_HASH)


async def main():

    if not sender.is_connected() or not recepient.is_connected():
        await sender.connect()
        await recepient.connect()

    photos = await sender.get_profile_photos("me")
    image_extension = ".jpeg"
    video_extension = ".mp4"
    photo: Photo
    for photo in reversed(photos):
        blob = await sender.download_media(photo, bytes)
        name = "Syncogram_" + datetime.datetime.strftime(
            photo.date, "%Y_%m_%d_%H_%M_%S"
        )
        if not photo.video_sizes:
            file = await recepient.upload_file(
                blob,
                file_name=name + image_extension
            )
            await recepient(UploadProfilePhotoRequest(file=file))
            continue
        file = await recepient.upload_file(
            blob,
            file_name=name + video_extension
        )
        await recepient(UploadProfilePhotoRequest(video=file))


if __name__ == "__main__":
    asyncio.run(main())
