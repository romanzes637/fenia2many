import os
import time

from fenia.object.cell_zones import CellZones

print("Working directory: {}".format(os.getcwd()))

# Is 2d points?
is_2d = False

print("Reading {} cell zones")
# Local path to points file
path = os.path.join('constant', 'polyMesh', 'cellZones')
print("\tFile path: {}".format(path))
cz = CellZones(path=path, is_2d=is_2d)
start_time = time.time()
cz.read()
end_time = time.time()
print("\tExecution time = {} seconds".format(end_time - start_time))
print("\tNumber of cell zones = {}".format(len(cz.names)))
print("\tExecution speed = {:.0f} cell zones per second".format(len(cz.names) / (end_time - start_time)))

print("Writing {} cell zones")
# Change path to new points file
cz.path = os.path.join('constant', 'polyMesh', 'cellZonesWrite')
start_time = time.time()
cz.write()
end_time = time.time()
print("\tExecution time = {} seconds".format(end_time - start_time))
print("\tNumber of cell zones = {}".format(len(cz.names)))
print("\tExecution speed = {:.0f} cell zones per second".format(len(cz.names) / (end_time - start_time)))
