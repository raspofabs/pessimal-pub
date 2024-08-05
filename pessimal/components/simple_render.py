from ast import literal_eval
from pessimal.component import Component
from pessimal.field import LiteralField

class SimpleRender(Component):
    fields = [
            LiteralField("colour", "50, 120, 220"),
            ]

    def __init__(self, parent, config):
        super().__init__(parent, config)
        #self.colour = literal_eval(config.get("colour", "50, 120, 220"))

    def render(self, engine):
        if not engine.should_render(self.parent.pos):
            return
        rect_size = self.parent.get_size()
        engine.render_rect(self.parent.pos - rect_size, self.parent.pos + rect_size, self.colour)
        darker = tuple(map(lambda x: int(x * 0.7), self.colour))
        engine.render_circle(self.parent.pos, rect_size * 0.8, darker)
