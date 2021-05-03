import numpy as np
import os
import sys
import time
import logging

from ..object.cell_zones import CellZones
from ..object.faces import Faces
from ..object.field import Field
from ..object.cells import Cells
from ..object.face_zones import FaceZones
from ..object.points import Points
from ..object.dictionary import Dictionary


class FeniaMesh:
    """FENIA mesh representation"""

    def __init__(self, face_zones_read_type=0, read_control=False):
        self.name = os.path.basename(os.getcwd())
        self.face_zones_read_type = face_zones_read_type
        self.read_control_dict = read_control
        if os.path.exists(os.path.relpath(os.path.join('constant', 'mesh2D'))):
            self.is_2d = True
        else:
            self.is_2d = False
        if not self.is_2d:
            self.points = Points(os.path.join('constant', 'polyMesh', 'fePoints.1'), mode=1)
            self.points2 = Points(os.path.join('constant', 'polyMesh', 'fePoints.2'), mode=1)
            self.cells = Cells(os.path.join('constant', 'polyMesh', 'glFe.1'), mode=1)
            self.cells2 = Cells(os.path.join('constant', 'polyMesh', 'glFe.2'), order=2, mode=1)
            self.faces = Faces(os.path.join('constant', 'polyMesh', 'faces'), mode=1)
            self.cell_zones = CellZones(os.path.join('constant', 'polyMesh', 'cellZones'))
            self.face_zones = FaceZones(os.path.join('constant', 'polyMesh', 'boundary'),
                                        os.path.join('constant', 'polyMesh', 'faceZones'),
                                        read_type=face_zones_read_type)
        else:
            self.points = Points(os.path.join('constant', 'mesh2D', 'points'), self.is_2d)
            self.points2 = Points(os.path.join('constant', 'mesh2D', 'points2'), self.is_2d)
            self.cells = Cells(os.path.join('constant', 'mesh2D', 'cells'), self.is_2d)
            self.cells2 = Cells(os.path.join('constant', 'mesh2D', 'cells2'), self.is_2d, order=2)
            self.faces = Faces(os.path.join('constant', 'mesh2D', 'faces'), self.is_2d)
            self.cell_zones = CellZones(os.path.join('constant', 'mesh2D', 'cellZones'), self.is_2d)
            self.face_zones = FaceZones(os.path.join('constant', 'mesh2D', 'boundary'),
                                        os.path.join('constant', 'mesh2D', 'faceZones'), is_2d=self.is_2d)
        self.control = Dictionary(os.path.join('system', 'controlDict'))
        self.times = list()
        self.times_fields = list()
        self.find_times()
        self.init_fields()

    def find_times(self):
        """
        Find directories with time data (e.g. field's values at some time step)
        and add time value to self.times as float(time_directory_name)
        """
        for d in os.listdir(os.getcwd()):
            if os.path.isdir(d):
                try:
                    float(d)
                except ValueError:
                    pass
                else:
                    self.times.append(d)
        self.times.sort(key=float)

    def init_fields(self):
        times_fields_paths = list()
        for t in self.times:
            fields_paths = list()
            for root, dirs, files in os.walk(os.path.relpath(str(t))):
                for name in files:
                    # TODO Workaround exclude temporary files and uniform/time field
                    if name[-1] != '~' and name != 'time':
                        fields_paths.append(os.path.join(root, name))
            times_fields_paths.append(fields_paths)
        for fields_paths in times_fields_paths:
            time_fields = list()
            for field_path in fields_paths:
                time_fields.append(Field(field_path))
            self.times_fields.append(time_fields)

    def clear_fields(self):
        self.times = []
        self.times_fields = []

    def read(self):
        n_files = 8
        for time_fields in self.times_fields:
            n_files += len(time_fields)
        files_cnt = 0
        sys.stdout.write('{:.0f}% Reading {}\n'.format(float(files_cnt) / n_files * 100, self.points.path))
        if self.points.is_exists():
            self.points.read()
        else:
            self.points.mode = 2
            self.points.read()
            self.points.mode = 1
            logging.warning(f"{self.points.path} doesn't exist! "
                            f"Reading from points")
        files_cnt += 1
        sys.stdout.write('{:.0f}% Reading {}\n'.format(float(files_cnt) / n_files * 100, self.points2.path))
        if self.points2.is_exists():
            self.points2.read()
        else:
            print(f"{self.points2.path} doesn't exist! No 2 order points")
        files_cnt += 1
        sys.stdout.write('{:.0f}% Reading {}\n'.format(float(files_cnt) / n_files * 100, self.faces.path))
        if self.faces.is_exists():
            self.faces.read()
        else:
            raise ValueError(f"{self.faces.path} doesn't exist!")
        files_cnt += 1
        sys.stdout.write('{:.0f}% Reading {}\n'.format(float(files_cnt) / n_files * 100, self.cells.path))
        if self.cells.is_exists():
            self.cells.read()
        else:
            logging.warning(f"{self.cells.path} doesn't exist! "
                            f"Reading from owner and neighbour")
            self.cells.mode = 2
            self.cells.read(faces_data=self.faces.data)
            self.cells.mode = 1
        files_cnt += 1
        sys.stdout.write('{:.0f}% Reading {}\n'.format(float(files_cnt) / n_files * 100, self.cells2.path))
        if self.cells2.is_exists():
            self.cells2.read()
        else:
            print(f"{self.cells2.path} doesn't exist! No 2 order cells")
        files_cnt += 1
        sys.stdout.write('{:.0f}% Reading {}\n'.format(float(files_cnt) / n_files * 100, self.cell_zones.path))
        self.cell_zones.read()
        files_cnt += 1
        if self.face_zones_read_type == 0:
            output = '{:.0f}% Reading {}\n'.format(float(files_cnt) / n_files * 100, self.face_zones.path)
        elif self.face_zones_read_type == 1:
            output = '{:.0f}% Reading {}\n'.format(float(files_cnt) / n_files * 100, self.face_zones.path2)
        else:
            output = '{:.0f}% Reading {} and {}\n'.format(float(files_cnt) / n_files * 100, self.face_zones.path,
                                                          self.face_zones.path2)
        sys.stdout.write(output)
        self.face_zones.read()
        files_cnt += 1
        if self.read_control_dict:
            sys.stdout.write('{:.0f}% Reading {}\n'.format(float(files_cnt) / n_files * 100, self.control.path))
            self.control.read()
        files_cnt += 1
        for time_fields in self.times_fields:
            for time_field in time_fields:
                sys.stdout.write('\r{:.0f}% Reading {}'.format(float(files_cnt) / n_files * 100, time_field.path))
                sys.stdout.flush()
                if time_field.is_exists():
                    time_field.read()
                    # Uniform field correction
                    if time_field.n_elements == 1:
                        if 'meshTypeI' in time_field.dictionary and 'intSet' in time_field.dictionary:
                            # TODO Integration point field
                            pass
                        elif 'meshTypeI' in time_field.dictionary:
                            # Point field
                            if int(time_field.dictionary.get('meshTypeI')) == 1:
                                time_field.n_elements = self.points.n_points
                            elif int(time_field.dictionary.get('meshTypeI')) == 2:
                                time_field.n_elements = self.points2.n_points
                            if time_field.mode == 0:
                                value = time_field.data[0]
                                for i in range(time_field.n_elements - 1):
                                    time_field.data = np.append(time_field.data, [value], axis=0)
                            else:
                                value = time_field.data.tolist()
                                data = []
                                for i in range(time_field.n_elements):
                                    data.extend(value)
                                time_field.data = np.ascontiguousarray(data, dtype=float)
                        else:
                            # Cell field
                            time_field.n_elements = self.cells.n_cells
                            if time_field.mode == 0:
                                for i in range(self.cells.n_cells - 1):
                                    time_field.data = np.append(time_field.data, [value])
                            else:
                                data = []
                                for i in range(time_field.n_elements):
                                    data.extend(value)
                                time_field.data = np.ascontiguousarray(data, dtype=float)
                else:
                    raise OSError("File doesn't exists: " + time_field.path)
                files_cnt += 1
        sys.stdout.write('\r{:.0f}%\n'.format(float(files_cnt) / n_files * 100))
        sys.stdout.flush()
