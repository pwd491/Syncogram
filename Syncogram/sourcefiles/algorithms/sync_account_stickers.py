import asyncio

from telethon import errors
from telethon.tl.functions import messages
from telethon.tl import types
from telethon import events

from .decorators import autoconnect
from ..components import Task
from ..telegram import UserClient
from ..utils import logging

logger = logging()


@logger.catch()
@autoconnect
async def sync_stickers_emojis_gifs(ui: Task, **kwargs):
    """The algorithm for synchronizing stickers and other things."""
    async def __get_entity(client: UserClient) -> types.User | None:
        while True:
            try:
                request: types.User = await client.get_entity('me')
                return request
            except (
                errors.AuthKeyPermEmptyError,
                errors.MemberNoLocationError,
                errors.NeedMemberInvalidError,
                errors.SessionPasswordNeededError,
                errors.TimeoutError
            ) as error:
                logger.critical(error)
                ui.message(error)
                return
            except errors.FloodWaitError as flood:
                logger.warning(flood)
                ui.message(flood)
                ui.cooldown(flood)
                await asyncio.sleep(flood.seconds)
                ui.uncooldown()

    async def is_already_have():
        pass

    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    s_entity: types.User = await __get_entity(sender)
    r_entity: types.User = await __get_entity(recepient)

    if s_entity is None or r_entity is None:
        ui.unsuccess()
        return

    while True:
        try:
            faved_stickers_list: types.messages.FavedStickers = await sender(
                messages.GetFavedStickersRequest(0)
            )
            faved_stickers: list[types.Document] = faved_stickers_list.stickers
            break
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    while True:
        try:
            stickers_list: types.messages.AllStickers = await sender(
                messages.GetAllStickersRequest(0)
            )
            stickers: list[types.TypeStickerSet] = stickers_list.sets
            break
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    while True:
        try:
            stickers_archived_list: types.messages.ArchivedStickers = await sender(
                messages.GetArchivedStickersRequest(
                    offset_id=0,
                    limit=0,
                    masks=False,
                    emojis=False
                )
            )
            stickers_archived: list[types.StickerSetCovered] = stickers_archived_list.sets
            break
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    while True:
        try:
            emojis_list: types.messages.AllStickers = await sender(
                messages.GetEmojiStickersRequest(0)
            )
            emojis: list[types.TypeStickerSet] = emojis_list.sets
            break
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    while True:
        try:
            emojis_archived_list: types.messages.ArchivedStickers = await sender(
                messages.GetArchivedStickersRequest(
                    offset_id=0,
                    limit=0,
                    masks=False,
                    emojis=True
                )
            )
            emojis_archived: list[types.StickerSetFullCovered] = emojis_archived_list.sets
            break
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    while True:
        try:
            gifs_list: types.messages.SavedGifs = await sender(
                messages.GetSavedGifsRequest(0)
            )
            gifs: list[types.TypeDocument] = gifs_list.gifs
            break
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    ui.total = len(faved_stickers) + len(stickers) + len(stickers_archived) \
            + len(emojis) + len(emojis_archived) + len(gifs)
    ui.progress_counters.visible = True
    timeout = 5

    if faved_stickers:
        for sticker in reversed(faved_stickers):
            while True:
                try:
                    await asyncio.sleep(timeout)
                    await recepient(
                        messages.FaveStickerRequest(
                            id=types.InputDocument(
                                id=sticker.id,
                                access_hash=sticker.access_hash,
                                file_reference=sticker.file_reference
                            ),
                            unfave=False
                        )
                    )
                    ui.value += 1
                    break
                except errors.StickerIdInvalidError as error:
                    logger.warning(error)
                    ui.message(error, True)
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout += 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()
    if stickers:
        for sticker in reversed(stickers):
            while True:
                try:
                    await asyncio.sleep(timeout)
                    await recepient(
                        messages.InstallStickerSetRequest(
                            stickerset=types.InputStickerSetShortName(
                                sticker.short_name
                            ),
                            archived=False
                        )
                    )
                    ui.value += 1
                    break
                except errors.StickersetInvalidError as error:
                    logger.warning(error)
                    ui.message(error, True)
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout += 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

    if stickers_archived:
        for sticker in reversed(stickers_archived):
            while True:
                try:
                    await asyncio.sleep(timeout)
                    await recepient(
                        messages.InstallStickerSetRequest(
                            stickerset=types.InputStickerSetShortName(
                                sticker.set.short_name
                            ),
                            archived=True
                        )
                    )
                    ui.value += 1
                    break
                except errors.StickersetInvalidError as error:
                    logger.warning(error)
                    ui.message(error, True)
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout += 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

    if emojis:
        for emoji in reversed(emojis):
            while True:
                try:
                    await asyncio.sleep(timeout)
                    await recepient(
                        messages.InstallStickerSetRequest(
                            stickerset=types.InputStickerSetShortName(
                                emoji.short_name
                            ),
                            archived=False
                        )
                    )
                    ui.value += 1
                    break
                except errors.StickersetInvalidError as error:
                    logger.warning(error)
                    ui.message(error, True)
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout += 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

    if emojis_archived:
        for emoji in reversed(emojis_archived):
            while True:
                try:
                    await asyncio.sleep(timeout)
                    await recepient(
                        messages.InstallStickerSetRequest(
                            stickerset=types.InputStickerSetShortName(
                                emoji.set.short_name
                            ),
                            archived=True
                        )
                    )
                    ui.value += 1
                    break
                except errors.StickersetInvalidError as error:
                    logger.warning(error)
                    ui.message(error, True)
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout += 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

    if gifs:
        timeout_gif = 1 if len(gifs) < 50 else 2 if 20 < len(gifs) < 50 else 3.5
        for gif in reversed(gifs):
            while True:
                try:
                    request = await sender.download_file(gif, bytes)
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout_gif += 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

            while True:
                try:
                    await asyncio.sleep(timeout_gif)
                    upload = await recepient.upload_file(
                        request, file_name="gif.mp4"
                    )
                    media = (await recepient._file_to_media(upload))[1]
                    x: types.MessageMediaDocument = await recepient(
                    messages.UploadMediaRequest('me', media)
                    )
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout_gif += 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

            while True:
                try:
                    await recepient(
                        messages.SaveGifRequest(
                            types.InputDocument(
                                id=x.document.id,
                                access_hash=x.document.access_hash,
                                file_reference=x.document.file_reference
                            ),
                            unsave=False
                        )
                    )
                    ui.value += 1
                    break
                except errors.FileReferenceExpiredError as error:
                    logger.error(error)
                    ui.message(error, True)
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout_gif += 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()


    ui.success()
