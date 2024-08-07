from pessimal.component import Component
from pessimal.field import Field
from pessimal.v2 import V2
from pessimal.sprite_manager import SpriteManager


class SpriteRender(Component):
    fields = [
        Field("sprite_id", None),
    ]

    def __init__(self, parent, config):
        super().__init__(parent, config)

        self.sprite = None  # lazy load in case we don't need to render

    def render(self, engine):
        if not engine.should_render(self.parent.pos):
            return
        if self.sprite is None and self.sprite_id:
            self.sprite = SpriteManager.get_manager().get_sprite(self.sprite_id)

        if self.sprite is not None:
            engine.render_sprite(self.sprite, self.parent.pos)
