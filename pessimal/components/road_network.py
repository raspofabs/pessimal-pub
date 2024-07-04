from ast import literal_eval
from pessimal.component import Component, DictField, IntField, Field
from pessimal.v2 import V2
from pessimal.sprite_manager import SpriteManager


class RoadSegment:
    def __init__(self, start: V2 = V2(0,0), end: V2 = V2(1,0)):
        self.start = start
        self.end = end
        diff = end - start
        self.length = diff.mag()
        self.dir = diff * (1 / self.length)

    def closest_point(self, pos: V2):
        relative = pos - self.start
        distance = relative.dot(self.dir)
        if distance <= 0.0:
            return self.start
        if distance >= self.length:
            return self.end
        return self.start + self.dir * distance


class RoadNetwork(Component):
    fields = [
            DictField("roads", None),
            ]

    def __init__(self, parent, config):
        super().__init__(parent, config)

        #self.roads = config.get("roads")
        self.road_segments = {}

        sm = SpriteManager.get_manager()
        self.dirtpaths = sm.get_sprite("roguelike:dirtpath_")
        for name, road_segment in self.roads.items():
            sx, sy, ex, ey = literal_eval(road_segment)
            self.road_segments[name] = RoadSegment(V2(sx, sy), V2(ex, ey))

    def get_closest_road(self, pos: V2) -> tuple:
        best = RoadSegment(), V2(0,0)
        best_distance = 1e1000
        for name, segment in self.road_segments.items():
            point_on_segment = segment.closest_point(pos)
            distance = (point_on_segment - pos).mag()
            if distance < best_distance:
                best = (segment, point_on_segment)
                best_distance = distance
        return best

    def get_distance(self, start: V2, end: V2) -> float:
        return 0.0

    def render(self, engine):
        if not engine.should_render(self.parent.pos):
            return

        # door
        for name, road_segment in self.roads.items():
            sx, sy, ex, ey = literal_eval(road_segment)
            engine.render_sprite(self.dirtpaths, self.parent.pos + V2(sx, sy))
            engine.render_sprite(self.dirtpaths, self.parent.pos + V2(ex, ey))
            roadlength = abs(ex-sx) + abs(ey-sy)
            steps = int(roadlength / 16)
            for x in range(steps):
                movement = V2((ex-sx) * x / float(steps), (ey-sy) * x / float(steps))
                engine.render_sprite(self.dirtpaths, self.parent.pos + V2(sx, sy) + movement)

