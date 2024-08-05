from pessimal.v2 import V2

class Camera2D:
    def __init__(self, *, display_size: V2 = None):
        self.display_size = display_size or V2(100,100)
        self.scale = 1.0
        self.centre_on(V2(0,0))

    def set_display(self, display_size: V2):
        # find old pos
        pos = self.top_left - self.display_size * (-0.5 / self.scale)
        # set members
        self.display_size = display_size
        self.top_left = pos + self.display_size * (-0.5 / self.scale)

    def centre_on(self, pos: V2, scale: float = 1.0):
        self.scale = scale
        self.top_left = pos + self.display_size * (-0.5 / scale)

    def pos_to_screen(self, pos: V2) -> V2:
        return (pos - self.top_left) * self.scale

    def screen_to_pos(self, screen_pos: V2) -> V2:
        return screen_pos * (1.0 / self.scale) + self.top_left

    def size_to_screen(self, size: V2) -> V2:
        return size * self.scale

    def screen_to_size(self, size: V2) -> V2:
        return size / self.scale
