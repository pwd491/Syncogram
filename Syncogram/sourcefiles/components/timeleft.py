from datetime import timedelta
from flet import Container, Text


class Timeleft(Container):
    """
    A class for calculating the remaining time for completing current tasks.
    """
    def __init__(self, _) -> None:
        super().__init__()
        self.time = timedelta(seconds=0)
        self.text = Text()
        self.label = _("Execution time:")
        self.text.value = f"{self.label} {self.time}"
        self.text.size = 10
        self.content = self.text

    def __iadd__(self, value: int | float):
        self.time = self.time + timedelta(seconds=value)
        self.text.value = f"{self.label} {self.time}"
        self.text.update()
        return self

    def __isub__(self, value: int | float):
        self.time = self.time - timedelta(seconds=value)
        self.text.value = f"{self.label} {self.time}"
        self.text.update()
        return self
