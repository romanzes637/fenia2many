import os
import sys


class GmshMesh:
    """gmsh mesh representation

    https://gmsh.info/
    """

    def __init__(self, path):
        self.path = path
        self.name = os.path.splitext(os.path.basename(self.path))[0]
        self.ext = os.path.splitext(os.path.basename(self.path))[1]
        self.mesh_format = []
        self.nodes = []
        self.points = []
        self.points_types = []
        self.lines = []
        self.lines_types = []
        self.faces = []
        self.faces_types = []
        self.cells = []
        self.cells_types = []
        self.point_zones = []
        self.point_zones_numbers = []
        self.point_zones_names = []
        self.line_zones = []
        self.line_zones_numbers = []
        self.line_zones_names = []
        self.face_zones = []
        self.face_zones_numbers = []
        self.face_zones_names = []
        self.cell_zones = []
        self.cells_zones_numbers = []
        self.cells_zones_names = []
        self.gmsh_point_numbers = [15]
        self.gmsh_line_numbers = [1, 8, 26, 27, 28]
        self.gmsh_face_numbers = [2, 3, 9, 10, 16, 20, 21, 22, 23, 24, 25]
        self.gmsh_cell_numbers = [4, 5, 6, 7, 11, 12, 13, 14, 17, 18, 19, 29, 30, 31]

    def is_exists(self):
        return os.path.exists(os.path.relpath(self.path))

    def read(self):
        is_mesh_format = False
        is_physical_names = False
        is_nodes = False
        is_elements = False
        n_objects = 0
        lines_ctr = 0
        if self.is_exists():
            with open(self.path) as f:
                for i, line in enumerate(f):
                    if line.startswith('$MeshFormat'):
                        is_mesh_format = True
                        lines_ctr = 0
                        print('Reading Mesh Format')
                        continue
                    elif line.startswith('$EndMeshFormat'):
                        is_mesh_format = False
                        print('End Reading Mesh Format')
                        continue
                    elif line.startswith('$PhysicalNames'):
                        is_physical_names = True
                        lines_ctr = 0
                        print('Reading Physical Names')
                        continue
                    elif line.startswith('$EndPhysicalNames'):
                        is_physical_names = False
                        print('\nEnd Reading Physical Names')
                        continue
                    elif line.startswith('$Nodes'):
                        is_nodes = True
                        lines_ctr = 0
                        print('Reading Nodes')
                        continue
                    elif line.startswith('$EndNodes'):
                        is_nodes = False
                        print('\nEnd Reading Nodes')
                        continue
                    elif line.startswith('$Elements'):
                        is_elements = True
                        lines_ctr = 0
                        print('Reading Elements')
                        continue
                    elif line.startswith('$EndElements'):
                        is_elements = False
                        print('\nEnd Reading Elements')
                        continue

                    if lines_ctr == 0 and not is_mesh_format:
                        n_objects = int(line)
                        lines_ctr += 1
                        print('Number of objects = {}'.format(n_objects))
                        continue

                    lines_ctr += 1

                    if is_mesh_format:
                        self.mesh_format = line.split()
                    elif is_physical_names:
                        tokens = line.split()
                        # If dim of zone = 0
                        if tokens[0] == '0':
                            self.point_zones_numbers.append(int(tokens[1]))
                            self.point_zones_names.append(tokens[2])
                            self.point_zones.append([])
                        # If dim of zone = 1
                        elif tokens[0] == '1':
                            self.line_zones_numbers.append(int(tokens[1]))
                            self.line_zones_names.append(tokens[2])
                            self.line_zones.append([])
                        # If dim of zone = 2
                        elif tokens[0] == '2':
                            self.face_zones_numbers.append(int(tokens[1]))
                            self.face_zones_names.append(tokens[2])
                            self.face_zones.append([])
                        # If dim of zone = 3
                        elif tokens[0] == '3':
                            self.cells_zones_numbers.append(int(tokens[1]))
                            self.cells_zones_names.append(tokens[2])
                            self.cell_zones.append([])
                        else:
                            raise ValueError('Bad dim = {} in line {}'.format(tokens[0], i))
                    elif is_nodes:
                        tokens = line.split()
                        self.nodes.extend(map(float, tokens[1:]))
                        # print(self.points)
                    elif is_elements:
                        tokens = list(map(int, line.split()))
                        # If element is 0D
                        if tokens[1] in self.gmsh_point_numbers:
                            self.points_types.append(tokens[1])
                            # tags: physical_entity, elementary_entity, mesh_partition
                            n_tags = tokens[2]
                            point_zone_number = tokens[3]
                            point_zone_i = self.point_zones_numbers.index(point_zone_number)
                            self.point_zones[point_zone_i].append(tokens[0])
                            nodes_start_i = 3 + n_tags
                            self.points.append(len(tokens[nodes_start_i:]))
                            self.points.extend(tokens[nodes_start_i:])
                        # If element is 1D
                        elif tokens[1] in self.gmsh_line_numbers:
                            self.lines_types.append(tokens[1])
                            # tags: physical_entity, elementary_entity, mesh_partition
                            n_tags = tokens[2]
                            line_zone_number = tokens[3]
                            line_zone_i = self.line_zones_numbers.index(line_zone_number)
                            self.line_zones[line_zone_i].append(tokens[0])
                            nodes_start_i = 3 + n_tags
                            self.lines.append(len(tokens[nodes_start_i:]))
                            self.lines.extend(tokens[nodes_start_i:])
                        # If element is 2D
                        elif tokens[1] in self.gmsh_face_numbers:
                            self.faces_types.append(tokens[1])
                            # tags: physical_entity, elementary_entity, mesh_partition
                            n_tags = tokens[2]
                            face_zone_number = tokens[3]
                            face_zone_i = self.face_zones_numbers.index(face_zone_number)
                            self.face_zones[face_zone_i].append(tokens[0])
                            nodes_start_i = 3 + n_tags
                            self.faces.append(len(tokens[nodes_start_i:]))
                            self.faces.extend(tokens[nodes_start_i:])
                        # If element is 3D
                        elif tokens[1] in self.gmsh_cell_numbers:
                            self.cells_types.append(tokens[1])
                            # tags: physical_entity, elementary_entity, mesh_partition
                            n_tags = tokens[2]
                            cell_zone_number = tokens[3]
                            cell_zone_i = self.cells_zones_numbers.index(cell_zone_number)
                            self.face_zones[cell_zone_i].append(tokens[0])
                            nodes_start_i = 3 + n_tags
                            self.cells.append(len(tokens[nodes_start_i:]))
                            self.cells.extend(tokens[nodes_start_i:])
                        else:
                            raise ValueError('Bad gmsh element number = {} in line {}'.format(tokens[1], i))
                    if not is_mesh_format:
                        sys.stdout.write('\r{:.0f}%'.format(float(lines_ctr - 1) / n_objects * 100))
                        sys.stdout.flush()
