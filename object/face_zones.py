from .base import BaseObject
import os


class FaceZones(BaseObject):
    def __init__(self, path, path2, is_2d=False, read_type=0):
        BaseObject.__init__(self, path)
        self.path2 = path2
        self.is_2d = is_2d
        # If read_type == 0 - read boundary, 1 - faceZones, otherwise - both files
        self.read_type = read_type
        self.name = os.path.basename(self.path)
        self.name2 = os.path.basename(self.path2)
        self.data = []
        self.names = []

    def read(self):
        if self.read_type == 0:
            self.read_boundary()
        elif self.read_type == 1:
            self.read_face_zones()
        else:
            self.read_boundary()
            self.read_face_zones()

    def read_boundary(self):
        data = self.read_data()
        n_zones = int(data[0])
        zone_start_index = 1
        for i in range(n_zones):
            self.names.append(data[zone_start_index])
            zone_size = int(data[zone_start_index + 4])
            zone_start_face = int(data[zone_start_index + 6])
            zone_faces = []
            for j in range(zone_size):
                zone_faces.append(zone_start_face + j)
            self.data.append(zone_faces)
            zone_start_index += 7

    def read_face_zones(self):
        # Save path
        path = self.path
        # Temporarily set self.path to faceZones file
        self.path = self.path2
        # Read faceZones file
        data = self.read_data()
        n_zones = int(data[0])
        zone_start_index = 1
        for i in range(n_zones):
            self.names.append(data[zone_start_index])
            zone_size = int(data[zone_start_index + 5])
            zone_data_start_index = zone_start_index + 6
            zone_faces = []
            for j in range(zone_data_start_index, zone_data_start_index + zone_size):
                zone_faces.append(int(data[j]))
            self.data.append(zone_faces)
            zone_start_index += (6 + zone_size + 4)
        # Return self.path to boundary file
        self.path = path

    # FIXME Workaround all face zones writes to faceZones file
    def write(self):
        with open(self.path2, 'w') as f:
            f.write(self.header(cls='regIOobject'))
            f.write('{}\n'.format(len(self.names)))
            f.write('(\n')
            for i in range(len(self.names)):
                f.write('{}\n'.format(self.names[i]))
                f.write('{\n')
                f.write('type faceZone;\n')
                f.write('faceLabels List<label>\n')
                f.write('{}\n'.format(len(self.data[i])))
                f.write('(\n')
                for j in self.data[i]:
                    f.write('{}\n'.format(j))
                f.write(');\n')
                f.write('}\n\n')
            f.write(')\n')
            f.write(self.footer())
