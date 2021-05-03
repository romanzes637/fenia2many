import unittest
import os
import time
import numpy as np

from fenia.object.points import Points
from fenia.object.faces import Faces
from fenia.object.cells import Cells
from fenia.object.face_zones import FaceZones
from fenia.object.cell_zones import CellZones
from fenia.object.dictionary import Dictionary
from fenia.object.field import Field


class TestFenia(unittest.TestCase):
    def test_points(self):
        print("Working directory: {}".format(os.getcwd()))
        # Storage mode (0 - as numpy shape array, 1 - as numpy contiguous array (C-array))
        mode = 1
        # Is 2d points?
        is_2d = False
        # Orders of mesh
        orders = [1]
        for i in orders:
            print("Reading {} order points".format(i))
            # Local path to points file
            path = os.path.join('fePoints.{}'.format(i))
            print("\tFile path: {}".format(path))
            p = Points(path=path, is_2d=is_2d, mode=mode, order=i)
            start_time = time.time()
            p.read()
            end_time = time.time()
            print("\tExecution time = {} seconds".format(end_time - start_time))
            print("\tNumber of points = {}".format(p.n_points))
            print("\tNumber of elements = {}".format(p.data.shape[0]))
            print("\tExecution speed = {:.0f} points per second".format(p.n_points / (end_time - start_time)))
            print("\tExecution speed = {:.0f} items per second".format(p.data.shape[0] / (end_time - start_time)))
            print("Writing {} order points".format(i))
            # Change path to new points file
            p.path = os.path.join('fePointsNew.{}'.format(i))
            start_time = time.time()
            p.write()
            end_time = time.time()
            print("\tExecution time = {} seconds".format(end_time - start_time))
            print("\tNumber of points = {}".format(p.n_points))
            print("\tNumber of items = {}".format(p.data.shape[0]))
            print("\tExecution speed = {:.0f} points per second".format(p.n_points / (end_time - start_time)))
            print("\tExecution speed = {:.0f} items per second".format(p.data.shape[0] / (end_time - start_time)))

    def test_faces(self):
        print("Working directory: {}".format(os.getcwd()))
        # Storage mode (0 - as numpy shape array, 1 - as numpy contiguous array (C-array))
        mode = 1
        # Is 2d points?
        is_2d = False
        # Orders of mesh
        orders = [1]
        for i in orders:
            print("Reading {} order faces".format(i))
            # Local path to points file
            path = os.path.join('faces'.format(i))
            print("\tFile path: {}".format(path))
            f = Faces(path=path, is_2d=is_2d, mode=mode, order=i)
            start_time = time.time()
            f.read()
            end_time = time.time()
            print("\tExecution time = {} seconds".format(end_time - start_time))
            print("\tNumber of faces = {}".format(f.n_faces))
            print("\tNumber of items = {}".format(f.data.shape[0]))
            print("\tExecution speed = {:.0f} faces per second".format(f.n_faces / (end_time - start_time)))
            print("\tExecution speed = {:.0f} items per second".format(f.data.shape[0] / (end_time - start_time)))
            print("Writing {} order points".format(i))
            # Change path to new points file
            f.path = os.path.join('facesNew'.format(i))
            start_time = time.time()
            f.write()
            end_time = time.time()
            print("\tExecution time = {} seconds".format(end_time - start_time))
            print("\tNumber of faces = {}".format(f.n_faces))
            print("\tNumber of items = {}".format(f.data.shape[0]))
            print("\tExecution speed = {:.0f} faces per second".format(f.n_faces / (end_time - start_time)))
            print("\tExecution speed = {:.0f} items per second".format(f.data.shape[0] / (end_time - start_time)))

    def test_cells(self):
        print("Working directory: {}".format(os.getcwd()))
        # Storage mode (0 - as numpy shape array, 1 - as numpy contiguous array (C-array))
        mode = 1
        # Is 2d points?
        is_2d = False
        # Orders of mesh
        orders = [1]
        for i in orders:
            print("Reading {} order cells".format(i))
            # Local path to points file
            path = os.path.join('glFe.{}'.format(i))
            print("\tFile path: {}".format(path))
            c = Cells(path=path, is_2d=is_2d, mode=mode, order=i)
            start_time = time.time()
            c.read()
            end_time = time.time()
            print("\tExecution time = {} seconds".format(end_time - start_time))
            print("\tNumber of cells = {}".format(c.n_cells))
            print("\tNumber of items = {}".format(c.data.shape[0]))
            print("\tExecution speed = {:.0f} cells per second".format(c.n_cells / (end_time - start_time)))
            print("\tExecution speed = {:.0f} items per second".format(c.data.shape[0] / (end_time - start_time)))
            print("Writing {} order points".format(i))
            # Change path to new points file
            c.path = os.path.join('glFeNew.{}'.format(i))
            start_time = time.time()
            c.write()
            end_time = time.time()
            print("\tExecution time = {} seconds".format(end_time - start_time))
            print("\tNumber of cells = {}".format(c.n_cells))
            print("\tNumber of items = {}".format(c.data.shape[0]))
            print("\tExecution speed = {:.0f} cells per second".format(c.n_cells / (end_time - start_time)))
            print("\tExecution speed = {:.0f} items per second".format(c.data.shape[0] / (end_time - start_time)))

    def test_face_zones(self):
        print("Working directory: {}".format(os.getcwd()))
        path2 = os.path.join('faceZones')
        path = os.path.join('boundary')
        is_2d = False
        read_type = 0
        print("Reading {} face zones")
        fz = FaceZones(path=path, path2=path2, is_2d=is_2d, read_type=read_type)
        start_time = time.time()
        fz.read()
        end_time = time.time()
        print("\tExecution time = {} seconds".format(end_time - start_time))
        print("\tNumber of face zones = {}".format(len(fz.names)))
        print("\tExecution speed = {:.0f} face zones per second".format(len(fz.names) / (end_time - start_time)))
        print("Writing {} face zones")
        start_time = time.time()
        fz.write()
        end_time = time.time()
        print("\tExecution time = {} seconds".format(end_time - start_time))
        print("\tNumber of face zones = {}".format(len(fz.names)))
        print("\tExecution speed = {:.0f} face zones per second".format(len(fz.names) / (end_time - start_time)))

    def test_cell_zones(self):
        print("Working directory: {}".format(os.getcwd()))
        # Is 2d points?
        is_2d = False
        print("Reading cell zones")
        # Local path to file
        path = os.path.join('cellZones')
        print("\tFile path: {}".format(path))
        cz = CellZones(path=path, is_2d=is_2d)
        start_time = time.time()
        cz.read()
        end_time = time.time()
        print("\tExecution time = {} seconds".format(end_time - start_time))
        print("\tNumber of cell zones = {}".format(len(cz.names)))
        print("\tExecution speed = {:.0f} cell zones per second".format(len(cz.names) / (end_time - start_time)))
        print("Writing cell zones")
        # Change path to new file
        cz.path = os.path.join('cellZonesNew')
        start_time = time.time()
        cz.write()
        end_time = time.time()
        print("\tExecution time = {} seconds".format(end_time - start_time))
        print("\tNumber of cell zones = {}".format(len(cz.names)))
        print("\tExecution speed = {:.0f} cell zones per second".format(len(cz.names) / (end_time - start_time)))
        print("Reading written cell zones")
        # Change path to written file
        path = os.path.join('cellZonesNew')
        print("\tFile path: {}".format(path))
        cz = CellZones(path=path, is_2d=is_2d)
        start_time = time.time()
        cz.read()
        end_time = time.time()
        print("\tExecution time = {} seconds".format(end_time - start_time))
        print("\tNumber of cell zones = {}".format(len(cz.names)))
        print("\tExecution speed = {:.0f} cell zones per second".format(len(cz.names) / (end_time - start_time)))

    def test_read_dictionary(self):
        print("Working directory: {}".format(os.getcwd()))
        print("Reading dictionary")
        path = os.path.join('controlDict')
        print("\tFile path: {}".format(path))
        d = Dictionary(path)
        start_time = time.time()
        d.read()
        end_time = time.time()
        print("\tExecution time = {} seconds".format(end_time - start_time))
        print(d.data)

    def test_field(self):
        print("Working directory: {}".format(os.getcwd()))
        # Storage mode (0 - as numpy shape array, 1 - as numpy contiguous array (C-array))
        mode = 1
        print("Reading data")
        path = os.path.join('dU')
        print("\tFile path: {}".format(path))
        f = Field(path=path, mode=mode)
        start_time = time.time()
        f.read()
        end_time = time.time()
        print("\tReading time = {} seconds".format(end_time - start_time))
        print("\tNumber of elements = {}".format(f.n_elements))
        print("\tNumber of all elements = {}".format(f.data.shape[0]))
        print("\tReading speed = {:.0f} items per second".format(f.n_elements / (end_time - start_time)))
        print("\tAll reading speed = {:.0f} items per second".format(f.data.shape[0] / (end_time - start_time)))
        print("Extending data")
        start_time = time.time()
        if f.n_elements == 1:
            n_points = 10000000
            value = f.data.tolist()
            f.n_elements = n_points
            data = []
            for i in range(f.n_elements):
                data.extend(value)
            f.data = np.ascontiguousarray(data, dtype=float)
        end_time = time.time()
        print("\tExtending time = {} seconds".format(end_time - start_time))
        print("\tNumber of elements = {}".format(f.n_elements))
        print("\tNumber of all elements = {}".format(f.data.shape[0]))
        if end_time - start_time > 0:
            print("\tExecution speed = {:.0f} items per second".format(f.n_elements / (end_time - start_time)))
            print("\tAll execution speed = {:.0f} items per second".format(f.data.shape[0] / (end_time - start_time)))

if __name__ == '__main__':
    unittest.main()
