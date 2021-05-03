from .base import BaseObject
import os


class CellZones(BaseObject):
    def __init__(self, path, is_2d=False):
        BaseObject.__init__(self, path)
        self.is_2d = is_2d
        self.name = os.path.basename(self.path)
        self.data = []
        self.names = []

    def read(self):
        data = self.read_data()
        n_zones = int(data[0])
        zone_start_index = 1
        for i in range(n_zones):
            self.names.append(data[zone_start_index])
            zone_size = int(data[zone_start_index + 5])
            zone_data_start_index = zone_start_index + 6
            zone_cells = []
            for j in range(zone_data_start_index, zone_data_start_index + zone_size):
                zone_cells.append(int(data[j]))
            # print(zone_cells)
            self.data.append(zone_cells)
            zone_start_index += (6 + zone_size)
        # print(self.data)

    def write(self):
        with open(self.path, 'w') as f:
            f.write(self.header(cls='regIOobject'))
            f.write('{}\n'.format(len(self.names)))
            f.write('(\n')
            for i in range(len(self.names)):
                f.write('{}\n'.format(self.names[i]))
                f.write('{\n')
                f.write('type cellZone;\n')
                f.write('cellLabels List<label>\n')
                f.write('{}\n'.format(len(self.data[i])))
                f.write('(\n')
                for j in self.data[i]:
                    f.write('{}\n'.format(j))
                f.write(');\n')
                f.write('}\n\n')
            f.write(')\n')
            f.write(self.footer())
