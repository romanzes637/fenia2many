from .base import BaseObject
import numpy as np
import os


class Field(BaseObject):
    def __init__(self, path, mode=1):
        BaseObject.__init__(self, path)
        self.name = os.path.basename(self.path)
        self.data = np.empty([0])
        self.mode = mode
        self.element_size = 0
        self.n_elements = 0
        self.dictionary = {}

    def read(self):
        if self.mode == 0:
            data = self.read_data()
            field_index = data.index('internalField')
            # print data[:field_index]
            keys = []
            values = []
            for i, d in enumerate(data[:field_index]):
                if i % 2 == 0:
                    keys.append(d)
                else:
                    values.append(d)
            for i, key in enumerate(keys):
                self.dictionary.update({key: values[i]})
            if data[field_index + 1] == 'uniform':
                self.n_elements = 1
                start_index = field_index + 2
            else:
                self.n_elements = int(data[field_index + 3])
                start_index = field_index + 4
            self.element_size = int(len(data[start_index:]) / self.n_elements)
            self.data = np.reshape(data[start_index:], [self.n_elements, self.element_size])
        else:
            data = self.read_data()
            field_index = data.index('internalField')
            # print data[:field_index]
            keys = []
            values = []
            for i, d in enumerate(data[:field_index]):
                if i % 2 == 0:
                    keys.append(d)
                else:
                    values.append(d)
            for i, key in enumerate(keys):
                self.dictionary.update({key: values[i]})
            if data[field_index + 1] == 'uniform':
                self.n_elements = 1
                start_index = field_index + 2
            else:
                self.n_elements = int(data[field_index + 3])
                start_index = field_index + 4
            self.element_size = int(len(data[start_index:]) / self.n_elements)
            self.data = np.ascontiguousarray(data[start_index:], dtype=float)
