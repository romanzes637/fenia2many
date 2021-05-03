import os
import time

from fenia.object.dictionary import Dictionary

print("Working directory: {}".format(os.getcwd()))

print("Reading dictionary")
path = os.path.join('system', 'controlDict')
print("\tFile path: {}".format(path))
d = Dictionary(path)
start_time = time.time()
d.read()
end_time = time.time()
print("\tExecution time = {} seconds".format(end_time - start_time))
print(d.data)
