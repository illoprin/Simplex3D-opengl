from src.settings import *
from src.shader_program import ShaderManager

class PointLight:
    def __init__(self, position=(0, 0, 0), color=(1, 1, 1), radius=5.3, specular=10, intensity=1):
        self.attributes = {
            "type": "point_lights",
            "PL_position": glm.vec3(position),
            "PL_color": glm.vec3(color),
            "PL_specular": specular,
            "PL_radius": radius,
            "PL_intensity": intensity,
        }

    def set_position(self, new_position: tuple[float, float, float]):
        self.attributes["PL_position"] = glm.vec3(new_position)

    def set_color(self, new_color: tuple[float, float, float]):
        self.attributes["PL_position"] = glm.vec3(new_color)
