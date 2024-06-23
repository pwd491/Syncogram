from typing import Coroutine
from ..telegram import UserClient
from ..database import SQLite

database = SQLite()

def autoconnect(func: Coroutine):
    """Decorator got token and connect user to server."""
    async def wrapper(*args):
        sender: UserClient = UserClient(database.get_session_by_status(1))
        recepient: UserClient = UserClient(database.get_session_by_status(0))
        if not sender.is_connected():
            await sender.connect()
        if not recepient.is_connected():
            await recepient.connect()
        return await func(*args, sender=sender, recepient=recepient)
    return wrapper