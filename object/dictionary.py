from .base import BaseObject
import os


class Dictionary(BaseObject):
    def __init__(self, path):
        BaseObject.__init__(self, path)
        self.name = os.path.basename(self.path)
        self.data = {}

    def read(self):
        data = self.read_data(clear_data=False)
        start_index = 0
        keys = []
        values = []
        for i, d in enumerate(data[start_index:]):
            if i % 2 == 0:
                keys.append(d)
            else:
                values.append(d)
        for i, key in enumerate(keys):
            try:
                self.data.update({key: values[i]})
            except ValueError as e:
                print(e)
