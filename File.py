import os

from datetime import datetime
from dataclasses import dataclass


@dataclass(order=True)
class File:
    path: str = ""
    name: str = ""
    last_modified: datetime = datetime.fromtimestamp(0)
    created: datetime = datetime.fromtimestamp(0)
    size: int = 0
    extension: str = ""

    def __post_init__(self):
        self.name = os.path.basename(self.path)
        self.last_modified = datetime.fromtimestamp(os.path.getmtime(self.path))
        self.created = datetime.fromtimestamp(os.path.getctime(self.path))
        self.size = os.path.getsize(self.path)
        self.extension = os.path.splitext(self.path)[1]

    def is_folder(self) -> bool:
        return os.path.isdir(self.path)
