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

import copy, json, locale, re, subprocess
from os import makedirs, environ
from PIL import Image
from os.path import exists

from .const import *


class ImageModes:
    CENTERED = 0
    STRETCH_FILL = 1
    REPEAT = 2


def getScreensInfo():
    out = {'screens': [], 'total_resolution': {}}

    try:
        result = subprocess.run(
            "xrandr | grep ' connected'", capture_output=True, shell=True,
            universal_newlines=True, check=True)

        result = result.stdout.strip()

        regex = re.compile(
            r"(?P<screen_id>[-\w+\d+]{1,})?.+\s+(?P<width>\d+)x(?P<height>\d+)"
            r"\+(?P<x>\d+)\+(?P<y>\d+)")

        for i in result.split('\n'):
            if i:
                info = regex.match(i)
                if info:
                    out['screens'].append(info.groupdict())
                    for key, value in out['screens'][-1].items():
                        if key == "screen_id":
                            continue
                        else:
                            out['screens'][-1][key] = int(value)

    except subprocess.CalledProcessError:
        return out

    try:
        result = subprocess.run(
            r"xdpyinfo | grep -oP 'dimensions:\s+\K\S+'", capture_output=True,
            shell=True, universal_newlines=True, check=True)

        result = result.stdout.strip()

        regex = re.compile(r"(?P<width>\d+)x(?P<height>\d+)")
        info = regex.match(result)

        if info:
            out['total_resolution'] = info.groupdict()
            for key, value in out['total_resolution'].items():
                out['total_resolution'][key] = int(value)

    except subprocess.CalledProcessError as e:
        return out

    return out


def getSetWallpaperCommand():
    desktop_session = \
        environ.get('XDG_CURRENT_DESKTOP') or environ.get('DESKTOP_SESSION')

    if desktop_session:
        desktop_session = desktop_session.lower()

    if (desktop_session == "lxqt") or (desktop_session == "lubuntu"):
        return f"pcmanfm-qt --set-wallpaper \"{WALLPAPER_PATH}\" --wallpaper-mode=center"

    elif desktop_session == "gnome":
        return ("gsettings set org.gnome.desktop.background picture-uri "
                f"\"{WALLPAPER_PATH}\" && gsettings set org.gnome.desktop.background "
                f"picture-uri-dark \"{WALLPAPER_PATH}\" && gsettings set "
                "org.gnome.desktop.background picture-options spanned")


def createImage(size: tuple, image_config: dict, reduction: bool = False):
    wallpaper = Image.new("RGB", size)

    def reSizeImage(value1, value2, new_size):
        if value1 > new_size:
            aspect_ration = value1 / value2
            value1 = new_size
            value2 = int(new_size / aspect_ration)
            value2 = value2 if value2 > 0 else 1

        elif value1 < new_size:
            aspect_ration = value1 / value2
            value1 = new_size
            value2 = int(new_size / aspect_ration)
            value2 = value2 if value2 > 0 else 1

        return value1, value2

    try:
        image = Image.open(image_config['image_path'])
    except Exception:
        return

    if image_config['image_mode'] == ImageModes.CENTERED:
        width, height = image.width, image.height

        if width > height:
            width, height = reSizeImage(width, height, size[0])
            box = (0, size[1] // 2 - height // 2)
        else:
            height, width = reSizeImage(height, width, size[1])
            box = (size[0] // 2 - width // 2, 0)

        image = image.resize((width, height))
        wallpaper.paste(image, box)

    elif image_config['image_mode'] == ImageModes.STRETCH_FILL:
        image = image.resize(size)
        wallpaper.paste(image, (0, 0))

    else:
        width, height = image.width, image.height

        if reduction:
            width = int(width * REDUCTION_PERCENTAGE)
            height = int(height * REDUCTION_PERCENTAGE)
            image = image.resize((width, height))

        if (width >= size[0]) and (height >= size[1]):
            wallpaper.paste(image, (0, 0))

        else:
            width_free = size[0]
            new_width = 0

            while width_free > 0:
                if width >= width_free:
                    new_width = width_free
                else:
                    new_width = width

                if height >= size[1]:
                    wallpaper.paste(image, (size[0]-width_free, 0))

                else:
                    height_free = size[1]
                    new_height = height

                    while height_free > 0:
                        wallpaper.paste(
                            image, (size[0]-width_free, size[1]-height_free))

                        if height >= height_free:
                            new_height = height_free
                            height_free = 0
                        else:
                            new_height = height
                            height_free -= height

                if width >= width_free:
                    width_free = 0
                else:
                    width_free -= width

    return wallpaper
