import numpy as np

from src.settings import *
from src.mesh.base_mesh import *
from src.mesh.primitives import *

class CubeMesh(BaseMesh):
    name = "mesh.Cube"
    data = {
        'vertices': get_index_based_data(
            CUBE['vertices'], CUBE['indices'], 3, 'f4'
        ),
        'uv': get_index_based_data(
            CUBE['face_uv'], CUBE['tex_coord_indices'], 2, 'u1'
        )
    }
    format_data = '3f 2f'
    attributes = ('in_vertex', 'in_uv')


class PyramidMesh(BaseMesh):
    name = "mesh.Pyramid"
    data = {
        'vertices': get_index_based_data(
            PYRAMID['vertices'], PYRAMID['indices'], 3, 'f4'
        ),
        'uv': get_index_based_data(
            PYRAMID['face_uv'], PYRAMID['tex_coord_indices'], 2, 'f4'
        )
    }
    format_data = '3f 2f'
    attributes = ('in_vertex', 'in_uv')

class SphereMesh(BaseMesh):
    obj = load_from_obj('sphere')
    name = obj['name']
    data = {
        'vertices': obj['vertices'],
        'normal': obj['normal'],
        'uv': obj['uv'],
    }
    format_data = '3f 3f 2f'
    attributes = ('in_vertex', 'in_normal', 'in_uv')

class CubeNMesh(BaseMesh):
    obj = load_from_obj('cube')
    name = obj['name']
    data = {
        'vertices': obj['vertices'],
        'normal': obj['normal'],
        'uv': obj['uv'],
    }
    format_data = '3f 3f 2f'
    attributes = ('in_vertex', 'in_normal', 'in_uv')

class CylinderMesh(BaseMesh):
    obj = load_from_obj('cylinder')
    name = obj['name']
    data = {
        'vertices': obj['vertices'],
        'normal': obj['normal'],
        'uv': obj['uv'],
    }
    format_data = '3f 3f 2f'
    attributes = ('in_vertex', 'in_normal', 'in_uv')

class ConeMesh(BaseMesh):
    obj = load_from_obj('cone')
    name = obj['name']
    data = {
        'vertices': obj['vertices'],
        'normal': obj['normal'],
        'uv': obj['uv'],
    }
    format_data = '3f 3f 2f'
    attributes = ('in_vertex', 'in_normal', 'in_uv')

class PlaneMesh(BaseMesh):
    obj = load_from_obj('plane')
    name = obj['name']
    data = {
        'vertices': obj['vertices'],
        'normal': obj['normal'],
        'uv': obj['uv'],
    }
    format_data = '3f 3f 2f'
    attributes = ('in_vertex', 'in_normal', 'in_uv')

class LevelMesh(BaseMesh):
    obj = load_from_obj('test_level')
    name = obj['name']
    data = {
        'vertices': obj['vertices'],
        'normal': obj['normal'],
        'uv': obj['uv'],
    }
    format_data = '3f 3f 2f'
    attributes = ('in_vertex', 'in_normal', 'in_uv')


# Debug meshes
class AxisMesh(BaseMesh):
    name = "debug.Axis"
    data = {
        'vertices': get_index_based_data(
            AXIS['vertices'], AXIS['indices'], format_size=3, type='uint8'
        ),
        'color': get_index_based_data(
            AXIS['color'], AXIS['color_indices'], format_size=3, type='uint8'
        )
    }
    format_data = '3f 3f'
    attributes = ('in_vertex', 'in_color')