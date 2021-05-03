import os
import time

from fenia.object.points import Points

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
    path = os.path.join('constant', 'polyMesh', 'fePoints.{}'.format(i))
    print("\tFile path: {}".format(path))
    p = Points(path=path, is_2d=is_2d, mode=mode, order=i)
    start_time = time.time()
    p.read()
    end_time = time.time()
    print("\tExecution time = {} seconds".format(end_time - start_time))
    print("\tNumber of points = {}".format(p.n_points))
    print("\tNumber of elements = {}".format(p.data.shape[0]))
    print("\tExecution speed = {:.0f} points per second".format(p.n_points / (end_time - start_time)))
    print("\tExecution speed = {:.0f} elements per second".format(p.data.shape[0] / (end_time - start_time)))
