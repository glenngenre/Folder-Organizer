### This contains the main logic of the program. You can run this as a console program. ###

import os
import shutil
import datetime

from config_utils import *
from File import File
from FileManager import FileManager

config = load_config()
files = []
folders = []


def create_log_file() -> None:
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


def get_folders(folder_path: str) -> list[File]:
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isdir(file_path):
            folders.append(File(path=file_path))
    return folders


def organize_folder(folder_path: str):
    files: list[File] = get_files(folder_path)
    config = load_config()

    # Write the path of the folder to the log file
    write_to_log(f"Folder path to be organized: {folder_path}")

    for file in (f for f in files if not f.name.startswith(".") and not f.is_folder()):
        subfolder_path = os.path.join(folder_path, get_file_type(file))
        if get_file_type(file) == "None":
            continue

        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        move_files(file, subfolder_path)
        delete_old_files(file)
    delete_empty_folders(folder_path)

    write_to_log(
        f"""
--- Organizing complete! ---
Files moved: {files_moved}
Files deleted: {files_deleted}
Files renamed: {files_renamed}
Megabytes moved: {megabytes_moved}
----------------------------"""
    )


def move_files(file: File, folder_path: str):
    global files_moved, files_deleted, files_renamed, megabytes_moved
    files_moved = 0
    files_renamed = 0
    megabytes_moved = 0

    try:
        FileManager(file).move(folder_path)
    except shutil.Error:
        new_name: str = rename_file(file.name, os.listdir(folder_path))
        write_to_log(f"File already exists: {file.name}, renaming to {new_name}")
        FileManager(file).rename(new_name).move(folder_path)
        files_renamed += 1
    files_moved += 1
    megabytes_moved += file.size / 1000000
    write_to_log(f"Moved: {file.name} to {folder_path}")


def delete_old_files(file: File):
    global files_deleted
    files_deleted = 0

    if get_bool(config, "DeleteOldFiles"):
        time_difference = datetime.datetime.now().timestamp() - os.path.getmtime(
            file.path
        )
        if time_difference < get_time(config, "DeleteOldFilesTime"):
            return

        try:
            FileManager(file).send_to_trash()
        except OSError:
            print(f"Couldn't delete: {file.name}")
            write_to_log(f"Couldn't delete: {file.name}")
        files_deleted += 1
        write_to_log(f"Deleted: {file.name}")


def delete_empty_folders(folder_path: str):
    delete_empty_folders = get_bool(config, "DeleteEmptyFolders")
    delete_empty_folders_not_created = get_bool(config, "DeleteEmptyFoldersNotCreated")

    if not delete_empty_folders or not delete_empty_folders_not_created:
        return

    file_types = get_dict(config, "FileTypes")

    for file_type in file_types:
        subfolder_path = os.path.join(folder_path, file_type)
        if os.path.exists(subfolder_path) and not os.listdir(subfolder_path):
            try:
                os.rmdir(subfolder_path)
                write_to_log(f"Deleted: {subfolder_path}")
            except OSError:
                print(f"Couldn't delete: {subfolder_path}")
                write_to_log(f"Couldn't delete: {subfolder_path}")

    for folder in get_folders(folder_path):
        if not os.listdir(folder.path):
            try:
                os.rmdir(folder.path)
                write_to_log(f"Deleted: {folder.path}")
            except OSError:
                print(f"Couldn't delete: {folder.path}")
                write_to_log(f"Couldn't delete: {folder.path}")


def rename_file(file: str, file_list: list) -> str:
    file_name = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]

    # If the file already exists, add a number to the end of the file name
    n = 1
    while f"{file_name} ({n}){extension}" in file_list:
        # increment n until the file name doesn't exist in the folder
        n += 1

    # return the new file name
    return f"{file_name} ({n}){extension}"


def get_file_type(file: File) -> str:
    config = load_config()
    file_types = get_dict(config, "FileTypes")

    for file_type, extensions in file_types.items():
        if file.extension in extensions:
            return file_type

    return "None"


if __name__ == "__main__":
    folder_path = input("Enter the path of the folder you want to organize: ")
    organize_folder(folder_path)
    print(f"{folder_path} has been organized!")
