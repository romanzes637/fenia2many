import os
import shutil


class ObjMesh:
    """OBJ mesh representation

    https://en.wikipedia.org/wiki/Wavefront_.obj_file
    """

    def __init__(self):
        self.mesh_dirname = 'Obj'
        self.name = 'mesh'
        self.ext = '.obj'
        self.vertices = []  # Format: [X1, Y1, Z1, X2, Y2, Z2, ..., XN, YN, ZN]
        self.texture_vertices = []  # Format: [X1, Y1, Z1, X2, Y2, Z2, ..., XN, YN, ZN]
        self.vertex_normals = []  # Format: [X1, Y1, Z1, X2, Y2, Z2, ..., XN, YN, ZN]
        self.points = []
        self.lines = []
        self.faces = []  # Format: 2D Array [[V1, V2, ..., VN], ...]
        self.face_zones = []  # Format: 2D Array [[F1, F2, ..., FN], ...]
        self.face_zones_names = []
        self.is_write_texture_vertices = False

    # Remove volume vertices from mesh (not removing volume faces)
    def remove_volume_vertices(self):
        print("Removing volume vertices")
        print("Creating map arrays")
        new_to_old_map = {}
        old_to_new_map = {}
        n_new_vertices = 0
        for face_zone in self.face_zones:
            for face_index in face_zone:
                for vertex_index in self.faces[face_index]:
                    if vertex_index not in old_to_new_map:
                        old_to_new_map[vertex_index] = n_new_vertices
                        new_to_old_map[n_new_vertices] = vertex_index
                        n_new_vertices += 1

        print("Removing volume vertices from vertices")
        new_vertices = []
        for new_vertex_index in range(n_new_vertices):
            old_vertex_index = new_to_old_map.get(new_vertex_index)
            new_vertices.extend(self.vertices[old_vertex_index*3:old_vertex_index*3 + 3])
        self.vertices = new_vertices

        print("Reindexing vertices in faces")
        for face_vertices in self.faces:
            for i, vertex_index in enumerate(face_vertices):
                new_vertex_index = old_to_new_map.get(vertex_index)
                if new_vertex_index is not None:
                    face_vertices[i] = new_vertex_index
        return new_to_old_map

    def write(self):
        if not os.path.isdir(self.mesh_dirname):
            os.makedirs(self.mesh_dirname)

        with open(os.path.join(self.mesh_dirname, self.name + self.ext), 'w') as f:
            f.write('# {}\n'.format(os.path.join(self.mesh_dirname, self.name + self.ext)))

            # Write vertices
            for i in range(0, len(self.vertices), 3):
                vertex = 'v '
                coordinates = ' '.join(map(str, self.vertices[i:i + 3]))
                vertex += coordinates
                vertex += '\n'
                f.write(vertex)
            f.write('\n')

            # Write texture vertices
            if self.is_write_texture_vertices:
                for i in range(0, len(self.texture_vertices), 2):
                    vertex = 'vt '
                    coordinates = ' '.join(map(str, self.texture_vertices[i:i + 2]))
                    vertex += coordinates
                    vertex += '\n'
                    f.write(vertex)
                f.write('\n')

            # Write faces
            for i, face_zone in enumerate(self.face_zones):
                f.write('g {}\n'.format(self.face_zones_names[i]))
                for face_index in face_zone:
                    face_vertices = self.faces[face_index]
                    face = 'f '
                    for j, vertex_index in enumerate(face_vertices):
                        if self.is_write_texture_vertices:
                            # Add + 1 to vertex index, because obj vertices numbering starts from 1
                            face += '{}/{}'.format(vertex_index + 1, j + 1)
                        else:
                            # Add + 1 to vertex index, because obj vertices numbering starts from 1
                            face += '{}'.format(vertex_index + 1)
                        if not j == len(face_vertices) - 1:
                            face += ' '
                    face += '\n'
                    f.write(face)
                f.write('\n')

    def read(self):
        pass

    def clear(self):
        if os.path.isdir(os.path.join(self.mesh_dirname)):
            shutil.rmtree(os.path.join(self.mesh_dirname))
