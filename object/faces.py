import os
import numpy as np
import logging
import time

from .base import BaseObject


class Faces(BaseObject):
    """FENIA faces representation

    TODO:
        write mode == 0, 2
    """

    def __init__(self, path, is_2d=False, mode=1, order=1):
        BaseObject.__init__(self, path)
        self.name = os.path.basename(self.path)
        self.is_2d = is_2d
        self.mode = mode
        self.order = order
        self.lines = np.empty([0, 2 + 1], int)
        self.lines_ids = np.empty([0], int)
        self.triangles = np.empty([0, 3 + 1], int)
        self.triangles_ids = np.empty([0], int)
        self.quads = np.empty([0, 4 + 1], int)
        self.quads_ids = np.empty([0], int)
        self.n_faces = 0
        self.data = np.empty([0])

    def read(self):
        logging.info('Reading faces')
        t00 = time.perf_counter()
        if self.mode == 0:
            data = self.read_data()
            self.n_faces = int(data[0])
            start_index = 1
            face_id = 0
            face = np.empty([0], int)
            point_ctr = 0
            is_point = False
            for d in data[start_index:]:
                if not is_point:
                    n_points = int(d)
                    point_ctr = 0
                    face = np.empty([0], int)
                    face = np.append(face, [n_points], 0)
                    is_point = True
                else:
                    face = np.append(face, [int(d)], 0)
                    point_ctr += 1
                    if point_ctr == n_points:
                        is_point = False
                        if not self.is_2d:
                            if n_points == 3:
                                self.triangles = np.append(self.triangles, [face], 0)
                                self.triangles_ids = np.append(self.triangles_ids, [face_id], 0)
                                face_id += 1
                                continue
                            elif n_points == 4:
                                self.quads = np.append(self.quads, [face], 0)
                                self.quads_ids = np.append(self.quads_ids, [face_id], 0)
                                face_id += 1
                                continue
                        else:
                            if n_points == 2:
                                self.lines = np.append(self.lines, [face], 0)
                                self.lines_ids = np.append(self.lines_ids, [face_id], 0)
                                face_id += 1
                                continue
        else:
            data = self.read_data()
            self.n_faces, self.data = int(data[0]), np.array(data[1:], dtype=int)
        logging.debug(f'faces: {self.n_faces}, len(data): {len(self.data)}, '
                      f'data: {self.data}')
        logging.info(f'Reading faces total: {time.perf_counter() - t00}s')

    def write(self):
        if self.mode == 1:
            with open(self.path, 'w') as f:
                f.write(self.header(cls='faceList'))
                f.write('{}\n'.format(self.n_faces))
                f.write('(\n')
                i = 0
                while i != len(self.data):
                    n_points = self.data[i]
                    cell = '{}('.format(n_points)
                    points = ' '.join(map(str, self.data[i + 1:i + 1 + n_points]))
                    cell += points
                    cell += ')\n'
                    f.write(cell)
                    i += n_points + 1
                f.write(')\n')
                f.write(self.footer())
