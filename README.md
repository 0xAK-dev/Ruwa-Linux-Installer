# Ruwa Linux Installer

A simple **Linux installer** for [Ruwa](https://github.com/LuskusDeus/Ruwa).

The installer downloads **Ruwa 0.3.0**, builds the project, installs the required application files and creates a desktop entry.


![Ruwa Linux Installer](assets/preview.png)

## Features

- Install Ruwa 0.3.0
- Select a custom installation directory
- Automatically clone the required Git tag
- Build Ruwa from source
- Install application binaries and resources
- Install shared libraries
- Install shaders, effects and plugins
- Create a `.desktop` launcher
- Configure environment variables
- Support for custom installation paths

## Requirements
Install the dependencies:

### Arch Linux

```bash
sudo pacman -S python base-devel cmake ninja git qt6-base qt6-tools qt6-declarative qt6-svg
```

### Ubuntu

```bash
sudo apt install python3 python3-venv build-essential cmake ninja-build \
    git qt6-base-dev qt6-tools-dev qt6-declarative-dev libqt6svg6-dev
```
### Fedora
```bash
sudo dnf install python3 python3-devel cmake ninja-build git gcc gcc-c++ make \
    qt6-qtbase-devel qt6-qttools-devel qt6-qtdeclarative-devel qt6-qtsvg-devel
```


## Installation

```bash
git clone https://github.com/0xAK-dev/Ruwa-Linux-Installer.git
cd Ruwa-Linux-Installer
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python installer_window.py
```