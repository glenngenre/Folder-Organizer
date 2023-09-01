### This file contains functions to load the config file and get values from it ###

import yaml
import os


def load_config() -> dict:
    if not os.path.exists("config.yaml"):
        create_default_config()

    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError:
        print("config.yaml corrupted. Creating a default config.yaml file.")
        create_default_config(error=True)
        return load_config()
    return config


def create_default_config(error: bool = False) -> None:
    if not error and os.path.exists("config.yaml"):
        print("config.yaml file already exists.")
        return
    if error and os.path.exists("config.yaml"):
        os.remove("config.yaml")

    with open("config.yaml", mode="w+") as f:
        f.write(
            f"""# This is the configuration file for the program

# The log file path relative to the program
LogFileName: "log.txt"

# Should empty folders created by the program be deleted?
DeleteEmptyFolders: true

# Should the program delete files that are not modified for a certain amount of time?
DeleteOldFiles: false

# If DeleteOldFiles is true, then the program will delete files that are not modified for this amount of time
# The format is: [number][unit]
# Units: s, m, h, d, w, M, y
# Example: 1d = 1 day
DeleteOldFilesTime: 1y

# File types and their extensions
FileTypes:
  Documents:
    - .pdf
    - .docx
    - .txt
    - .doc
    - .pptx
    - .ppt
    - .xlsx
    - .xls
    - .csv
    - .rtf
  Images:
    - .jpg
    - .jpeg
    - .png
    - .gif
    - .bmp
    - .svg
    - .ico
    - .psd
    - .ai
    - .raw
    - .tiff
    - .tif
    - .jfif
    - .webp
  Audio:
    - .mp3
    - .wav
    - .ogg
    - .m4a
    - .flac
    - .aac
    - .opus
  Video:
    - .mp4
    - .mov
    - .avi
    - .flv
    - .mkv
    - .webm
    - .wmv
    - .m4v
  Compressed:
    - .zip
    - .rar
    - .tar
    - .gz
    - .7z
    - .xz
    - .bz2
    - .lzma
    - .z
    - .lz
  Code:
    - .py
    - .js
    - .html
    - .css
    - .c
    - .cpp
    - .java
    - .json
    - .xml
    - .db
    - .yaml
    - .yml
    - .sql
    - .log
    - .md
    - .gd
  Font:
    - .ttf
    - .otf
  Executables and Installers:
    - .exe
    - .msi
    - .apk
    - .bat
    - .sh
    - .deb
  Shortcuts:
    - .lnk
    - .url
  Torrent:
    - .torrent
  OSU!:
    - .osz
  WEB:
    - .crdownload
    - .part
    - .htm
  Minecraft:
    - .mcworld
    - .mcpack
    - .mcaddon
    - .schem
    - .mctemplate
    - .schematic   
                """
        )


def get_dict(config, key) -> dict:
    if not isinstance(config[key], dict):
        raise TypeError(
            f"Expected {key} to be a dictionary, but got {type(config[key])}"
        )
    return config[key]


def get_list(config, key) -> list:
    if not isinstance(config[key], list):
        raise TypeError(f"Expected {key} to be a list, but got {type(config[key])}")
    return config[key]


def get_str(config, key) -> str:
    if not isinstance(config[key], str):
        raise TypeError(f"Expected {key} to be a string, but got {type(config[key])}")
    return config[key]


def get_int(config, key) -> int:
    if not isinstance(config[key], int):
        raise TypeError(f"Expected {key} to be an integer, but got {type(config[key])}")
    return config[key]


def get_bool(config, key) -> bool:
    if not isinstance(config[key], bool):
        raise TypeError(f"Expected {key} to be a boolean, but got {type(config[key])}")
    return config[key]


def get_float(config, key) -> float:
    if not isinstance(config[key], float):
        raise TypeError(f"Expected {key} to be a float, but got {type(config[key])}")
    return config[key]


def get_time(config, key) -> int:
    if not isinstance(config[key], str):
        raise TypeError(f"Expected {key} to be a string, but got {type(config[key])}")
    time = config[key]
    time_dict = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800,
        "M": 2629800,
        "y": 31557600,
    }
    unit = time[-1]
    if unit not in time_dict:
        raise ValueError(f"Invalid unit: {unit}")
    time = time[:-1]
    if not time.isdigit():
        raise ValueError(f"Invalid time: {time}")
    return int(time) * time_dict[unit]
