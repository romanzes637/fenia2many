import os
import time

from fenia.object.faces import Faces

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
    path = os.path.join('constant', 'polyMesh', 'faces'.format(i))
    print("\tFile path: {}".format(path))
    f = Faces(path=path, is_2d=is_2d, mode=mode, order=i)
    start_time = time.time()
    f.read()
    end_time = time.time()
    print("\tExecution time = {} seconds".format(end_time - start_time))
    print("\tNumber of faces = {}".format(f.n_faces))
    print("\tNumber of elements = {}".format(f.data.shape[0]))
    print("\tExecution speed = {:.0f} faces per second".format(f.n_faces / (end_time - start_time)))
    print("\tExecution speed = {:.0f} elements per second".format(f.data.shape[0] / (end_time - start_time)))

    print("Writing {} order points".format(i))
    # Change path to new points file
    f.path = os.path.join('constant', 'polyMesh', 'facesWrite'.format(i))
    start_time = time.time()
    f.write()
    end_time = time.time()
    print("\tExecution time = {} seconds".format(end_time - start_time))
    print("\tNumber of faces = {}".format(f.n_faces))
    print("\tNumber of elements = {}".format(f.data.shape[0]))
    print("\tExecution speed = {:.0f} faces per second".format(f.n_faces / (end_time - start_time)))
    print("\tExecution speed = {:.0f} elements per second".format(f.data.shape[0] / (end_time - start_time)))