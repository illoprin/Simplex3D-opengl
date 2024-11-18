from settings import *

class Camera():
    def __init__(self, program):
        self.program = program
        self.position = (0, 0, 0)
        self.yaw = 0
        self.pitch = 0

        self.up = UP
        self.right = RIGHT
        self.forward = FORWARD

        self.projection = glm.perspective(V_FOV, ASPECT, NEAR_CLIP, FAR_CLIP)
        self.program['m_projection'].write(self.projection)


        self.view = glm.mat4()

    def update(self):
        self.update_vectors()
        self.update_matrices()

    def update_matrices(self):
        self.view = glm.lookAt(self.position, self.position + self.forward, self.up)
        self.program['m_view'].write(self.view)

    def update_vectors(self):
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, UP))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def move_forward(self, vel):
        self.position += self.forward * vel

    def move_backward(self, vel):
        self.position -= self.forward * vel

    def move_up(self, vel):
        self.position += self.up * vel

    def move_down(self, vel):
        self.position -= self.up * vel

    def move_left(self, vel):
        self.position -= self.right * vel

    def move_right(self, vel):
        self.position += self.right * vel

    def rotate_pitch(self, angle):
        self.pitch += angle
        self.pitch = glm.clamp(self.pitch, -MAX_PITCH, MAX_PITCH)

    def rotate_yaw(self, angle):
        self.yaw += angle
