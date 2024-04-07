from .client import UserClient
from ..database import SQLite

class TelegramTasksManager:
    def __init__(self) -> None:
        self.database = SQLite()

        self.sender = UserClient(session="1ApWapzMBu7LeKaQf_xoTYfwP4Vyf5LTar9Y-LysxXetw4Sz8fl_WPLmx0ibXCJZJOUZWjSpJ4_SSL84rpOL6qoG4sN5bsBBezPS5AI08sYQuhrr8nMv7v3OjpEkyQ6BB_aYKzpQRRdbv3HLiwSouN_zgDW57z-b9bNCOz0XUfdL-sQ5z0aRl25qPTmTv4fdl37UAfa9Kev3MGPTY0DMnB0Famf1ob_v0kHPhrZqIo7kHZFlXnrKbjf5xWTsBu7R-JjxATLdvUA-2gmxmG5OfQFiKa7M8WqaG2YSY_GGDGuapmYq62uYp_Nm0FGS1iWZYd0h21wDU53B5lIcxAYVedswtOB7S71g=")
        self.recipient = UserClient()
        self.tasks = self.database.get_options()

    async def sync_saved_messages(self):
        """
        Важно учитывать:
        a. Последовательность отвеченных сообщений
        b. Контекст сообщения, для навигации используют хештег
        c. Статус о закреплении сообщения в диалоге
        
        Важно итерировать диалог, таким образом получится достичь максимума
        информации для каждого сообщения. Стоит коолекционировать данные, для
        следующих функций, где мы могли бы переиспользовать эти данные.
        """
        if not self.sender.is_connected():
            await self.sender.connect()

        data = await self.sender.get_messages("me")
        print(data)

        self.sender.disconnect()
