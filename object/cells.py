from .base import BaseObject
import os
import numpy as np
from pathlib import Path
import time
import logging


class Cells(BaseObject):
    """FENIA cells representation

    https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.1-mesh-description

    TODO:
        write mode == 0, 2
        read mode == 2 (by owner and neighbour) pyramid and prism conversion
    """
    def __init__(self, path, is_2d=False, mode=1, order=1):
        BaseObject.__init__(self, path)
        self.name = os.path.basename(self.path)
        self.is_2d = is_2d
        self.mode = mode
        self.order = order
        if self.order == 1:
            self.lines = np.empty([0, 2 + 1], int)
            self.lines_ids = np.empty([0], int)
            self.triangles = np.empty([0, 3 + 1], int)
            self.triangles_ids = np.empty([0], int)
            self.quads = np.empty([0, 4 + 1], int)
            self.quads_ids = np.empty([0], int)
            self.tetras = np.empty([0, 4 + 1], int)
            self.tetras_ids = np.empty([0], int)
            self.hexahedra = np.empty([0, 8 + 1], int)
            self.hexahedra_ids = np.empty([0], int)
            self.wedges = np.empty([0, 6 + 1], int)
            self.wedges_ids = np.empty([0], int)
            self.pyramids = np.empty([0, 5 + 1], int)
            self.pyramids_ids = np.empty([0], int)
        else:
            self.lines = np.empty([0, 2 + 1], int)
            self.lines_ids = np.empty([0], int)
            self.triangles = np.empty([0, 3 + 1], int)
            self.triangles_ids = np.empty([0], int)
            self.quads = np.empty([0, 4 + 1], int)
            self.quads_ids = np.empty([0], int)
            self.tetras = np.empty([0, 10 + 1], int)
            self.tetras_ids = np.empty([0], int)
            self.hexahedra = np.empty([0, 20 + 1], int)
            self.hexahedra_ids = np.empty([0], int)
            self.wedges = np.empty([0, 15 + 1], int)
            self.wedges_ids = np.empty([0], int)
            self.pyramids = np.empty([0, 13 + 1], int)
            self.pyramids_ids = np.empty([0], int)
        self.n_cells = 0
        self.data = np.empty([0])

    def read(self, faces_data=None):
        logging.info('Reading cells')
        t00 = time.perf_counter()
        if self.mode == 0:
            data = self.read_data()
            self.n_cells = int(data[0])
            start_index = 1
            cell_id = 0
            cell = np.empty([0], int)
            point_ctr = 0
            is_point = False
            for d in data[start_index:]:
                n_points = None
                if not is_point:
                    n_points = int(d)
                    point_ctr = 0
                    cell = np.empty([0], int)
                    cell = np.append(cell, [n_points], 0)
                    is_point = True
                else:
                    cell = np.append(cell, [int(d)], 0)
                    point_ctr += 1
                    if point_ctr == n_points:
                        is_point = False
                        if not self.is_2d:
                            if self.order == 1:
                                if n_points == 4:
                                    self.tetras = np.append(self.tetras, [cell], 0)
                                    self.tetras_ids = np.append(self.tetras_ids, [cell_id], 0)
                                    cell_id += 1
                                    continue
                                elif n_points == 5:
                                    self.pyramids = np.append(self.pyramids, [cell], 0)
                                    self.pyramids_ids = np.append(self.pyramids_ids, [cell_id], 0)
                                    cell_id += 1
                                    continue
                                elif n_points == 6:
                                    self.wedges = np.append(self.wedges, [cell], 0)
                                    self.wedges_ids = np.append(self.wedges_ids, [cell_id], 0)
                                    cell_id += 1
                                    continue
                                elif n_points == 8:
                                    self.hexahedra = np.append(self.hexahedra, [cell], 0)
                                    self.hexahedra_ids = np.append(self.hexahedra_ids, [cell_id], 0)
                                    cell_id += 1
                                    continue
                            else:
                                if n_points == 10:
                                    self.tetras = np.append(self.tetras, [cell], 0)
                                    self.tetras_ids = np.append(self.tetras_ids, [cell_id], 0)
                                    cell_id += 1
                                    continue
                                elif n_points == 13:
                                    self.pyramids = np.append(self.pyramids, [cell], 0)
                                    self.pyramids_ids = np.append(self.pyramids_ids, [cell_id], 0)
                                    cell_id += 1
                                    continue
                                elif n_points == 15:
                                    self.wedges = np.append(self.wedges, [cell], 0)
                                    self.wedges_ids = np.append(self.wedges_ids, [cell_id], 0)
                                    cell_id += 1
                                    continue
                                elif n_points == 20:
                                    self.hexahedra = np.append(self.hexahedra, [cell], 0)
                                    self.hexahedra_ids = np.append(self.hexahedra_ids, [cell_id], 0)
                                    cell_id += 1
                                    continue
                        else:
                            if n_points == 2:
                                self.lines = np.append(self.lines, [cell], 0)
                                self.lines_ids = np.append(self.lines_ids, [cell_id], 0)
                                cell_id += 1
                                continue
                            elif n_points == 3:
                                self.triangles = np.append(self.triangles, [cell], 0)
                                self.triangles_ids = np.append(self.triangles_ids, [cell_id], 0)
                                cell_id += 1
                                continue
                            elif n_points == 4:
                                self.quads = np.append(self.quads, [cell], 0)
                                self.quads_ids = np.append(self.quads_ids, [cell_id], 0)
                                cell_id += 1
                                continue
        elif self.mode == 1:
            data = self.read_data()
            self.n_cells = int(data[0])
            start_index = 1
            self.data = np.ascontiguousarray(data[start_index:], dtype=int)
        else:  # by owner and neighbour
            path = Path(self.path)
            if faces_data is None:
                logging.info('Reading faces')
                t0 = time.perf_counter()
                faces_path = path.parent / 'faces'
                faces = BaseObject(path=faces_path)
                faces_data = [int(x) for x in faces.read_data()][1:]
                logging.info(f'{time.perf_counter() - t0}s')
            logging.info('Reading owner')
            t0 = time.perf_counter()
            owner_path = path.parent / 'owner'
            owner = BaseObject(path=owner_path)
            owner_data = [int(x) for x in owner.read_data()]
            logging.info(f'{time.perf_counter() - t0}s')
            logging.info('Reading neighbour')
            t0 = time.perf_counter()
            neighbour_path = path.parent / 'neighbour'
            neighbour = BaseObject(path=neighbour_path)
            neighbour_data = [int(x) for x in neighbour.read_data()]
            logging.info(f'{time.perf_counter() - t0}s')
            logging.info('Evaluating faces points')
            t0 = time.perf_counter()
            faces_points = []
            i = 0
            while i < len(faces_data):
                n_points = faces_data[i]
                faces_points.append(faces_data[i+1:i+1+n_points])
                i += n_points + 1
            owner_cells = set(owner_data[1:])
            neighbour_cells = set(neighbour_data[1:])
            all_cells = owner_cells.union(neighbour_cells)
            n_cells = len(all_cells)
            logging.info(f'{time.perf_counter() - t0}s')
            logging.info('Evaluating cells faces')
            t0 = time.perf_counter()
            cells_faces = [[] for _ in range(n_cells)]
            cells_faces_type = [[] for _ in range(n_cells)]
            # if "owner" (1) face normal points to the cell
            # if "neighbour" (0) face normal points out of the cell
            for face_id, cell_id in enumerate(owner_data[1:]):
                cells_faces[cell_id].append(face_id)
                cells_faces_type[cell_id].append(1)  # owner
            for face_id, cell_id in enumerate(neighbour_data[1:]):
                cells_faces[cell_id].append(face_id)
                cells_faces_type[cell_id].append(0)  # neighbour
            data = []
            logging.info(f'{time.perf_counter() - t0}s')
            logging.info('Evaluating cells points')
            t0 = time.perf_counter()
            for i, cell_faces in enumerate(cells_faces):
                if len(cell_faces) == 6:  # hexahedron
                    cell_faces_points = [faces_points[x] for x in cell_faces]
                    # Evaluate cell_edges
                    cell_edges = set()
                    for ps in cell_faces_points:
                        p0 = ps[-1]
                        for p1 in ps:
                            edge = frozenset((p0, p1))  # unordered set
                            cell_edges.add(edge)
                            p0 = p1
                    # Set first face
                    f1 = cell_faces_points[0]
                    if cells_faces_type[i][0] == 0:  # reverse if neighbour
                        f1 = f1[::-1]
                    f2 = None
                    # Get second face as opposite to the first one
                    for j, ps in enumerate(cell_faces_points[1:], start=1):
                        if len(set(f1) & set(ps)) == 0:
                            f2 = ps
                            if cells_faces_type[i][j] == 1:  # reverse if owner
                                f2 = f2[::-1]
                                break
                    # Align f1 and f2 faces points by first f1 point
                    p0 = f1[0]
                    for point_j, p1 in enumerate(f2):
                        edge = frozenset((p0, p1))  # unordered set
                        if edge in cell_edges:
                            f1 = np.roll(f1, point_j)  # align f1 and f2 by p0
                            break
                    cell_points = np.concatenate((f1, f2))
                else:  # TODO tetrahedron, pyramid, prism, wedge, tet wedge
                    cell_points = set()
                    for face_id in cell_faces:
                        cell_points.update(faces_points[face_id])
                data.append(len(cell_points))
                data.extend(cell_points)
            logging.info(f'{time.perf_counter() - t0}s')
            logging.info('Updating data')
            t0 = time.perf_counter()
            self.n_cells = n_cells
            self.data = np.ascontiguousarray(data, dtype=int)
            logging.info(f'{time.perf_counter() - t0}s')
        logging.debug(f'cells: {self.n_cells}, len(data): {len(self.data)}, '
                      f'data: {self.data}')
        logging.info(f'Reading cells total: {time.perf_counter() - t00}s')

    def write(self):
        if self.mode == 1:
            with open(self.path, 'w') as f:
                f.write(self.header(cls='labelListList'))
                f.write('{}\n'.format(self.n_cells))
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
