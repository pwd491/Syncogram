import asyncio

from telethon import errors
from telethon.tl import patched
from telethon.helpers import TotalList

from .decorators import autoconnect
from ..components import Task
from ..telegram import UserClient
from ..utils import logging

logger = logging()

timeout: int = 0

@logger.catch()
@autoconnect
async def sync_favorite_messages(ui: Task, **kwargs):
    """
    An algorithm for forwarding messages to the recipient entity is
    implemented.
    """
    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    source: TotalList[patched.Message] = await sender.get_messages(
        "me", min_id=0, max_id=0, reverse=True
    )
    sender_entity = await sender.get_entity('me')
    recepient_entity = await recepient.get_entity('me')

    global timeout
    timeout = source.total / 325
    timeout = timeout if timeout <= 10 else 10

    async def pin_messages():
        if pinned:
            pin_timeout = 1 if len(pinned) <= 10 else 3.5
            for message in pinned.copy():
                while True:
                    try:
                        pin_id = ids.get(message.id)
                        pin_id = pin_id if pin_id is not None else 123
                        await asyncio.sleep(pin_timeout)
                        await recepient.pin_message(
                            'me',
                            pin_id
                        )
                        pinned.remove(message)
                        break
                    except errors.MessageIdInvalidError as e:
                        logger.error(e)
                        ui.message(e, True)
                        break
                    except errors.FloodWaitError as flood:
                        logger.warning(flood)
                        ui.message(flood)
                        ui.cooldown(flood)
                        pin_timeout += pin_timeout
                        await asyncio.sleep(flood.seconds)
                        ui.uncooldown()

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
    async def forward_messages_and_save_ids() -> None:
        global timeout
        if will_forward:
            while True:
                try:
                    await asyncio.sleep(timeout)
                    messages_to_recepient = await sender.forward_messages(
                        recepient_entity.username,
                        will_forward
                    )
                    will_delete.extend(messages_to_recepient)
                    break
                except (
                    errors.MessageIdsEmptyError,
                    errors.MessageIdInvalidError,
                    errors.GroupedMediaInvalidError
                ) as error:
                    logger.error(error)
                    ui.message(f"{error}. {len(will_forward)} messages wasn't sync.", True)
                    will_forward.clear()
                    return
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout = timeout + 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

            while True:
                try:
                    get_messages_from_sender = await recepient.get_messages(
                        sender_entity.username,
                        limit=len(messages_to_recepient),
                    )
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout = timeout + 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

            while True:
                try:
                    await asyncio.sleep(timeout)
                    send_to_saved_chat = await recepient.forward_messages(
                        'me',
                        get_messages_from_sender,
                        drop_author=True
                    )
                    break
                except (
                    errors.MessageIdsEmptyError,
                    errors.MessageIdInvalidError,
                    errors.GroupedMediaInvalidError
                ) as error:
                    logger.error(error)
                    ui.message(f"{error}. {len(get_messages_from_sender)} messages wasn't sync.", True)
                    will_forward.clear()
                    return
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout = timeout + 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

                send_to_saved_chat = reversed(send_to_saved_chat)
                was_saved.extend(send_to_saved_chat)
                await merge_old_and_new_ids()
                await pin_messages()
                will_forward.clear()
                was_saved.clear()

    async def reply_message_and_save_ids() -> None:
        global timeout
        if will_reply:
            while True:
                try:
                    await asyncio.sleep(timeout)
                    messages_to_recepient = await sender.forward_messages(
                        recepient_entity.username,
                        will_reply
                    )
                    will_delete.extend(messages_to_recepient)
                    break
                except (
                    errors.MessageIdsEmptyError,
                    errors.MessageIdInvalidError,
                    errors.GroupedMediaInvalidError
                ) as error:
                    logger.error(error)
                    ui.message(f"{error}. {len(will_reply)} messages wasn't sync.", True)
                    will_reply.clear()
                    return
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout = timeout + 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

            while True:
                try:
                    get_messages_from_sender = await recepient.get_messages(
                        sender_entity.username,
                        limit=len(messages_to_recepient),
                    )
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout = timeout + 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

                if get_messages_from_sender[-1].text == "":
                    while True:
                        try:
                            await asyncio.sleep(timeout)
                            send_to_saved_chat = await recepient.send_file(
                                'me',
                                file=get_messages_from_sender,
                                reply_to=ids.get(will_reply[-1].reply_to_msg_id)
                            )
                            break
                        except (
                            errors.MultiMediaTooLongError,
                            errors.EntityBoundsInvalidError
                        ) as error:
                            logger.error(error)
                            ui.message(error, True)
                            will_reply.clear()
                            break
                        except errors.FloodWaitError as flood:
                            logger.warning(flood)
                            ui.message(flood)
                            ui.cooldown(flood)
                            timeout = timeout + 5
                            await asyncio.sleep(flood.seconds)
                            ui.uncooldown()
                else:
                    while True:
                        try:
                            await asyncio.sleep(timeout)
                            send_to_saved_chat = await recepient.send_message(
                                'me',
                                message=get_messages_from_sender[-1].text,
                                reply_to=ids.get(will_reply[-1].reply_to_msg_id),
                                file=get_messages_from_sender \
                                    if len(get_messages_from_sender) > 1 else None
                            )
                            break
                        except (
                            errors.MsgIdInvalidError,
                            errors.MessageEmptyError,
                            errors.MessageTooLongError,
                        ) as error:
                            logger.error(error)
                            ui.message(error, True)
                            will_reply.clear()
                            break
                        except errors.FloodWaitError as flood:
                            logger.warning(flood)
                            ui.message(flood)
                            ui.cooldown(flood)
                            timeout = timeout + 5
                            await asyncio.sleep(flood.seconds)
                            ui.uncooldown()

                if isinstance(send_to_saved_chat, list):
                    send_to_saved_chat = reversed(send_to_saved_chat)
                    was_saved.extend(send_to_saved_chat)
                else:
                    was_saved.append(send_to_saved_chat)

                await merge_old_and_new_ids()
                await pin_messages()
                will_reply.clear()
                was_saved.clear()

    ids: dict[int, int] = {}

    will_delete: list[patched.Message] = [] # сообщения которые будут удалены
    will_forward: list[patched.Message] = [] # сообщения которые должны быть пересланны
    will_reply: list[patched.Message] = [] # группа сообщений или одно сообщение для ответа
    was_saved: list[patched.Message] = [] # сообщения которые были сохраненны успешно
    pinned: list[patched.Message] = []

    reply_flag = False
    grouped_id = 0
    last_grouped_id = 0

    ui.progress_counters.visible = True
    ui.total = source.total

    message: patched.Message
    for i, message in enumerate(source):
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
                        await forward_messages_and_save_ids()
                    else:
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
            logger.error(msg)
            ui.message(msg)
    ui.success()
