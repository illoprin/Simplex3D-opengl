import glm

from settings import *
from world_objects.game_object import GameObject
from mesh.meshes import *


class Cube(GameObject):
    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0), scl=(1, 1, 1), **attrs):
        super().__init__(pos, rot, scl, *attrs)
        self.mesh = CubeMesh()

class Pyramid(GameObject):
    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0), scl=(1, 1, 1), **attrs):
        super().__init__(pos, rot, scl, *attrs)
        self.mesh = PyramidMesh()


# From OBJ
class Sphere(GameObject):
    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.origin = glm.translate(glm.mat4(), (0, 1, -2.333))
        self.m_model *= self.origin
        self.mesh = SphereMesh()

class Cube_N(GameObject):
    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.m_model *= self.origin
        self.mesh = CubeNMesh()

class Cylinder(GameObject):
    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.mesh = CylinderMesh()

class Cone(GameObject):
    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.origin = glm.translate(glm.mat4(1.0), (0, 0, 2))
        self.m_model *= self.origin
        self.mesh = ConeMesh()



class Plane(GameObject):
    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.origin = glm.translate(glm.mat4(), (-1, -.5, 0))
        self.m_model *= self.origin
        self.mesh = PlaneMesh()

class TestLevel(GameObject):
    def __init__(self, **attrs):
        super().__init__(scl=(2,2,2), **attrs)
        self.origin = glm.translate(glm.mat4(1.0), (-15, -2, 5))
        self.m_model *= self.origin
        self.mesh = LevelMesh()


