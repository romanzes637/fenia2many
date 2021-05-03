import os
import time

import numpy as np

from fenia.object import Field

print("Working directory: {}".format(os.getcwd()))

# Storage mode (0 - as numpy shape array, 1 - as numpy contiguous array (C-array))
mode = 1

print("Reading data")
path = os.path.join('0', 'U')
print("\tFile path: {}".format(path))
f = Field(path=path, mode=mode)
start_time = time.time()
f.read()
end_time = time.time()
print("\tReading time = {} seconds".format(end_time - start_time))
print("\tNumber of elements = {}".format(f.n_elements))
print("\tNumber of all elements = {}".format(f.data.shape[0]))
print("\tReading speed = {:.0f} elements per second".format(f.n_elements / (end_time - start_time)))
print("\tAll reading speed = {:.0f} elements per second".format(f.data.shape[0] / (end_time - start_time)))

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
print("\tExecution speed = {:.0f} elements per second".format(f.n_elements / (end_time - start_time)))
print("\tAll execution speed = {:.0f} elements per second".format(f.data.shape[0] / (end_time - start_time)))
