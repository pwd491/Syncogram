import asyncio
import datetime
import random
import time
from typing import Dict
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl import types
from telethon.tl.functions import messages
from telethon import events
from telethon import errors
from telethon.tl.custom import Dialog
from telethon.tl import patched
from telethon.helpers import TotalList

from environments import API_HASH, API_ID, R_SESSION, S_SESSION, M_SESSION

sender = TelegramClient(StringSession(R_SESSION), API_ID, API_HASH)
# sender = TelegramClient(StringSession(S_SESSION), API_ID, API_HASH)
recepient = TelegramClient(StringSession(M_SESSION), API_ID, API_HASH)


async def main():
    """
    An algorithm for forwarding messages to the recipient entity is
    implemented.
    """
    ui.default()
    sender = self.client(self.database.get_session_by_status(1))
    recepient = self.client(self.database.get_session_by_status(0))

    if not sender.is_connected() or not recepient.is_connected():
        await sender.connect()
        await recepient.connect()

    source: TotalList[patched.Message] = await sender.get_messages(
        "me", min_id=0, max_id=0, reverse=True
    )
    sender_entity = await sender.get_entity('me')
    recepient_entity = await recepient.get_entity('me')

    async def pin_messages():
        if pinned:
            timeout = .5
            for message in pinned.copy():
                try:
                    pin_id = ids.get(message.id)
                    pin_id = pin_id if pin_id is not None else 123
                    await asyncio.sleep(timeout)
                    await recepient.pin_message(
                        'me',
                        pin_id
                    )
                except errors.MessageIdInvalidError:
                    continue
                except errors.FloodWaitError as flood:
                    timeout += timeout
                    await asyncio.sleep(flood.seconds)
                finally:
                    pinned.remove(message)

    async def merge_old_and_new_ids():
        if will_forward:
            for k, message in enumerate(will_forward):
                ids.setdefault(
                    message.id,
                    was_saved[k].id
                )
        elif will_reply:
            for k, message in enumerate(will_reply):
                ids.setdefault(
                    message.id,
                    was_saved[k].id
                )
    async def forward_messages_and_save_ids():
        if will_forward:
            try:
                await asyncio.sleep(timeout)
                messages_to_recepient = await sender.forward_messages(
                    recepient_entity.username,
                    will_forward
                )
                will_delete.extend(messages_to_recepient)

                get_messages_from_sender = await recepient.get_messages(
                    sender_entity.username,
                    limit=len(messages_to_recepient),
                )

                send_to_saved_chat = await recepient.forward_messages(
                    'me',
                    get_messages_from_sender,
                    drop_author=True
                )
                send_to_saved_chat = reversed(send_to_saved_chat)
                was_saved.extend(send_to_saved_chat)
                await merge_old_and_new_ids()
                await pin_messages()
                will_forward.clear()
                was_saved.clear()
            except errors.FloodWaitError as flood:
                await asyncio.sleep(flood.seconds)

    async def reply_message_and_save_ids():
        if will_reply:
            try:
                await asyncio.sleep(timeout)
                messages_to_recepient = await sender.forward_messages(
                    recepient_entity.username,
                    will_reply
                )
                will_delete.extend(messages_to_recepient)

                get_messages_from_sender = await recepient.get_messages(
                    sender_entity.username,
                    limit=len(messages_to_recepient),
                )
                if get_messages_from_sender[-1].text == "":
                    send_to_saved_chat = await recepient.send_file(
                        'me',
                        file=get_messages_from_sender,
                        reply_to=ids.get(will_reply[-1].reply_to_msg_id)
                    )
                else:
                    send_to_saved_chat = await recepient.send_message(
                        'me',
                        message=get_messages_from_sender[-1].text,
                        reply_to=ids.get(will_reply[-1].reply_to_msg_id),
                        file=get_messages_from_sender \
                            if len(get_messages_from_sender) > 1 else None
                    )

                if isinstance(send_to_saved_chat, list):
                    send_to_saved_chat = reversed(send_to_saved_chat)
                    was_saved.extend(send_to_saved_chat)
                else:
                    was_saved.append(send_to_saved_chat)

                await merge_old_and_new_ids()
                await pin_messages()
                will_reply.clear()
                was_saved.clear()
            except errors.FloodWaitError as flood:
                await asyncio.sleep(flood.seconds)

    ids: Dict[int, int] = {}

    will_delete: list[patched.Message] = [] # сообщения которые будут удалены
    will_forward: list[patched.Message] = [] # сообщения которые должны быть пересланны
    will_reply: list[patched.Message] = [] # группа сообщений или одно сообщение для ответа
    was_saved: list[patched.Message] = [] # сообщения которые были сохраненны успешно
    pinned: list[patched.Message] = []

    reply_flag = False
    grouped_id = 0
    last_grouped_id = 0
    timeout = 5

    ui.progress_counters.visible = True
    ui.total = source.total

    message: patched.Message
    for k, message in enumerate(source):
        if not isinstance(message, patched.MessageService):
            if message.pinned:
                pinned.append(message)
            if message.grouped_id and reply_flag:
                if message.grouped_id == grouped_id:
                    will_reply.append(message)
                    ui.value = i
                    continue
            if message.is_reply:
                if message.grouped_id:
                    if message.grouped_id == grouped_id:
                        will_reply.append(message)
                    else:
                        await forward_messages_and_save_ids()
                        await reply_message_and_save_ids()
                        grouped_id = message.grouped_id
                        reply_flag = True
                        will_reply.append(message)
                else:
                    await forward_messages_and_save_ids()
                    will_reply.append(message)
                    await reply_message_and_save_ids()
            else:
                await reply_message_and_save_ids()
                reply_flag = False
                if len(will_forward) < 90:
                    will_forward.append(message)
                    last_grouped_id = message.grouped_id
                else:
                    if message.grouped_id:
                        if message.grouped_id == last_grouped_id:
                            ui.value = i
                            continue
                        print(f"Пересылка за раз: {len(will_forward)}")
                        await forward_messages_and_save_ids()
                    else:
                        print(f"Пересылка за раз: {len(will_forward)}")
                        await forward_messages_and_save_ids()
        ui.value = i

    if will_forward:
        await forward_messages_and_save_ids()
        await pin_messages()

    if will_reply:
        await reply_message_and_save_ids()
        await pin_messages()

    if pinned:
        await pin_messages()

    if will_delete:
        try:
            await sender.delete_messages(
                recepient_entity.username,
                will_delete
            )
        except errors.MessageIdInvalidError as msg:
            print(msg.message, msg.code)
    


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time() - start
    print(end)