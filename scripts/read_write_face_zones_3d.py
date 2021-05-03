import os
import time

from fenia.object.face_zones import FaceZones

print("Working directory: {}".format(os.getcwd()))

path = os.path.join('constant', 'polyMesh', 'faceZones')
path2 = os.path.join('constant', 'polyMesh', 'boundary')
is_2d = False
read_type = 2

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
