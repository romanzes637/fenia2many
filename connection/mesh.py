"""Mesh conversions"""


def fenia_to_obj(fm, om, is_triangulate=False):
    om.vertices = fm.points.data
    om.face_zones = fm.face_zones.data
    om.face_zones_names = fm.face_zones.names

    # Converting faces
    faces_vertices = []
    i = 0
    while i != len(fm.faces.data):
        n_vertices = fm.faces.data[i]
        faces_vertices.append(fm.faces.data[i + 1:i + 1 + n_vertices])
        i += n_vertices + 1
    om.faces = faces_vertices

    # Check if all faces are triangles
    is_triangle_faces = True
    for face_vertices in om.faces:
        n_vertices = len(face_vertices)
        if n_vertices != 3:
            is_triangle_faces = False
            break

    if is_triangulate and not is_triangle_faces:
        print("Triangulating faces")
        face_counter = 0
        new_face_counter = 0
        new_faces = []
        new_face_zones = []
        for i in range(len(om.face_zones)):
            new_face_zones.append([])
        for face_vertices in om.faces:
            n_vertices = len(face_vertices)
            if n_vertices == 3:
                new_faces.append(face_vertices)
                new_face_counter += 1
            elif n_vertices == 4:
                tri1_vertices = face_vertices[0:3]
                tri2_vertices = [face_vertices[0]]
                tri2_vertices.extend(face_vertices[2:4])
                new_faces.append(tri1_vertices)
                new_faces.append(tri2_vertices)
                new_face_counter += 2
            for j, face_zone in enumerate(om.face_zones):
                if face_counter in face_zone:
                    if n_vertices == 3:
                        new_face_zones[j].append(new_face_counter - 1)
                    elif n_vertices == 4:
                        new_face_zones[j].extend([new_face_counter - 2, new_face_counter - 1])
            face_counter += 1
        om.faces = new_faces
        om.face_zones = new_face_zones
        is_triangle_faces = True

    # Set texture vertices
    if is_triangle_faces:
        om.texture_vertices = [0.0, 0.0, 1.0, 0.0, 0.0, 1.0]
    else:
        om.texture_vertices = [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0]


def fenia_to_unity(fm, um):
    um.times = map(float, fm.times)
    um.times_fields = fm.times_fields
    um.evaluate_field_names()
    um.evaluate_fields()
    if um.mesh is not None:
        um.remove_volume_vertices()
    um.evaluate_fields_limits()
    um.calculate_fields_velocities()
    um.calculate_relative_fields()
    um.calculate_relative_fields_velocities()