import numpy as np
import os
from pathlib import Path
import logging
import time

from .base import BaseObject


class Points(BaseObject):
    """FENIA points representation

    TODO:
        write mode == 0
    """

    def __init__(self, path, is_2d=False, mode=1, order=1):
        BaseObject.__init__(self, path)
        self.name = os.path.basename(self.path)
        self.is_2d = is_2d
        self.mode = mode
        self.order = order
        self.data = np.empty([0])
        self.n_points = 0

    def read(self):
        logging.info('Reading points')
        t00 = time.perf_counter()
        if self.mode == 0:
            data = self.read_data()
            self.n_points = int(data[0])
            start_index = 1
            points_size = len(data[start_index:]) / self.n_points
            self.data = np.reshape(map(float, data[start_index:]), [self.n_points, points_size])
        elif self.mode == 1:
            data = self.read_data()
            self.n_points = int(data[0])
            start_index = 1
            self.data = np.ascontiguousarray(data[start_index:], dtype=float)
        else:
            path = Path(self.path)
            points_path = path.parent / 'points'
            points = BaseObject(path=points_path)
            data = points.read_data()
            self.n_points = int(data[0])
            start_index = 1
            self.data = np.ascontiguousarray(data[start_index:], dtype=float)
        logging.debug(f'points: {self.n_points}, len(data): {len(self.data)}, '
                      f'data: {self.data}')
        logging.info(f'Reading points total: {time.perf_counter() - t00}s')

    def write(self):
        if self.mode == 1:
            with open(self.path, 'w') as f:
                f.write(self.header(cls='vector2DField'))
                f.write('{}\n'.format(self.n_points))
                f.write('(\n')
                for i in range(len(self.data)):
                    if i % 3 == 0 and i != 0:
                        f.write('({} {} {})\n'.format(
                            self.data[i - 3], self.data[i - 2], self.data[i - 1]))
                f.write(')\n')
                f.write(self.footer())
