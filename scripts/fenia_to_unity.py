import os
import sys
import time

from fenia.connection import fenia_to_obj
from fenia.connection import fenia_to_unity
from fenia.mesh.fenia import FeniaMesh
from fenia.obj import ObjMesh
from fenia.unity import UnityMesh

print("Working directory: {}".format(os.getcwd()))

if len(sys.argv) > 1 and sys.argv[1] == '1':
    face_zones_read_type = 1
elif len(sys.argv) > 1 and sys.argv[1] == '2':
    face_zones_read_type = 2
else:
    face_zones_read_type = 0

fm = FeniaMesh(face_zones_read_type=face_zones_read_type)
um = UnityMesh()
om = ObjMesh()

print("Clearing existing mesh")
start_time = time.time()
um.clear()
time_clear = time.time() - start_time
print("\tClearing time = {} seconds".format(time_clear))

print("Reading data")
start_time = time.time()
fm.read()
time_read = time.time() - start_time
print("\tReading time = {} seconds".format(time_read))

print("Converting mesh")
start_time = time.time()
fenia_to_obj(fm, om, is_triangulate=True)
um.mesh = om
fenia_to_unity(fm, um)
time_convert = time.time() - start_time
print("\tConverting time = {} seconds".format(time_convert))

print("Writing data")
start_time = time.time()
um.write()
time_write = time.time() - start_time
print("\tWriting time = {} seconds".format(time_write))

print("Execution time = {} seconds".format(time_clear + time_read + time_convert + time_write))
