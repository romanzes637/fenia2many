import os
import time

from fenia.unity import UnityMesh

print("Working directory: {}".format(os.getcwd()))

m = UnityMesh()

print("Clearing existing mesh")
start_time = time.time()
m.clear()
time_clear = time.time() - start_time
print("\tClearing time = {} seconds".format(time_clear))

print("Execution time = {} seconds".format(time_clear))
