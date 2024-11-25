from src.settings import *
from src.world_objects.game_object import GameObject
from src.mesh.meshes import AxisMesh


# Debug objects
class GizmoAxis(GameObject):
    def __init__(self, m_model):
        super().__init__(m_model=m_model)
        self.mesh = AxisMesh()
        # self.resize((10, 10, 10))