import os
import datetime
import json


class File:
    def __init__(self, path):
        self.path = path

    @property
    def name(self):
        return os.path.basename(self.path)

    @property
    def last_modified(self):
        timestamp = os.path.getmtime(self.path)
        return datetime.datetime.fromtimestamp(timestamp)

    @last_modified.setter
    def last_modified(self, value):
        self.last_modified = value

    @property
    def created(self) -> datetime.datetime:
        timestamp = os.path.getctime(self.path)
        return datetime.datetime.fromtimestamp(timestamp)

    @created.setter
    def created(self, value):
        self.created = value

    @property
    def size(self) -> int:
        return os.path.getsize(self.path)

    @size.setter
    def size(self, value):
        self.size = value

    @property
    def extension(self) -> str:
        return os.path.splitext(self.path)[1]

    @extension.setter
    def extension(self, value):
        self.extension = value

    def serialize(self):
        data = {
            "path": self.path,
            "name": self.name,
            "last_modified": self.last_modified.timestamp(),
            "created": self.created.timestamp(),
            "size": self.size,
            "extension": self.extension,
        }
        return json.dumps(data)

    @classmethod
    def deserialize(cls, data):
        data = json.loads(data)
        file = cls(data["path"])
        file.last_modified = datetime.datetime.fromtimestamp(data["last_modified"])
        file.created = datetime.datetime.fromtimestamp(data["created"])
        file.size = data["size"]
        file.extension = data["extension"]
        return file
