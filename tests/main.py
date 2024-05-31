import asyncio
import datetime
import random
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl import types
from telethon.tl.functions import messages
from telethon import events
from telethon import errors

from environments import API_HASH, API_ID, R_SESSION, S_SESSION

sender = TelegramClient(StringSession(S_SESSION), API_ID, API_HASH)
recepient = TelegramClient(StringSession(R_SESSION), API_ID, API_HASH)


async def main():

    if not sender.is_connected() or not recepient.is_connected():
        await sender.connect()
        await recepient.connect()

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
            print(e)

    stickers_list: types.messages.AllStickers = await sender(
        messages.GetAllStickersRequest(0)
    )
    stickers: list[types.TypeStickerSet] = stickers_list.sets

    emojis_list: types.messages.AllStickers = await sender(
        messages.GetEmojiStickersRequest(0)
    )
    emojis: list[types.TypeStickerSet] = emojis_list.sets

    gifs_list: types.messages.SavedGifs = await sender(
        messages.GetSavedGifsRequest(0)
    )
    gifs: list[types.TypeDocument] = gifs_list.gifs
    
    will_delete = []
    if gifs:
        for i, gif in enumerate(reversed(gifs), 1):
            await asyncio.sleep(timeout)
            message = await sender.send_file(r_entity.username, gif)
            will_delete.append(message)

    if will_delete:
        await sender.delete_messages(r_entity.username, will_delete)

    if stickers:
        for i, sticker in enumerate(reversed(stickers), 1):
            await asyncio.sleep(timeout)
            await recepient(
                messages.InstallStickerSetRequest(
                    stickerset=types.InputStickerSetShortName(
                        sticker.short_name
                    ),
                    archived=False
                )
            )

    if emojis:
        for i, emoji in enumerate(reversed(emojis), 1):
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
            except errors.StickersetInvalidError:
                continue


if __name__ == "__main__":
    asyncio.run(main())
