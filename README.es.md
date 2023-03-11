# Wallpaper LX
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/FrankC64/Wallpaper-LX/blob/main/README.md)

Wallpaper LX es una app de código abierto que te ayuda a establecer el fondo de pantalla en una o más pantallas de forma rápida y fácil.

[![license](https://img.shields.io/badge/license-GPL-blue.svg)]()
[![release](https://img.shields.io/badge/release-v1.0-blue.svg)]()

Distribuciones compatibles: Lubuntu.

---

## Instalar
**1. Paquetes necesarios**<br>
Para que la app funcione se deben instalar varios paquetes. Escriba los siguientes comandos en su terminal:

```bash
sudo apt-get update
sudo apt-get install python3-venv python3-tk python3-pil.imagetk git
```

**2. Clonar el repositorio**<br>
Escriba los siguientes comandos en su terminal:

```bash
mkdir ~/apps
cd ~/apps
git clone https://github.com/FrankC64/Wallpaper-LX.git
cd Wallpaper-LX
```

**3. Instalar**<br>
Escriba los siguientes comandos en su terminal:

```bash
chmod +x install
sudo ./install
```

## Desinstalar
Para desinstalar la app solo debe ejecutar los siguientes comandos desde la raíz del repositorio clonado. 

```bash
chmod +x uninstall
sudo ./uninstall
```

## ¿Cómo uso la app sin instalarla?
Para utilizarlo de esta manera siga los pasos uno y dos de la instalación y en la raíz del repositorio clonado ejecute el siguiente comando:

```bash
chmod +x Wallpaper-LX
```

Y para ejecutarlo use el siguiente comando:

```bash
./Wallpaper-LX
```

| :warning: ADVERTENCIA |
|:-----------------------------------------|
| En caso de que vayas a dejar de utilizar la app definitivamente, deberás seguir los pasos de desinstalación de la misma manera para eliminar los archivos residuales. |

## Capturas de pantalla
<img src="https://raw.githubusercontent.com/FrankC64/Wallpaper-LX/master/screenshots/one-screen.jpg">
<img src="https://raw.githubusercontent.com/FrankC64/Wallpaper-LX/master/screenshots/two-screen.jpg">
<img src="https://raw.githubusercontent.com/FrankC64/Wallpaper-LX/master/screenshots/two-screen-one-image.jpg">
<img src="https://raw.githubusercontent.com/FrankC64/Wallpaper-LX/master/screenshots/two-screen-two-image.jpg">
<img src="https://raw.githubusercontent.com/FrankC64/Wallpaper-LX/master/screenshots/two-screen-wallpaper.jpg">
