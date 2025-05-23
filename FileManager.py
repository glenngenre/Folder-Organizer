import os
import shutil
from send2trash import send2trash
from File import File


class FileManager:
    def __init__(self, file: File):
        self.file = file

    def rename(self, new_name):
        new_path = os.path.join(os.path.dirname(self.file.path), new_name)
        self.file.name = new_name
        os.rename(self.file.path, new_path)
        self.file.path = new_path

        return self

    def send_to_trash(self):
        send2trash(self.file.path)

    def move(self, destination):
        shutil.move(self.file.path, destination)
        self.file.path = os.path.join(destination, os.path.basename(self.file.path))
