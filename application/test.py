
from httpx import options
from sourcefiles import SQLite

database = SQLite()

opt_list = database.get_options()[1:]

class M:
    def __init__(self) -> None:
        self.options = {
            "is_sync_fav": {
                "function": self.sync_fav_messages,
                "status": bool()
            },
            "is_sync_pin_fav": {
                "function": self.sync_sequence_of_pinned_messages,
                "status": bool()
            }
        }

    async def sync_fav_messages(self):
        pass

    async def sync_sequence_of_pinned_messages(self):
        pass

    def test(self):
        list_of_options = database.get_options()[1:]
        
        for n, option in enumerate(self.options.items()):
            option[1].update({"status": bool(list_of_options[n])})

        print(self.options)

x = M()
x.test()
