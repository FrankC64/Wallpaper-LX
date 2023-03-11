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

__version__ = "1.0"
__author__ = "FrankC64"

import copy, json, subprocess
from tkinter import Tk, Button, Canvas, Entry, Frame, Label, Scrollbar, ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from os import getlogin
from os.path import abspath, dirname, exists, join

from .const import *
from .auxiliar import *

global_lang = "en"
lang_name = "English"
app_resources = {
    'appicon': None,
    'appicon-no-bg': None,
    'settings-icon': None,
    'about-icon': None
}
restart_app = True
window = None


class App(Tk):
    appdata: dict = {}
    screen_data: dict = {}
    focus_highlight_id: str = ""
    images_list: list = []
    last_tag: str = ""
    actives_screen: list = []

    def __init__(self):
        super().__init__()
        global window, global_lang, lang_name

        window = self
        _preLoad()

        self.appdata = loadAppData()
        self.screen_data = getScreensInfo()

        # Variable initialization
        if len(self.screen_data['screens']) > 0:
            self.last_tag = self.screen_data['screens'][0]['screen_id']

        for screen in self.screen_data['screens']:
            self.actives_screen.append(screen['screen_id'])

        # Data update
        for image_config in self.appdata['images_configs'].values():
            try:
                Image.open(image_config['image_path'])
            except Exception:
                image_config['image_path'] = ""

        for screen in self.screen_data['screens']:
            if screen['screen_id'] not in self.appdata['images_configs']:
                self.appdata['images_configs'].update(
                    {screen['screen_id']: copy.copy(IMAGE_CONFIG)})

        # Config lang
        global_lang = self.appdata['lang']

        for lang in LANG_JSON['langs']:
            if global_lang == lang[1]:
                lang_name = lang[0]

        # Widgets
        self.canvas = ScrollableCanvas(self)
        self.separator1 = ttk.Separator(self, orient="horizontal")
        self.center_frame = CenterFrame(self)
        self.separator2 = ttk.Separator(self, orient="horizontal")
        self.bottom_frame = BottomFrame(self, self.setWallpapers)

        self.canvas.grid(column=0, row=0, sticky="nsew")
        self.separator1.grid(column=0, row=1, sticky="nsew")
        self.center_frame.grid(column=0, row=2, sticky="nsew")
        self.separator2.grid(column=0, row=3, sticky="nsew")
        self.bottom_frame.grid(column=0, row=4, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.bind("<Configure>", self.updateAppData, True)

        self.configWindow()
        self.drawRectangles()

    def configWindow(self):
        self.title("Wallpaper LX")
        self.config(bg=BACKGROUND)

        self.iconphoto(True, app_resources['appicon'])

        try:
            self.geometry(self.appdata['geometry'])

            if self.appdata['state'] == "zoomed":
                self.wm_attributes('-zoomed', True)
            else:
                self.state("normal")

        except Exception as e:
            self.appdata = copy.copy(DEFAULT_APPDATA_JSON)
            self.geometry(self.appdata['geometry'])

    def drawRectangles(self):
        canvas = self.canvas.getCanvas()
        self.images_list.clear()
        canvas.delete("all")

        for screen in self.screen_data['screens']:
            tag = screen['screen_id']

            self._drawRectangle(
                screen, "black", self.appdata['images_configs'][tag],
                fill="#F5F5F5", tag=tag)
            canvas.tag_bind(tag, "<Button-1>", self.getFunction(tag))

        self.pressRectangleEvent(self.last_tag, None)

    def pressRectangleEvent(self, tag: str, e):
        canvas = self.canvas.getCanvas()
        screen_data = None

        for screen in self.screen_data['screens']:
            if screen['screen_id'] == tag:
                screen_data = screen
                canvas.delete(self.focus_highlight_id)
                self.focus_highlight_id = \
                    self._drawRectangle(screen, "blue", None)

                break

        if screen_data:
            self.center_frame.setData(
                screen_data,
                self.appdata['images_configs'][screen_data['screen_id']]
            )

            self.last_tag = tag

    def getFunction(self, tag: str):
        return lambda e: self.pressRectangleEvent(tag, e)

    def updateCanvas(self):
        self.drawRectangles()

    def setWallpapers(self):
        if self.screen_data['total_resolution'] == {}:
            messagebox.showerror(
                getText('error'), getText('internal_error_resolution'))
            return

        wallpaper = Image.new(
            "RGB", (
                self.screen_data['total_resolution']['width'],
                self.screen_data['total_resolution']['height']
            )
        )

        if self.actives_screen == []:
            return

        for screen_id, image_config in self.appdata['images_configs'].items():
            if screen_id not in self.actives_screen:
                continue

            for screen in self.screen_data['screens']:
                if screen_id == screen['screen_id']:
                    break

            if image_config['image_path'] == "":
                messagebox.showerror(
                    getText('error'), getText('not_all_image_selected_error'))
                return

            elif not exists(image_config['image_path']):
                messagebox.showerror(
                    getText('error'),
                    getText('image_not_exists').format(screen_id=screen_id))
                return

            image = createImage(
                (screen['width'], screen['height']), image_config)
            wallpaper.paste(image, (screen['x'], screen['y']))

        wallpaper.save(WALLPAPER_PATH)
        command = getSetWallpaperCommand()

        if command is None:
            messagebox.showerror(
                getText('error'), getText('not_support_set_wallpaper'))
            return

        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror(
                getText('error'), getText('not_wallpaper_set'))

    def saveAppData(self):
        saveAppData(self.appdata)

    def updateAppData(self, e):
        if not self.winfo_ismapped():
            return

        if (self.wm_attributes('-zoomed') == 0) and (self.state() == "normal"):
            self.appdata['state'] = "normal"
            self.appdata['geometry'] = self.geometry()
        elif self.wm_attributes('-zoomed') == 1:
            self.appdata['state'] = "zoomed"

    def destroy(self):
        self.saveAppData()
        super().destroy()

    def _drawRectangle(self, screen: dict, outline: str, image, **args):
        canvas = self.canvas.getCanvas()
        screen = copy.copy(screen)
        tag = screen.pop('screen_id')
        resolution = []

        for value in screen.values():
            value = int(value * REDUCTION_PERCENTAGE)
            if value > 0:
                resolution.append(value)
            else:
                resolution.append(0)

        width, height = resolution[0], resolution[1]

        resolution = (
            resolution[2], resolution[3], resolution[0] + resolution[2],
            resolution[1] + resolution[3]
        )

        if image:
            reduction = \
                True if image['image_mode'] == ImageModes.REPEAT else False
            image = createImage((width, height), image, reduction)

            if image:
                image = ImageTk.PhotoImage(image)
                self.images_list.append(image)

                canvas.create_image(
                    resolution[0], resolution[1], anchor="nw", image=image,
                    tag=tag)

                args.pop('fill')

        return canvas.create_rectangle(resolution, outline=outline, **args)


class CenterFrame(Frame):
    columns = 0
    min_height = 0
    screen_data = None
    image_config = None

    def __init__(self, master):
        super().__init__(master, bg=BACKGROUND)

        self.screen_id = Label(
            self, text="(none)", bg=BACKGROUND, font=BOLD_FONT1)
        self.screen_id.pack(side="top")

        self.image_frame = Frame(self, bg=BACKGROUND)
        self.image = Label(
            self.image_frame, text=getText('image')+':', bg=BACKGROUND,
            anchor="w", font=BOLD_FONT2)
        self.image_path = Entry(
            self.image_frame, state="readonly", bg=BACKGROUND)
        self.select_image = Button(
            self.image_frame, text="...", bg=BACKGROUND,
            command=self.selectImage)
        self.padding = Frame(self.image_frame, bg=BACKGROUND)
        self.mode = Label(
            self.image_frame, text=getText('mode')+':', bg=BACKGROUND,
            anchor="w", font=BOLD_FONT2)
        self.mode_cbbox = ttk.Combobox(
            self.image_frame, state="readonly", background=BACKGROUND)

        self.mode_cbbox['values'] = getText('image_mode')
        self.mode_cbbox.bind("<<ComboboxSelected>>", self.updateImageMode)

        self.image_frame.pack(side="top", fill="x", padx=2, pady=5)
        self.image.grid(column=0, row=0, sticky="nsew")
        self.image_path.grid(column=1, row=0, sticky="nsew")
        self.select_image.grid(column=2, row=0, sticky="nsew")
        self.padding.grid(column=0, columnspan=3, row=1, sticky="nsew", pady=5)
        self.mode.grid(column=0, row=2, sticky="nsew")
        self.mode_cbbox.grid(column=1, columnspan=2, row=2, sticky="nsew")

        self.image_frame.columnconfigure(1, weight=1)

        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.pack(side="top", fill="x")

        self.screen_information_frame = Frame(self, bg=BACKGROUND)
        self.screen_information = Label(
            self.screen_information_frame, text=getText('screen_information'),
            bg=BACKGROUND, font=BOLD_FONT2)
        self.information_frame = Frame(
            self.screen_information_frame, bg=BACKGROUND)
        self.width = Label(
            self.information_frame, text="Width:", anchor="w", bg=BACKGROUND,
            font=BOLD_FONT2)
        self.width_value = Label(
            self.information_frame, text="(none)", anchor="w", bg=BACKGROUND)
        self.height = Label(
            self.information_frame, text="Height:", anchor="w", bg=BACKGROUND,
            font=BOLD_FONT2)
        self.height_value = Label(
            self.information_frame, text="(none)", anchor="w", bg=BACKGROUND)
        self.x = Label(
            self.information_frame, text="x:", anchor="w", bg=BACKGROUND,
            font=BOLD_FONT2)
        self.x_value = Label(
            self.information_frame, text="(none)", anchor="w", bg=BACKGROUND)
        self.y = Label(
            self.information_frame, text="y:", anchor="w", bg=BACKGROUND,
            font=BOLD_FONT2)
        self.y_value = Label(
            self.information_frame, text="(none)", anchor="w", bg=BACKGROUND)

        self.screen_information_frame.pack(
            side="top", fill="both", expand=True, padx=2, pady=5)
        self.screen_information.pack(side="top")
        self.information_frame.pack(side="top", fill="both", expand=True)

        self.screen_information_frame.bind(
            "<Configure>", self.adjustScreenInformation)

    def adjustScreenInformation(self, e):
        if (e.height > self.min_height) and (self.columns == 1):
            return

        self.columns = 1
        self.min_height = 0

        columns_aux = 0
        height = 0
        row = 0
        field, value = None, None

        for children in self.information_frame.winfo_children():
            if not field:
                field = children
                continue
            else:
                value = children

            if (height + field.winfo_height() + 20) > e.height:
                self.columns += 1

                if self.min_height == 0:
                    self.min_height = height

                columns_aux += 2
                row = 0
                height = 0

            field.grid(
                column=columns_aux, row=row, sticky="nsew", padx=5, pady=5)
            children.grid(
                column=columns_aux+1, row=row, sticky="nsew", padx=5, pady=5)

            height += field.winfo_reqheight() + 20
            field, value = None, None
            row += 1

        if self.min_height == 0:
            self.min_height = height

    def setData(self, screen_data: dict, image_config: dict):
        self.screen_data = screen_data
        self.image_config = image_config
        self.updateData()

    def updateData(self):
        if not self.screen_data or not self.image_config:
            return

        self.screen_id['text'] = self.screen_data['screen_id']

        self.image_path['state'] = "normal"
        self.image_path.delete(0, "end")
        self.image_path.insert(0, self.image_config['image_path'])
        self.image_path['state'] = "readonly"

        self.mode_cbbox.current(self.image_config['image_mode'])
        self.width_value['text'] = self.screen_data['width']
        self.height_value['text'] = self.screen_data['height']
        self.x_value['text'] = self.screen_data['x']
        self.y_value['text'] = self.screen_data['y']

    def selectImage(self):
        if self.image_config is None:
            return

        if self.image_config['image_path'] == "":
            initialdir = f"/home/{getlogin()}"
        else:
            initialdir = dirname(abspath(self.image_config['image_path']))

        image = filedialog.askopenfilename(
            title=getText('select_image'), initialdir=initialdir)

        if not image:
            return

        try:
            Image.open(image)

            if self.image_config:
                self.image_config['image_path'] = image
                self.updateData()

                window.updateCanvas()
                window.saveAppData()

        except Exception:
            messagebox.showerror(
                getText('error'), getText('open_image_error_message'))

    def updateImageMode(self, e):
        if self.image_config:
            if self.image_config['image_mode'] == self.mode_cbbox.current():
                return

            self.image_config['image_mode'] = self.mode_cbbox.current()

            window.updateCanvas()
            window.saveAppData()


class BottomFrame(Frame):
    def __init__(self, master, set_wallpapers_function):
        super().__init__(master, bg=BACKGROUND)

        # Widget
        self.settings = Button(
            self, text="", image=app_resources['settings-icon'], relief="flat",
            bg=BACKGROUND)
        self.set_wallpapers = Button(
            self, text=getText('set_wallpapers'), bg=BACKGROUND,
            command=set_wallpapers_function)

        self.settings.pack(side="left")
        self.set_wallpapers.pack(side="right")

        # Dialog
        self.settings_widget = SettingsWidget()
        self.settings['command'] = self.settings_widget.showSettings


class ScrollableCanvas(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.y_scroll = Scrollbar(self)
        self.x_scroll = Scrollbar(self, orient="horizontal")
        self.canvas = Canvas(
            self, yscrollcommand=self.y_scroll.set,
            xscrollcommand=self.x_scroll.set,
            scrollregion=(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))
        self.container = Canvas(
            self.canvas, bg=BACKGROUND, width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT)

        self.canvas.create_window(
            (0, 0), window=self.container, anchor="nw")

        self.y_scroll.config(command=self.canvas.yview)
        self.x_scroll.config(command=self.canvas.xview)

        self.y_scroll.pack(side="right", fill="y")
        self.x_scroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

    def getCanvas(self):
        return self.container


class SettingsWidget(Frame):
    def __init__(self):
        super().__init__(window, bg=BACKGROUND, relief="solid", bd=2)

        # Widgets
        self.app_widget = Frame(self, bg=BACKGROUND)
        self.app_logo = Label(
            self.app_widget, image=app_resources['appicon-no-bg'],
            bg=BACKGROUND)
        self.app_text = Label(
            self.app_widget, bg=BACKGROUND,
            text=(
                "Wallpaper LX\n"
                f"Version: {__version__}\n"
                "Copyright © 2023 FrankC64"
            ), justify="left"
        )

        self.app_widget.pack(side="top", fill="x", pady=1)
        self.app_logo.pack(side="left", padx=10, fill="y")
        self.app_text.pack(side="left", anchor="n", pady=5)

        ttk.Separator(self, orient="horizontal").pack(
            side="top", fill="x", pady=10)

        self.lang_widget = Frame(self, bg=BACKGROUND)
        self.lang = Label(
            self.lang_widget, text=getText('lang')+":", bg=BACKGROUND)
        self.langs_cbbox = ttk.Combobox(
            self.lang_widget, state="readonly", background=BACKGROUND,
            width=8)

        self.lang_widget.pack(side="top", fill="x", padx=10)
        self.lang.pack(side="top", anchor="w")
        self.langs_cbbox.pack(side="top", anchor="w")

        self.close = Button(
            self, text=getText('close'), bg=BACKGROUND,
            command=self.closeDialog)

        self.close.pack(side="bottom", anchor="e", padx=1, pady=1)
        ttk.Separator(self, orient="horizontal").pack(side="bottom", fill="x")

        # Configs
        self.langs_cbbox['values'] = \
            tuple(lang[0] for lang in LANG_JSON['langs'])
        self.langs_cbbox.bind("<<ComboboxSelected>>", self.updateLang)
        self.langs_cbbox.set(lang_name)

        self.pack_propagate(0)
        window.bind("<Configure>", self.updatePos, True)

    def updateLang(self, e):
        global restart_app
        lang_id = ""

        for lang in LANG_JSON['langs']:
            if self.langs_cbbox.get() == lang[0]:
                lang_id = lang[1]

        if lang_id != global_lang:
            window.appdata['lang'] = lang_id
            window.saveAppData()

            result = messagebox.askyesno(
                getText('check_restart'), getText('check_restart_message'))

            if result:
                restart_app = True
                window.destroy()

    def showSettings(self):
        self._update_pos()
        self.grab_set()

    def closeDialog(self):
        self.grab_release()
        self.place_forget()

    def updatePos(self, e):
        if self.winfo_ismapped():
            self._update_pos()

    def _update_pos(self):
        width = int(window.winfo_width() * 0.90)
        width = width if width > 0 else 1

        height = int(window.winfo_height() * 0.90)
        height = height if height > 0 else 1

        x = window.winfo_width() // 2 - width // 2
        x = x if x >= 0 else 0

        y = window.winfo_height() // 2 - height // 2
        y = y if y >= 0 else 0

        self.place(x=x, y=y)
        self.config(width=width, height=height)


def getText(text_id: str):
    return LANG_JSON[global_lang][text_id]


def loadAppData():
    data = {}

    def dataWithLang():
        data = copy.copy(DEFAULT_APPDATA_JSON)

        if locale.getlocale()[0][0:2] in LANG_JSON:
            data['lang'] = locale.getlocale()[0][0:2]

        return data

    if not exists(CONFIG_PATH):
        makedirs(CONFIG_PATH)
        data = dataWithLang()

    else:
        try:
            with open(APP_DATA_PATH, "r") as f:
                data = json.load(f)
        except Exception:
            return dataWithLang()

        if len(data) != len(DEFAULT_APPDATA_JSON):
            data = copy.copy(DEFAULT_APPDATA_JSON)
            if locale.getlocale()[0:2] in LANG_JSON:
                data['lang'] = locale.getlocale()[0][0:2]

        else:
            if 'geometry' in data:
                width = data['geometry'][0:data['geometry'].find("x")]
                height = data['geometry'][data['geometry'].find("x")+1:data['geometry'].find("+")]

                try:
                    width = int(width)
                    height = int(height)

                    if (width <= 50) or (height <= 50):
                        data['geometry'] = DEFAULT_APPDATA_JSON['geometry']
                except ValueError:
                    return dataWithLang()

            for key, value in data.items():
                if key == 'images_configs':
                    for value in value.values():
                        if ('image_path' not in value) \
                                or ('image_mode' not in value):
                            return dataWithLang()
                        elif (type(value['image_path']) != str) \
                                or (type(value['image_mode']) != int):
                            return dataWithLang()
                elif key not in DEFAULT_APPDATA_JSON:
                    return dataWithLang()
                elif type(value) != str:
                    return dataWithLang()

    return data


def saveAppData(data: dict):
    if not exists(CONFIG_PATH):
        makedirs(CONFIG_PATH)

    with open(APP_DATA_PATH, "w") as f:
        json.dump(data, f)


def _preLoad():
    global LANG_JSON

    with open(LANG_JSON_PATH, "r") as f:
        LANG_JSON = json.load(f)

    appicon_no_bg = Image.open(join(APP_RESOURCES_PATH, "appicon.png"))
    appicon = appicon_no_bg.convert("RGB")
    appicon_no_bg = appicon_no_bg.resize((64, 64))

    appicon = ImageTk.PhotoImage(appicon)
    appicon_no_bg = ImageTk.PhotoImage(appicon_no_bg)
    app_resources['appicon-no-bg'] = appicon_no_bg
    app_resources['appicon'] = appicon

    settings_icon = Image.open(
        join(APP_RESOURCES_PATH, "interface", "settings.png"))
    settings_icon = ImageTk.PhotoImage(settings_icon)
    app_resources['settings-icon'] = settings_icon

    about_icon = Image.open(
        join(APP_RESOURCES_PATH, "interface", "about.png"))
    about_icon = ImageTk.PhotoImage(about_icon)
    app_resources['about-icon'] = about_icon


def main():
    global restart_app

    while restart_app:
        restart_app = False
        App().mainloop()
