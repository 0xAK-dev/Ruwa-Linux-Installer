# Ruwa Linux Installer

A simple **Arch Linux installer** for [Ruwa](https://github.com/LuskusDeus/Ruwa).

> **Note:** The installer currently supports **Arch Linux only**.

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

Currently, **Arch Linux is the only supported distribution**.

Install the dependencies with:

```bash
sudo pacman -S base-devel cmake ninja git qt6-base qt6-tools qt6-declarative qt6-svg
```

## Installation

```bash
git clone https://github.com/0xAK-dev/Ruwa-Linux-Installer.git
cd Ruwa-Linux-Installer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python installer_window.py
```