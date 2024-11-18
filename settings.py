import math
import glm
import moderngl as mgl
import moderngl_window as mglw
import numpy as np
import pyrr

# base vectors
FORWARD = glm.vec3(0, 0, 1)
BACKWARD = glm.vec3(0, 0, -1)
RIGHT = glm.vec3(1, 0, 0)
UP = glm.vec3(0, 1, 0)
DOWN = glm.vec3(0, -1, 0)
LEFT = glm.vec3(-1, 0, 0)
RIGHT = glm.vec3(1, 0, 0)

# player
PLAYER_SPEED = 0.1
PLAYER_SPEED_MODIFER = 2
MOUSE_SENSEVITY = 0.003

# window
WIN_RES = glm.vec2(1280, 720)
ASPECT = WIN_RES.x / WIN_RES.y
BASE_TITLE = "Simplex Engine"
FPS = 60

# opengl
OPENGL_STATEMENTS = mgl.DEPTH_TEST | mgl.BLEND | mgl.CULL_FACE
CLEAR_COLOR = (0.1, 0.1, 0.1)

# camera
FOV_DEG = 90
V_FOV = glm.radians(FOV_DEG)
H_FOV = 2 * math.tan(math.atan(V_FOV / 2) * ASPECT)
NEAR_CLIP = 0.1
FAR_CLIP = 1000.0
MAX_PITCH = math.pi / 2