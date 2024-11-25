from src.settings import *
from src.player.camera import Camera

class Player(Camera):
    def __init__(self, app, program: mgl.Program, position = (0, 0, 0), rotation=glm.vec2(0, -90)):
        super().__init__(program)
        self.position = glm.vec3(position)
        self.pitch = glm.radians(rotation.x)
        self.yaw = glm.radians(rotation.y)

        self.app = app
        self.wnd = app.wnd
        self.states = {
            self.wnd.keys.W: False,  # forward
            self.wnd.keys.S: False,  # backwards
            self.wnd.keys.A: False,  # left
            self.wnd.keys.D: False,  # right
            self.wnd.keys.Q: False,  # up
            self.wnd.keys.E: False,  # down
            self.wnd.keys.Z: False,  # zoom in
            self.wnd.keys.X: False,  # zoom out
        }

        self.velocity = PLAYER_SPEED
        self.update()

    def move(self, frame_time=1):
        self.velocity *= frame_time
        if self.states.get(self.wnd.keys.W):
            self.move_forward(self.velocity)
        if self.states.get(self.wnd.keys.S):
            self.move_backward(self.velocity)
        if self.states.get(self.wnd.keys.A):
            self.move_left(self.velocity)
        if self.states.get(self.wnd.keys.D):
            self.move_right(self.velocity)
        if self.states.get(self.wnd.keys.Q):
            self.move_up(self.velocity)
        if self.states.get(self.wnd.keys.E):
            self.move_down(self.velocity)

    def handle_speed_modifer(self, action, key):
        if action == self.wnd.keys.ACTION_PRESS:
            if key in self.states:
                self.states[key] = True
            if self.wnd.modifiers.shift:
                self.velocity = PLAYER_SPEED * PLAYER_SPEED_MODIFER
        else:
            if key in self.states:
                self.states[key] = False
            self.velocity = PLAYER_SPEED

    def handle_rotation(self, dx, dy):
        self.rotate_pitch(dy * MOUSE_SENSEVITY)
        self.rotate_yaw(dx * MOUSE_SENSEVITY)
