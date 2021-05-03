import os
import shutil
import sys


class UnityMesh:
    """Unity mesh representation

    https://docs.unity3d.com/ScriptReference/Mesh.html
    """

    def __init__(self):
        self.mesh = None
        self.mesh_dirname = 'Unity'
        self.fields_velocities_dirname = 'FieldsVelocities'
        self.relative_fields_velocities_dirname = 'RelativeFieldsVelocities'
        self.fields_dirname = 'Fields'
        self.relative_fields_dirname = 'RelativeFields'
        self.times_filename = 'times'
        self.fields_names_filename = 'fields_list'
        self.fields_min_filename = 'fields_min'
        self.fields_max_filename = 'fields_max'
        self.times = []
        self.times_fields = []
        self.fields_names = []
        self.fields = []
        self.fields_element_size = []
        self.fields_min = []
        self.fields_max = []
        self.fields_velocities = []
        self.relative_fields = []
        self.relative_fields_velocities = []

    # Remove volume vertices from mesh and fields
    def remove_volume_vertices(self):
        print("Removing volume vertices from mesh")
        new_to_old_map = self.mesh.remove_volume_vertices()
        print("Removing volume vertices from fields")
        for i, field in enumerate(self.fields):
            print("Field {}".format(self.fields_names[i]))
            n_time_fields = len(field)
            cnt = 0
            field_element_size = self.fields_element_size[i]
            for j, time_field in enumerate(field):
                sys.stdout.write('\r{:.0f}% Time {}'.format(float(cnt) / n_time_fields * 100, self.times[j]))
                new_time_field = []
                element_size = field_element_size[j]
                for new_vertex_index in range(len(new_to_old_map)):
                    old_vertex_index = new_to_old_map.get(new_vertex_index)
                    start_index = old_vertex_index * element_size
                    end_index = start_index + element_size
                    new_time_field.extend(time_field[start_index:end_index])
                self.fields[i][j] = new_time_field
                cnt += 1
            sys.stdout.write('\r{:.0f}% \n'.format(float(cnt) / n_time_fields * 100))
            sys.stdout.flush()

    def evaluate_field_names(self):
        print("Evaluating fields names")
        # TODO Get fields names from the first time step?
        if len(self.times_fields) > 1:
            for time_field in self.times_fields[1]:
                self.fields_names.append(time_field.name)

    def evaluate_fields(self):
        print("Evaluating fields")
        for name in self.fields_names:
            field = []
            field_element_sizes = []
            for i, time_fields in enumerate(self.times_fields):
                for time_field in time_fields:
                    if name == time_field.name:
                        field.append(time_field.data)
                        field_element_sizes.append(time_field.element_size)
            self.fields_element_size.append(field_element_sizes)
            self.fields.append(field)

    def evaluate_fields_limits(self):
        print("Evaluating fields limits")
        for field in self.fields:
            global_min = None
            global_max = None
            for time_field in field:
                time_min = min(time_field)
                time_max = max(time_field)
                if time_min < global_min or global_min is None:
                    global_min = time_min
                if time_max > global_max or global_max is None:
                    global_max = time_max
            self.fields_min.append(global_min)
            self.fields_max.append(global_max)

    def calculate_fields_velocities(self):
        print("Calculating fields velocities")
        for field in self.fields:
            field_velocities = []
            for i in range(1, len(field)):
                time_delta = self.times[i] - self.times[i - 1]
                time_field_velocities = []
                for j in range(len(field[i])):
                    time_field_velocities.append((field[i][j] - field[i - 1][j]) / time_delta)
                field_velocities.append(time_field_velocities)
            self.fields_velocities.append(field_velocities)

    def calculate_relative_fields(self):
        print("Calculating relative fields")
        for i, field in enumerate(self.fields):
            relative_field_data = []
            field_range = self.fields_max[i] - self.fields_min[i]
            for time_step_fd in field:
                relative_time_step_data = [(x - self.fields_min[i]) / field_range for x in time_step_fd]
                relative_field_data.append(relative_time_step_data)
            self.relative_fields.append(relative_field_data)

    def calculate_relative_fields_velocities(self):
        print("Calculating relative fields velocities")
        for i, field in enumerate(self.fields_velocities):
            relative_field_velocities = []
            field_range = self.fields_max[i] - self.fields_min[i]
            for time_step_fv in field:
                relative_time_step_field_velocities = [x * (1 / field_range) for x in time_step_fv]
                relative_field_velocities.append(relative_time_step_field_velocities)
            self.relative_fields_velocities.append(relative_field_velocities)

    def write(self):
        if not os.path.isdir(self.mesh_dirname):
            os.makedirs(self.mesh_dirname)

        if not os.path.isdir(os.path.join(self.mesh_dirname, self.fields_velocities_dirname)):
            os.makedirs(os.path.join(self.mesh_dirname, self.fields_velocities_dirname))
        for i, name in enumerate(self.fields_names):
            with open(os.path.join(self.mesh_dirname, self.fields_velocities_dirname, name), 'w') as f:
                for fv in self.fields_velocities[i]:
                    line = ' '.join(map(str, fv))
                    line += '\n'
                    f.write(line)

        if not os.path.isdir(os.path.join(self.mesh_dirname, self.fields_dirname)):
            os.makedirs(os.path.join(self.mesh_dirname, self.fields_dirname))
        for i, name in enumerate(self.fields_names):
            with open(os.path.join(self.mesh_dirname, self.fields_dirname, name), 'w') as f:
                for fd in self.fields[i]:
                    line = ' '.join(map(str, fd))
                    line += '\n'
                    f.write(line)

        if not os.path.isdir(os.path.join(self.mesh_dirname, self.relative_fields_dirname)):
            os.makedirs(os.path.join(self.mesh_dirname, self.relative_fields_dirname))
        for i, name in enumerate(self.fields_names):
            with open(os.path.join(self.mesh_dirname, self.relative_fields_dirname, name), 'w') as f:
                for rfd in self.relative_fields[i]:
                    line = ' '.join(map(str, rfd))
                    line += '\n'
                    f.write(line)

        if not os.path.isdir(os.path.join(self.mesh_dirname, self.relative_fields_velocities_dirname)):
            os.makedirs(os.path.join(self.mesh_dirname, self.relative_fields_velocities_dirname))
        for i, name in enumerate(self.fields_names):
            with open(os.path.join(self.mesh_dirname, self.relative_fields_velocities_dirname, name), 'w') as f:
                for rfv in self.relative_fields_velocities[i]:
                    line = ' '.join(map(str, rfv))
                    line += '\n'
                    f.write(line)

        with open(os.path.join(self.mesh_dirname, self.times_filename), 'w') as f:
            line = ' '.join(map(str, self.times))
            line += '\n'
            f.write(line)

        with open(os.path.join(self.mesh_dirname, self.fields_names_filename), 'w') as f:
            line = ' '.join(self.fields_names)
            line += '\n'
            f.write(line)

        with open(os.path.join(self.mesh_dirname, self.fields_min_filename), 'w') as f:
            line = ' '.join(map(str, self.fields_min))
            line += '\n'
            f.write(line)

        with open(os.path.join(self.mesh_dirname, self.fields_max_filename), 'w') as f:
            line = ' '.join(map(str, self.fields_max))
            line += '\n'
            f.write(line)

        if self.mesh is not None:
            os.chdir(self.mesh_dirname)
            self.mesh.write()
            os.chdir('..')

    def clear(self):
        if os.path.isdir(os.path.join(self.mesh_dirname)):
            shutil.rmtree(os.path.join(self.mesh_dirname))
