from os import getenv

from dotenv import load_dotenv


from .client import UserClient
from ..database import SQLite
from .task import CustomTask

from flet import Text


load_dotenv()

class Manager:
    def __init__(self, mainwindow = None) -> None:
        self.database = SQLite()
        self.mainwindow = mainwindow
        self.session: str = getenv("AUTH_TOKEN", "AUTH_TOKEN")

        self.sender = UserClient(self.session)
        self.recipient = UserClient()


    async def build(self):
        options = self.database.get_options()[1:]
        print(options)


    async def sync_saved_messages(self, e):
        """
        Важно учитывать:
        a. Последовательность отвеченных сообщений
        b. Контекст сообщения, для навигации используют хештег
        c. Статус о закреплении сообщения в диалоге
        
        Важно итерировать диалог, таким образом получится достичь максимума
        информации для каждого сообщения. Стоит коолекционировать данные, для
        следующих функций, где мы могли бы переиспользовать эти данные.
        """
        task = CustomTask("Hello world")
        self.mainwindow.wrapper_side_column.controls.append(task)
        await self.mainwindow.update_async()



        if not self.sender.is_connected():
            await self.sender.connect()

        data = await self.sender.get_messages("me")

        self.sender.disconnect()
