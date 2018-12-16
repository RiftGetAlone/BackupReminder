import os
import time
import ctypes
import calendar

from pathlib import Path
from ctypes import wintypes
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont

# Your backup day
backup_day = 28

font_name = "comic.ttf"
new_background = "current_day.jpg"
current_date = date.today()
days_left = backup_day - int(time.strftime("%d"))

if (days_left == 0):
    text = "BACKUP IS TODAY"
elif (days_left < 0):
    days_current_month = calendar.monthrange(current_date.year, current_date.month)[1]
    days_next_month = calendar.monthrange(current_date.year, current_date.month)[1]
    next_month_date = int(current_date) + int(timedelta(days=days_next_month))
    text = int(time.strftime("%d")) - 28 + int(calendar.monthrange(next_month_date.year, next_month_date.month)[1])
else:
    text = days_left

image_font = ImageFont.truetype(font_name, 200)
img = Image.open("background.jpg")
imgDrawer = ImageDraw.Draw(img)
width, height = imgDrawer.textsize(str(text), font=image_font)
imgDrawer.text(((1366 - width)/2, 250), str(text), font=image_font)
img.save(new_background)
image_path = os.path.join(Path(__file__).parent, new_background)
SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x0001
SPIF_SENDWININICHANGE = 0x0002
user32 = ctypes.WinDLL('user32')
SystemParametersInfo = user32.SystemParametersInfoW
SystemParametersInfo.argtypes = ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint
SystemParametersInfo.restype = wintypes.BOOL
SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
