from datetime import timedelta
from flet import Container, Text, Padding

class Timeleft(Container):
    """
    A class for calculating the remaining time for completing current tasks.
    """
    def __init__(self, _) -> None:
        super().__init__()

        self.time = timedelta(seconds=0)
        self.text = Text()
        self.label = _("Approximate execution time:\xa0")
        self.text.value = f"{self.label} {self.time}"

        self.content = self.text
        self.padding = Padding(20,0,0,0)

    def __iadd__(self, value: int | float):
        self.time = self.time + timedelta(seconds=value)
        self.__represent()
        print(self.text.value)
        return self

    def __isub__(self, value: int | float):
        self.time = self.time - timedelta(seconds=value)
        self.__represent()
        print(self.text.value)
        return self

    def __represent(self):
        self.text.value = f"{self.label} {self.time}"
        self.text.update()