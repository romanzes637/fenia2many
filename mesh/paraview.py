import time
import numpy as np
import sys
import os
import xml.etree.ElementTree as ET
import shutil
import vtk
from vtk.util import numpy_support

from mesh.fenia import FeniaMesh


class ParaViewMesh(FeniaMesh):
    """ParaView PVD mesh representation

    https://www.paraview.org/Wiki/ParaView/Data_formats
    """

    def __init__(self, face_zones_read_type=0):
        FeniaMesh.__init__(self, face_zones_read_type, False)
        self.mesh_dirname = 'ParaView'
        self.vtk_file_ext = '.vtm'
        self.paraview_file_ext = '.pvd'

    map_n_points_to_vtk_face_type_3d = {
        3: vtk.VTK_TRIANGLE,
        4: vtk.VTK_QUAD
    }

    map_n_points_to_vtk_face_type_2d = {
        2: vtk.VTK_LINE
    }

    map_n_points_to_vtk_cell_type_3d = {
        4: vtk.VTK_TETRA,
        8: vtk.VTK_HEXAHEDRON,
        6: vtk.VTK_WEDGE,
        5: vtk.VTK_PYRAMID,
        10: vtk.VTK_QUADRATIC_TETRA,
        13: vtk.VTK_QUADRATIC_PYRAMID,
        15: vtk.VTK_QUADRATIC_WEDGE,
        20: vtk.VTK_QUADRATIC_HEXAHEDRON
    }

    map_n_points_to_vtk_cell_type_2d = {
        3: vtk.VTK_TRIANGLE,
        4: vtk.VTK_QUAD
    }

    @staticmethod
    def time_field_to_vtk_field(time_field):
        if time_field.mode == 0:
            vtk_data = vtk.util.numpy_support.numpy_to_vtk(time_field.data, deep=1, array_type=vtk.VTK_FLOAT)
        else:
            vtk_data = vtk.util.numpy_support.numpy_to_vtk(time_field.data, array_type=vtk.VTK_FLOAT)
            vtk_data.SetNumberOfComponents(time_field.element_size)
        vtk_data.SetName(time_field.name)
        return vtk_data

    def get_vtk_points(self, order):
        if order == 1:
            points = self.points
        else:
            points = self.points2
        if points.mode == 0:
            # Workaround: Add Z-coordinate = 0.0 for ParaView
            if points.is_2d:
                zeros = np.zeros([points.data.shape[0]])
                points.data = np.column_stack((points.data, zeros))
            vtk_data = vtk.util.numpy_support.numpy_to_vtk(points.data, deep=1, array_type=vtk.VTK_FLOAT)
        else:
            if points.is_2d:
                # TODO mode 1 for 2D mesh
                pass
            vtk_data = vtk.util.numpy_support.numpy_to_vtk(points.data, array_type=vtk.VTK_FLOAT)
            vtk_data.SetNumberOfComponents(3)
        return vtk_data

    def get_vtk_cells(self, order=1):
        if order == 1:
            cells = self.cells
        else:
            cells = self.cells2
        if cells.mode == 0:
            vtk_lines = vtk.util.numpy_support.numpy_to_vtkIdTypeArray(cells.lines, deep=1)
            vtk_triangles = vtk.util.numpy_support.numpy_to_vtkIdTypeArray(cells.triangles, deep=1)
            vtk_quads = vtk.util.numpy_support.numpy_to_vtkIdTypeArray(cells.quads, deep=1)
            vtk_tetras = vtk.util.numpy_support.numpy_to_vtkIdTypeArray(cells.tetras, deep=1)
            vtk_hexahedra = vtk.util.numpy_support.numpy_to_vtkIdTypeArray(cells.hexahedra, deep=1)
            vtk_wedges = vtk.util.numpy_support.numpy_to_vtkIdTypeArray(cells.wedges, deep=1)
            vtk_pyramids = vtk.util.numpy_support.numpy_to_vtkIdTypeArray(cells.pyramids, deep=1)
            return vtk_lines, vtk_triangles, vtk_quads, vtk_tetras, vtk_hexahedra, vtk_wedges, vtk_pyramids
        else:
            return vtk.util.numpy_support.numpy_to_vtk(cells.data, array_type=vtk.VTK_ID_TYPE)

    def get_vtk_face_type(self, n_points, is_2d, order):
        if not is_2d:
            return self.map_n_points_to_vtk_face_type_3d[n_points]
        else:
            return self.map_n_points_to_vtk_face_type_2d[n_points]

    def get_face(self, face_id):
        if not self.faces.is_2d:
            x = np.where(face_id == self.faces.triangles_ids)
            if len(x[0]) != 0:
                face = self.faces.triangles[x[0][0]]
                return face
            x = np.where(face_id == self.faces.quads_ids)
            if len(x[0]) != 0:
                face = self.faces.quads[x[0][0]]
                return face
        else:
            x = np.where(face_id == self.faces.lines_ids)
            if len(x[0]) != 0:
                face = self.faces.lines[x[0][0]]
                return face

    def get_vtk_faces(self):
        if self.faces.mode == 0:
            vtk_lines = vtk.util.numpy_support.numpy_to_vtkIdTypeArray(self.faces.lines, deep=1)
            vtk_triangles = vtk.util.numpy_support.numpy_to_vtkIdTypeArray(self.faces.triangles, deep=1)
            vtk_quads = vtk.util.numpy_support.numpy_to_vtkIdTypeArray(self.faces.quads, deep=1)
            return vtk_lines, vtk_triangles, vtk_quads
        else:
            return vtk.util.numpy_support.numpy_to_vtk(self.faces.data, array_type=vtk.VTK_ID_TYPE)

    def get_vtk_faces_types(self):
        vtk_types = list()
        cnt = 0
        for i in range(self.faces.n_faces):
            n_points = self.faces.data[cnt]
            vtk_types.append(self.get_vtk_face_type(n_points, self.faces.is_2d, self.faces.order))
            cnt += self.faces.data[cnt] + 1
        return vtk_types

    def get_vtk_cell_type(self, n_points, is_2d, order):
        if not is_2d:
            return self.map_n_points_to_vtk_cell_type_3d[n_points]
        else:
            return self.map_n_points_to_vtk_cell_type_2d[n_points]

    def get_vtk_cells_types(self, order):
        if order == 1:
            cells = self.cells
        else:
            cells = self.cells2
        vtk_types = list()
        cnt = 0
        for i in range(cells.n_cells):
            n_points = cells.data[cnt]
            vtk_types.append(self.get_vtk_cell_type(n_points, cells.is_2d, cells.order))
            cnt += cells.data[cnt] + 1
        return vtk_types

    def get_cell(self, order, cell_id):
        if order == 1:
            cells = self.cells
        else:
            cells = self.cells2
        if not cells.is_2d:
            x = np.where(cell_id == cells.tetras_ids)
            if len(x[0]) != 0:
                cell = cells.tetras[x[0][0]]
                return cell
            x = np.where(cell_id == cells.hexahedra_ids)
            if len(x[0]) != 0:
                cell = cells.hexahedra[x[0][0]]
                return cell
            x = np.where(cell_id == cells.wedges_ids)
            if len(x[0]) != 0:
                cell = cells.wedges[x[0][0]]
                return cell
            x = np.where(cell_id == cells.pyramids_ids)
            if len(x[0]) != 0:
                cell = cells.pyramids[x[0][0]]
                return cell
        else:
            x = np.where(cell_id == cells.lines_ids)
            if len(x[0]) != 0:
                cell = cells.lines[x[0][0]]
                return cell
            x = np.where(cell_id == cells.triangles_ids)
            if len(x[0]) != 0:
                cell = cells.triangles[x[0][0]]
                return cell
            x = np.where(cell_id == cells.quads_ids)
            if len(x[0]) != 0:
                cell = cells.quads[x[0][0]]
                return cell

    def get_vtk_cell(self, cell):
        n_points = cell[0]
        if not self.is_2d:
            return self.map_n_points_to_vtk_cell_type_3d[n_points]
        else:
            return self.map_n_points_to_vtk_cell_type_2d[n_points]

    def get_vtk_face(self, face):
        n_points = face[0]
        if not self.is_2d:
            return self.map_n_points_to_vtk_face_type_3d[n_points]

        else:
            return self.map_n_points_to_vtk_face_type_2d[n_points]

    # Working
    def write(self, form=0):
        n_files = len(self.times) + 1
        files_cnt = 0
        time_steps_file_names = []
        for i in range(len(self.times)):  # for each time step
            # Multiblock mesh
            multiblock = vtk.vtkMultiBlockDataSet()
            n_cell_blocks = len(self.cell_zones.names)
            n_face_blocks = len(self.face_zones.names)
            if self.cells.n_cells > 0 and self.cells2.n_cells > 0:
                multiblock.SetNumberOfBlocks(n_cell_blocks + n_face_blocks + n_cell_blocks)
            else:
                multiblock.SetNumberOfBlocks(n_cell_blocks + n_face_blocks)
            # Add first order mesh
            if self.cells.n_cells > 0:
                # Whole 1 order cell mesh
                grid = vtk.vtkUnstructuredGrid()
                points = vtk.vtkPoints()
                points.SetData(self.get_vtk_points(order=1))
                grid.SetPoints(points)
                if self.cells.mode == 0:
                    for cell_id in range(self.cells.n_cells):
                        cell = self.cells.get_cell(cell_id)
                        vtk_cell = self.get_vtk_cell(cell)
                        for k in range(1, cell.shape[0]):
                            vtk_cell.GetPointIds().SetId(k - 1, cell[k])
                        grid.InsertNextCell(vtk_cell.GetCellType(), vtk_cell.GetPointIds())
                else:
                    cells = vtk.vtkCellArray()
                    cells.SetCells(self.cells.n_cells, self.get_vtk_cells(order=1))
                    grid.SetCells(self.get_vtk_cells_types(order=1), cells)
                # Add 1 order fields
                for time_field in self.times_fields[i]:
                    if time_field.n_elements == self.points.n_points:
                        grid.GetPointData().AddArray(self.time_field_to_vtk_field(time_field))
                    elif time_field.n_elements == self.cells.n_cells:
                        grid.GetCellData().AddArray(self.time_field_to_vtk_field(time_field))
                # Mesh blocks in accordance with cell zones
                for j in range(n_cell_blocks):
                    cells_ids = vtk.vtkIntArray()
                    for cell_id in self.cell_zones.data[j]:
                        cells_ids.InsertNextTuple1(cell_id)
                    selection = vtk.vtkSelection()
                    extraction = vtk.vtkExtractSelection()
                    nodes = vtk.vtkSelectionNode()
                    nodes.SetFieldType(vtk.vtkSelectionNode.CELL)
                    nodes.SetContentType(vtk.vtkSelectionNode.INDICES)
                    nodes.SetSelectionList(cells_ids)
                    selection.AddNode(nodes)
                    if vtk.VTK_MAJOR_VERSION <= 5:
                        extraction.SetInput(0, grid)
                        extraction.SetInput(1, selection)
                    else:
                        extraction.SetInputData(0, grid)
                        extraction.SetInputData(1, selection)
                    extraction.Update()
                    block = extraction.GetOutput()
                    multiblock.SetBlock(j, block)
                    multiblock.GetMetaData(j).Set(vtk.vtkCompositeDataSet.NAME(), self.cell_zones.names[j])
            # Add second order mesh
            if self.cells2.n_cells > 0:
                # Whole 2 order cell mesh
                grid = vtk.vtkUnstructuredGrid()
                points = vtk.vtkPoints()
                points.SetData(self.get_vtk_points(order=2))
                grid.SetPoints(points)
                if self.cells2.mode == 0:
                    for cell_id in range(self.cells2.n_cells):
                        cell = self.cells2.get_cell(cell_id)
                        vtk_cell = self.get_vtk_cell(cell)
                        for k in range(1, cell.shape[0]):
                            vtk_cell.GetPointIds().SetId(k - 1, cell[k])
                        grid.InsertNextCell(vtk_cell.GetCellType(), vtk_cell.GetPointIds())
                else:
                    cells2 = vtk.vtkCellArray()
                    cells2.SetCells(self.cells2.n_cells, self.get_vtk_cells(order=2))
                    grid.SetCells(self.get_vtk_cells_types(order=2), cells2)
                # Add 2 order fields
                for time_field in self.times_fields[i]:
                    if time_field.n_elements == self.points2.n_points:
                        grid.GetPointData().AddArray(self.time_field_to_vtk_field(time_field))
                    elif time_field.n_elements == self.cells2.n_cells:
                        grid.GetCellData().AddArray(self.time_field_to_vtk_field(time_field))
                # Mesh blocks in accordance with cell zones
                for j in range(n_cell_blocks):
                    cells_ids = vtk.vtkIntArray()
                    for cell_id in self.cell_zones.data[j]:
                        cells_ids.InsertNextTuple1(cell_id)
                    selection = vtk.vtkSelection()
                    extraction = vtk.vtkExtractSelection()
                    nodes = vtk.vtkSelectionNode()
                    nodes.SetFieldType(vtk.vtkSelectionNode.CELL)
                    nodes.SetContentType(vtk.vtkSelectionNode.INDICES)
                    nodes.SetSelectionList(cells_ids)
                    selection.AddNode(nodes)
                    if vtk.VTK_MAJOR_VERSION <= 5:
                        extraction.SetInput(0, grid)
                        extraction.SetInput(1, selection)
                    else:
                        extraction.SetInputData(0, grid)
                        extraction.SetInputData(1, selection)
                    extraction.Update()
                    block = extraction.GetOutput()
                    if self.cells.n_cells > 0:
                        multiblock.SetBlock(j + n_cell_blocks + n_face_blocks, block)
                        multiblock.GetMetaData(j + n_cell_blocks + n_face_blocks).Set(vtk.vtkCompositeDataSet.NAME(),
                                                                                      self.cell_zones.names[j] + '2')
                    else:
                        multiblock.SetBlock(j, block)
                        multiblock.GetMetaData(j).Set(vtk.vtkCompositeDataSet.NAME(), self.cell_zones.names[j] + '2')
            # Whole first order face mesh # TODO second order face mesh?
            face_grid = vtk.vtkUnstructuredGrid()
            points = vtk.vtkPoints()
            if self.cells.n_cells > 0:
                points.SetData(self.get_vtk_points(order=1))
            else:
                points.SetData(self.get_vtk_points(order=2))
            face_grid.SetPoints(points)
            if self.faces.mode == 0:
                for face_id in range(self.faces.n_faces):
                    face = self.faces.get_face(face_id)
                    vtk_face = self.get_vtk_face(face)
                    for k in range(1, face.shape[0]):
                        vtk_face.GetPointIds().SetId(k - 1, face[k])
                    face_grid.InsertNextCell(vtk_face.GetCellType(), vtk_face.GetPointIds())
            else:
                cells = vtk.vtkCellArray()
                cells.SetCells(self.faces.n_faces, self.get_vtk_faces())
                face_grid.SetCells(self.get_vtk_faces_types(), cells)
            # Add 1 order fields
            for time_field in self.times_fields[i]:
                if self.cells.n_cells > 0:
                    if time_field.n_elements == self.points.n_points:
                        face_grid.GetPointData().AddArray(self.time_field_to_vtk_field(time_field))
                else:
                    if time_field.n_elements == self.points2.n_points:
                        face_grid.GetPointData().AddArray(self.time_field_to_vtk_field(time_field))
            # Face blocks in accordance with face zones
            for j in range(n_face_blocks):
                faces_ids = vtk.vtkIntArray()
                for face_id in self.face_zones.data[j]:
                    faces_ids.InsertNextTuple1(face_id)
                selection = vtk.vtkSelection()
                extraction = vtk.vtkExtractSelection()
                nodes = vtk.vtkSelectionNode()
                nodes.SetFieldType(vtk.vtkSelectionNode.CELL)
                nodes.SetContentType(vtk.vtkSelectionNode.INDICES)
                nodes.SetSelectionList(faces_ids)
                selection.AddNode(nodes)
                if vtk.VTK_MAJOR_VERSION <= 5:
                    extraction.SetInput(0, face_grid)
                    extraction.SetInput(1, selection)
                else:
                    extraction.SetInputData(0, face_grid)
                    extraction.SetInputData(1, selection)
                extraction.Update()
                block = extraction.GetOutput()
                multiblock.SetBlock(j + n_cell_blocks, block)
                multiblock.GetMetaData(j + n_cell_blocks).Set(vtk.vtkCompositeDataSet.NAME(), self.face_zones.names[j])
            time_step_file_name = self.times[i] + self.vtk_file_ext
            time_step_path = os.path.join(self.mesh_dirname, time_step_file_name)
            time_steps_file_names.append(os.path.join(time_step_file_name))
            if form == 0:
                writer = vtk.vtkXMLMultiBlockDataWriter()
            else:
                writer = vtk.vtkXMLMultiBlockDataWriter()
                writer.SetDataModeToAscii()
            writer.SetFileName(time_step_path)
            if vtk.VTK_MAJOR_VERSION <= 5:
                writer.SetInput(multiblock)
            else:
                writer.SetInputData(multiblock)
            # start_time = time.time()
            sys.stdout.write('\r{:.0f}% Writing {}'.format(float(files_cnt) / n_files * 100, time_step_path))
            sys.stdout.flush()
            writer.Write()
            files_cnt += 1
            # sys.stdout.write(' Writing time = {} seconds\n'.format(time.time() - start_time))
            # sys.stdout.flush()
        # Write ParaView file
        sys.stdout.write(
            '\r{:.0f}%  Writing {}'.format(float(files_cnt) / n_files * 100, self.name + self.paraview_file_ext))
        sys.stdout.flush()
        d = {}
        d.update({'type': 'Collection'})
        d.update({'version': '0.1'})
        d.update({'byte_order': 'LittleEndian'})
        d.update({'compressor': 'vtkZLibDataCompressor'})
        vtk_file = ET.Element('VTKFile', d)
        collection = ET.SubElement(vtk_file, 'Collection')
        for i in range(len(self.times)):
            d = {}
            d.update({'timestep': self.times[i]})
            d.update({'group': ''})
            d.update({'part': '0'})
            d.update({'file': time_steps_file_names[i]})
            ds = ET.SubElement(collection, 'DataSet', d)
        f = ET.ElementTree(vtk_file)
        f.write(os.path.join(self.mesh_dirname, self.name + self.paraview_file_ext), xml_declaration=True,
                encoding='us-ascii')
        files_cnt += 1
        sys.stdout.write('\r{:.0f}% \n'.format(float(files_cnt) / n_files * 100))
        sys.stdout.flush()

    def clear(self):
        if os.path.isdir(os.path.join(self.mesh_dirname)):
            shutil.rmtree(os.path.join(self.mesh_dirname))
