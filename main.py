### This contains the main logic of the program. You can run this as a console program. ###

import os
import shutil
import datetime

from config_utils import *
from send2trash import send2trash
from File import File

config = {}
files = []


def create_log_file() -> None:
    # Create a log file if it doesn't exist in the same directory as the script

    # get log file path
    log_file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        get_str(load_config(), "LogFileName"),
    )

    if not os.path.exists(log_file_path):
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write(
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} >> Log file created\n"
            )
            f.close()


def write_to_log(str: str):
    # Write to the log file
    log_file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        get_str(load_config(), "LogFileName"),
    )

    if not os.path.exists(log_file_path):
        create_log_file()

    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} >> {str}\n")
        f.close()


def get_files(folder_path: str):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file = File(file_path)
            files.append(file)

    return files


def organize_files(folder_path: str):
    config = load_config()

    files = get_files(folder_path)

    # Write the path of the folder to the log file
    write_to_log(f"Folder path to be organized: {folder_path}")

    # Identify file types
    file_types = get_dict(config, "FileTypes")

    for file in files:
        if file.name.startswith("."):
            continue

        if file.extension.lower() in file_types


def organize_folder(folder_path: str):
    """
    Organizes a folder by moving files into subfolders based on their file type.
    It also creates a log file in the same directory as the script to keep track of the files that were moved.
    """

    config = load_config()

    # Write the path of the folder to the log file
    write_to_log(f"Folder path to be organized: {folder_path}")

    # Identify file types
    file_types = get_dict(config, "FileTypes")

    # Organize files
    for file_type, extensions in file_types.items():
        subfolder_path = os.path.join(folder_path, file_type)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        for file_name in (
            f
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and not f.startswith(".")
        ):
            file_path = os.path.join(folder_path, file_name)

            if get_bool(config, "DeleteOldFiles"):
                time_difference = (
                    datetime.datetime.now().timestamp() - os.path.getmtime(file_path)
                )
                if time_difference > get_time(config, "DeleteOldFilesTime"):
                    try:
                        send2trash(file_path)
                    except OSError:
                        print(f"Couldn't delete: {file_name}")
                    write_to_log(f"Deleted: {file_name}")
                    continue

            if any(file_name.endswith(ext) for ext in extensions):
                try:
                    shutil.move(file_path, subfolder_path)
                except shutil.Error:
                    print(f"File already exists: {file_name}")
                write_to_log(f"Moved: {file_name} to {subfolder_path}")

    if get_bool(config, "DeleteEmptyFolders"):
        for file_type in file_types:
            subfolder_path = os.path.join(folder_path, file_type)
            if os.path.exists(subfolder_path) and not os.listdir(subfolder_path):
                os.rmdir(subfolder_path)


if __name__ == "__main__":
    folder_path = input("Enter the path of the folder you want to organize: ")
    organize_folder(folder_path)
    print(f"{folder_path} has been organized!")
