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
    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    s_entity: types.User = await sender.get_entity('me')
    r_entity: types.User = await recepient.get_entity('me')

    timeout = 5

    @recepient.on(events.NewMessage(
        from_users=[s_entity.username], func=lambda e: e.message.gif)
    )
    async def gifhook(event: events.NewMessage.Event):
        gif: types.Document = event.message.gif
        try:
            await recepient(
                messages.SaveGifRequest(
                    types.InputDocument(
                        gif.id,
                        gif.access_hash,
                        gif.file_reference
                    ),
                    unsave=False
                )
            )
        except Exception as e:
            logger.warning(e)

    faved_stickers_list: types.messages.FavedStickers = await sender(
        messages.GetFavedStickersRequest(0)
    )
    faved_stickers: list[types.Document] = faved_stickers_list.stickers

    stickers_list: types.messages.AllStickers = await sender(
        messages.GetAllStickersRequest(0)
    )
    stickers: list[types.TypeStickerSet] = stickers_list.sets

    stickers_archived_list: types.messages.ArchivedStickers = await sender(
        messages.GetArchivedStickersRequest(
            offset_id=0,
            limit=0,
            masks=False,
            emojis=False
        )
    )
    stickers_archived: list[types.StickerSetCovered] = stickers_archived_list.sets

    emojis_list: types.messages.AllStickers = await sender(
        messages.GetEmojiStickersRequest(0)
    )
    emojis: list[types.TypeStickerSet] = emojis_list.sets

    emojis_archived_list: types.messages.ArchivedStickers = await sender(
        messages.GetArchivedStickersRequest(
            offset_id=0,
            limit=0,
            masks=False,
            emojis=True
        )
    )

    emojis_archived: list[types.StickerSetFullCovered] = emojis_archived_list.sets

    gifs_list: types.messages.SavedGifs = await sender(
        messages.GetSavedGifsRequest(0)
    )
    gifs: list[types.TypeDocument] = gifs_list.gifs

    ui.progress_counters.visible = True
    ui.total = len(faved_stickers) + len(stickers) + len(stickers_archived) \
            + len(emojis) + len(emojis_archived) + len(gifs)

    ui.value = 0
    if faved_stickers:
        for sticker in reversed(faved_stickers):
            await asyncio.sleep(timeout)
            try:
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
            except errors.StickerIdInvalidError as e:
                logger.warning(e)
                continue

    if stickers:
        for sticker in reversed(stickers):
            await asyncio.sleep(timeout)
            try:
                await recepient(
                    messages.InstallStickerSetRequest(
                        stickerset=types.InputStickerSetShortName(
                            sticker.short_name
                        ),
                        archived=False
                    )
                )
                ui.value += 1
            except errors.StickersetInvalidError as e:
                logger.warning(e)
                continue

    if stickers_archived:
        for sticker in reversed(stickers_archived):
            await asyncio.sleep(timeout)
            try:
                await recepient(
                    messages.InstallStickerSetRequest(
                        stickerset=types.InputStickerSetShortName(
                            sticker.set.short_name
                        ),
                        archived=True
                    )
                )
                ui.value += 1
            except errors.StickersetInvalidError as e:
                logger.warning(e)
                continue

    if emojis:
        for emoji in reversed(emojis):
            await asyncio.sleep(timeout)
            try:
                await recepient(
                    messages.InstallStickerSetRequest(
                        stickerset=types.InputStickerSetShortName(
                            emoji.short_name
                        ),
                        archived=False
                    )
                )
                ui.value += 1
            except errors.StickersetInvalidError as e:
                logger.warning(e)
                continue

    if emojis_archived:
        for emoji in reversed(emojis_archived):
            await asyncio.sleep(timeout)
            try:
                await recepient(
                    messages.InstallStickerSetRequest(
                        stickerset=types.InputStickerSetShortName(
                            emoji.set.short_name
                        ),
                        archived=True
                    )
                )
                ui.value += 1
            except errors.StickersetInvalidError as e:
                logger.warning(e)
                continue


    will_delete = []
    if gifs:
        for gif in reversed(gifs):
            await asyncio.sleep(timeout)
            try:
                message = await sender.send_file(r_entity.username, gif)
                will_delete.append(message)
                ui.value += 1
            except Exception as e:
                logger.error(e)
                continue

    if will_delete:
        try:
            await sender.delete_messages(r_entity.username, will_delete)
        except errors.MessageDeleteForbiddenError as e:
            logger.error(e)
            pass

    ui.success()