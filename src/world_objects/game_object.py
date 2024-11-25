from src.settings import *
from src.mesh.base_mesh import BaseMesh

class GameObject():
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scl=(1,1,1), m_model=glm.mat4(1.0), texture=0):
        # Mesh
        self.mesh: BaseMesh = None
        # Transform origin
        self.origin = glm.mat4()
        # Model init
        self.m_model = m_model
        # Applying transforms
        self.transform(pos)
        self.rotate(rot)
        self.resize(scl)
        # Write texture
        self.texture: int = texture



    def rotate(self, rotation=(0, 0, 0)):
        pitch, yaw, roll = rotation
        self.m_model = glm.rotate(self.m_model, glm.radians(pitch), (1, 0, 0))
        self.m_model = glm.rotate(self.m_model, glm.radians(yaw), (0, 1, 0))
        self.m_model = glm.rotate(self.m_model, glm.radians(roll), (0, 0, 1))

    def resize(self, scale=(1, 1, 1)):
        self.m_model = glm.scale(self.m_model, scale)

    def transform(self, transform=(0, 0, 0)):
        self.m_model = glm.translate(self.m_model, transform)
