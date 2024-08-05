from pessimal.component import Component
from pessimal.field import IntField


class Player(Component):
    fields = [
            IntField("which_player", 0),
            ]

    def __init__(self, parent, config):
        super().__init__(parent, config)

