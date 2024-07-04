from ast import literal_eval
from pessimal.component import Component, Field, IntField


class WorldResource(Component):
    fields = [
            Field("kind", "dirt"),
            IntField("quantity", 10),
            ]

    def __init__(self, parent, config):
        super().__init__(parent, config)
        self.current_quantity = self.quantity

    def __str__(self):
        return f"{self.kind} - {self.current_quantity}/{self.quantity}"
    
    def __repr__(self):
        return str(self)

    def start(self):
        self.current_quantity = self.quantity
