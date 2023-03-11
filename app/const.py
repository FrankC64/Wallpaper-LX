"""
    Wallpaper LX
    Copyright (C) 2023 FrankC64 <frankcedano64@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from os import getlogin
from os.path import abspath, dirname, join

# Paths
APP_PATH = dirname(dirname(abspath(__file__)))
APP_RESOURCES_PATH = join(APP_PATH, "resources")
LANG_JSON_PATH = join(APP_PATH, "lang.json")

CONFIG_PATH = f"/home/{getlogin()}/.config/Wallpaper-LX"
APP_DATA_PATH = join(CONFIG_PATH, "appdata.json")
WALLPAPER_PATH = join(CONFIG_PATH, "wallpaper.jpg")

# Dicts data
DEFAULT_APPDATA_JSON = {
    'geometry': "800x600+10+10", 'state': "normal", 'lang': "en",
    'images_configs': {}
}
IMAGE_CONFIG = {'image_path': '', 'image_mode': 0}

# Interface constants
BACKGROUND = "#FFFFFF"
FOREGROUND = "#000000"
BOLD_FONT1 = ("", 12, "bold")
BOLD_FONT2 = ("", 11, "bold")
LANG_JSON = {}

# Other constants
REDUCTION_PERCENTAGE = 0.10
CANVAS_WIDTH = 2500
CANVAS_HEIGHT = 2500
