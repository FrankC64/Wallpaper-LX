# Wallpaper LX
[![es](https://img.shields.io/badge/lang-es-green.svg)](https://github.com/FrankC64/Wallpaper-LX/blob/main/README.es.md)

Wallpaper LX is an open source app that helps you set the wallpaper on one or more screens quickly and easily.

[![license](https://img.shields.io/badge/license-GPL-blue.svg)]()
[![release](https://img.shields.io/badge/release-v1.0-blue.svg)]()

Compatible desktop environments: LXQT y GNOME.

---

## Install
**1. Necessary packages**<br>
Several packages must be installed for the app to work. Type the following commands in your terminal:

### Lubuntu (LXQT)
```bash
sudo apt-get update
sudo apt-get install python3-venv python3-tk python3-pil.imagetk git xrandr xdpyinfo
```

### Fedora (GNOME)
```bash
dnf check-update
sudo dnf install python3-virtualenv python3-tkinter python3-imaging-tk git xrandr xdpyinfo
```

**2. Clone the repository**<br>
Type the following commands in your terminal:

```bash
mkdir ~/apps
cd ~/apps
git clone https://github.com/FrankC64/Wallpaper-LX.git
cd Wallpaper-LX
```

**3. Install**<br>
Type the following commands in your terminal:

```bash
chmod +x install
sudo ./install
```

## Uninstall
To uninstall the app just run the following commands from the root of the cloned repository.

```bash
chmod +x uninstall
sudo ./uninstall
```

## How do I use the app without installing it?
To use it this way follow steps one and two of the installation and in the root of the cloned repository run the following command:

```bash
chmod +x Wallpaper-LX
```

And to execute it use the following command:

```bash
./Wallpaper-LX
```

| :warning: WARNING |
|:-----------------------------------------|
| In case you are going to stop using the app for good, you should follow the uninstallation steps in the same way to remove residual files. |

## Screenshots
<img src="https://raw.githubusercontent.com/FrankC64/Wallpaper-LX/master/screenshots/one-screen.jpg">
<img src="https://raw.githubusercontent.com/FrankC64/Wallpaper-LX/master/screenshots/two-screen.jpg">
<img src="https://raw.githubusercontent.com/FrankC64/Wallpaper-LX/master/screenshots/two-screen-one-image.jpg">
<img src="https://raw.githubusercontent.com/FrankC64/Wallpaper-LX/master/screenshots/two-screen-two-image.jpg">
<img src="https://raw.githubusercontent.com/FrankC64/Wallpaper-LX/master/screenshots/two-screen-wallpaper.jpg">
