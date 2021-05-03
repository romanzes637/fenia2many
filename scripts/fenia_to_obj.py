import os
import sys
import time

from connection import fenia_to_obj
from mesh.fenia import FeniaMesh
from obj import ObjMesh

print("Working directory: {}".format(os.getcwd()))

if len(sys.argv) > 1 and sys.argv[1] == '1':
    face_zones_read_type = 1
elif len(sys.argv) > 1 and sys.argv[1] == '2':
    face_zones_read_type = 2
else:
    face_zones_read_type = 0

if len(sys.argv) > 2 and sys.argv[2] == '1':
    is_triangulate = True
else:
    is_triangulate = False

if len(sys.argv) > 3 and sys.argv[3] == '1':
    is_write_texture_vertices = False
else:
    is_write_texture_vertices = True

fm = FeniaMesh(face_zones_read_type=face_zones_read_type)
om = ObjMesh()
om.is_write_texture_vertices = is_write_texture_vertices

print("Clearing existing mesh")
start_time = time.time()
om.clear()
time_clear = time.time() - start_time
print("\tClearing time = {} seconds".format(time_clear))

print("Reading data")
start_time = time.time()
fm.read()
time_read = time.time() - start_time
print("\tReading time = {} seconds".format(time_read))

print("Converting mesh")
start_time = time.time()
fenia_to_obj(fm, om, is_triangulate)
time_convert = time.time() - start_time
print("\tConverting time = {} seconds".format(time_convert))

print("Writing data")
start_time = time.time()
om.write()
time_write = time.time() - start_time
print("\tWriting time = {} seconds".format(time_write))

print("Execution time = {} seconds".format(time_clear+time_read+time_convert+time_write))
