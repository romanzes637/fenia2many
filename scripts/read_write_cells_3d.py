import os
import time

from fenia.object.cells import Cells

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
    path = os.path.join('constant', 'polyMesh', 'glFe.{}'.format(i))
    print("\tFile path: {}".format(path))
    c = Cells(path=path, is_2d=is_2d, mode=mode, order=i)
    start_time = time.time()
    c.read()
    end_time = time.time()
    print("\tExecution time = {} seconds".format(end_time - start_time))
    print("\tNumber of cells = {}".format(c.n_cells))
    print("\tNumber of elements = {}".format(c.data.shape[0]))
    print("\tExecution speed = {:.0f} cells per second".format(c.n_cells / (end_time - start_time)))
    print("\tExecution speed = {:.0f} elements per second".format(c.data.shape[0] / (end_time - start_time)))

    print("Writing {} order points".format(i))
    # Change path to new points file
    c.path = os.path.join('constant', 'polyMesh', 'glFeWrite.{}'.format(i))
    start_time = time.time()
    c.write()
    end_time = time.time()
    print("\tExecution time = {} seconds".format(end_time - start_time))
    print("\tNumber of cells = {}".format(c.n_cells))
    print("\tNumber of elements = {}".format(c.data.shape[0]))
    print("\tExecution speed = {:.0f} cells per second".format(c.n_cells / (end_time - start_time)))
    print("\tExecution speed = {:.0f} elements per second".format(c.data.shape[0] / (end_time - start_time)))