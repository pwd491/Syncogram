import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.patched import MessageService
from telethon.types import TypeInputUser
from environments import API_HASH, API_ID, R_SESSION, S_SESSION

sender = TelegramClient(StringSession(S_SESSION), API_ID, API_HASH)
recepient = TelegramClient(StringSession(R_SESSION), API_ID, API_HASH)


async def main():

    def length(lst):
        result = 0
        for i in range(len(lst)):
            if isinstance(lst[i], list):
                result += len(lst[i])
            else:
                result += 1
        return result

    async def forward(
        client: TelegramClient,
        from_peer: TypeInputUser,
        messages: list[int],
        to_peer: TypeInputUser,
        drop_author: bool | None,
    ):
        await client(
            ForwardMessagesRequest(
                from_peer, messages, to_peer, drop_author=drop_author
            )
        )

    if not sender.is_connected() or not recepient.is_connected():
        await sender.connect()
        await recepient.connect()

    sender_entity = await sender.get_entity("me")
    recepient_entity = await recepient.get_entity("me")

    source_messages = await sender.get_messages(
        sender_entity.username, min_id=0, max_id=0
    )

    group_id = 0
    grouped_message = []
    for message in source_messages:
        if not isinstance(message, MessageService):
            if message.grouped_id:
                if message.grouped_id == group_id:
                    grouped_message[-1].append(message.id)
                else:
                    grouped_message.append([])
                    grouped_message[-1].append(message.id)
                    group_id = message.grouped_id
                continue
            else:
                grouped_message.append(message.id)
                print(length(grouped_message))


if __name__ == "__main__":
    asyncio.run(main())
