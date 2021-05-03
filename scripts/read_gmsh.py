import os
import time

from gmsh.mesh import GmshMesh

path = os.path.join('cube.msh')
print("Reading {}".format(path))
m = GmshMesh(path)
start_time = time.time()
m.read()
end_time = time.time()
print("Execution time = {} seconds".format(end_time - start_time))
print("Execution speed (rough) = {:.0f} cells per second".format(len(m.cells_types) / (end_time - start_time)))
