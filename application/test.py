from screeninfo import get_monitors

SCREENWIDTH = 1280
SCREENHEIGHT = 960

for monitor in get_monitors():
    if monitor.is_primary:
        SCREENWIDTH: int = monitor.width
        SCREENHEIGHT: int = monitor.height
        break