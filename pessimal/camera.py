from pessimal.v2 import V2

class Camera2D:
    def __init__(self, *, display_size: V2 = None):
        self.display_size = display_size or V2(100,100)
        self.scale = 1.0
        self.centre_on(V2(0,0))

    def set_display(self, display_size: V2):
        self.display_size = V2(display_size)

    def centre_on(self, pos: V2, scale: float = 1.0):
        self.scale = scale
        self.top_left = pos + self.display_size * (-0.5 / scale)

    def pos_to_screen(self, pos: V2) -> V2:
        rel = (pos - self.top_left) * self.scale
        return rel

    def size_to_screen(self, size: V2) -> V2:
        return size * self.scale


