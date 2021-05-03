import os
import sys
import time
import logging
import argparse

from fenia.mesh.paraview import ParaViewMesh

if __name__ == '__main__':
    print("Working directory: {}".format(os.getcwd()))

    format_map = {'xml': 0, 'ascii': 1}
    faces_maps = {'boundary': 0, 'zones': 1, 'both': 2}
    verbose_map = logging._nameToLevel
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', default='DEBUG',
                        choices=verbose_map.keys())
    parser.add_argument('--format', '-o', default='xml',
                        choices=format_map.keys())
    parser.add_argument('--faces', '-f', default='boundary',
                        choices=faces_maps.keys())
    args = parser.parse_args()
    print(args)
    fmt = format_map[args.format]
    fz = faces_maps[args.faces]
    level = verbose_map[args.verbose]

    logging.basicConfig(filename='fenia_to_paraview.csv',
                        format='"%(asctime)s",%(levelname)s,"%(message)s"',
                        # encoding='utf-8'  # since python 3.9
                        level=level)

    print('Creating mesh')
    t0 = time.perf_counter()
    m = ParaViewMesh(face_zones_read_type=fz)
    time_create = time.perf_counter() - t0
    print(f"Creating time: {time_create}s")

    print("Clearing existing mesh")
    t0 = time.perf_counter()
    m.clear()
    time_clear = time.perf_counter() - t0
    print(f"Clearing time: {time_clear}s")

    print("Reading data")
    t0 = time.perf_counter()
    m.read()
    time_read = time.perf_counter() - t0
    print(f"Reading time: {time_read}s")

    print("Writing data")
    t0 = time.perf_counter()
    m.write(form=fmt)
    time_write = time.perf_counter() - t0
    print(f"Writing time: {time_write}s")

    time_total = time_create + time_clear + time_read + time_write
    print(f"Execution time: {time_total}s")
