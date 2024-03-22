from typing import Literal
from screeninfo import get_monitors

def screensize() -> tuple[int, int] | tuple[Literal[1920], Literal[1080]]:
    """
    Returns the primary resolution of the monitor, 
    otherwise Full HD is used by default.
    """
    for monitor in get_monitors():
        if monitor.is_primary:
            return (monitor.width, monitor.height)
    return (1920, 1080)
