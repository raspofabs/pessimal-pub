from pessimal.component import Component
from pessimal.field import Field, IntField, V2Field
from pessimal.v2 import V2


class Orbiter(Component):
    fields = [
            V2Field("centre", V2(0,0)),
            IntField("radius", 10, config={"min":1, "max": 300}),
            IntField("speed", 10, config={"min":0, "max":10, "slider":(0, 10)}),
            ]

    def __init__(self, parent, config):
        super().__init__(parent, config)
        self.dir = V2(0, 0)


    def update(self, dt):
        parent_dist = self.parent.pos - self.centre
        dist_to_parent = parent_dist.mag()
        if dist_to_parent == 0.0:
            parent_dist = V2(self.radius, 0.0)
            dist_to_parent = self.radius
            self.parent.pos = self.centre + parent_dist

        parent_dist_adjust = self.radius / dist_to_parent - 1.0

        self.dir = parent_dist.rot90() * 0.005 * self.speed + (parent_dist * parent_dist_adjust) * 0.01
        #self.dir + some fix
        self.parent.pos += self.dir
        pass


