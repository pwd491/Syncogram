import base64
from io import BytesIO
from typing import Literal

from flet import colors
import qrcode

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

def clr_on_secondary_container(platform_brightness, theme_mode,):
    if platform_brightness == "dark" and theme_mode == "system":
        return colors.with_opacity(0.2, colors.ON_SECONDARY_CONTAINER,)
    return colors.with_opacity(0.5, colors.ON_SECONDARY_CONTAINER,)

def clr_secondary_container(platform_brightness, theme_mode,):
    if platform_brightness == "dark" and theme_mode == "system":
        return colors.with_opacity(0.1, colors.SECONDARY_CONTAINER,)
    return colors.with_opacity(1, colors.SECONDARY_CONTAINER,)

def generate_qrcode(url):
    qr = qrcode.make(url)
    buffered = BytesIO()
    qr.save(buffered,format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
     