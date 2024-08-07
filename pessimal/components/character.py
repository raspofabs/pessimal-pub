from pessimal.component import Component
from pessimal.field import Field, IntField
from pessimal.v2 import V2
from pessimal.sprite_manager import SpriteManager

import random


class Character(Component):
    fields = [
        Field("variant", None),
        IntField("speed", 40),
        IntField("rseed", None),
    ]

    def __init__(self, parent, config):
        super().__init__(parent, config)

        sm = SpriteManager.get_manager()

        rand_source = random.Random()
        rand_source.seed(self.rseed)

        self.body_variant = rand_source.randint(0, 2)
        self.shoes_variant = rand_source.randint(0, 7)
        self.trousers_variant = rand_source.randint(0, 7)
        if self.shoes_variant > 3:
            self.shoes_variant += 1
        if self.trousers_variant > 3:
            self.trousers_variant += 1
        self.torso_variant = rand_source.randint(6, 17), rand_source.randint(0, 9)
        self.hair_colour = rand_source.randint(0, 1) * 4, rand_source.randint(0, 2) * 4
        self.hair_variant1 = (
            19 + rand_source.randint(0, 3) + self.hair_colour[0],
            rand_source.randint(0, 3) + self.hair_colour[1],
        )
        self.hair_variant2 = (
            19 + rand_source.randint(0, 3) + self.hair_colour[0],
            rand_source.randint(0, 3) + self.hair_colour[1],
        )

        self.body = sm.get_sprite(f"character:0,{self.body_variant}")
        self.trousers = sm.get_sprite(f"character:3,{self.shoes_variant}")
        self.shoes = sm.get_sprite(f"character:4,{self.shoes_variant}")
        self.torso = sm.get_sprite(f"character:{self.torso_variant}")
        self.hair1 = sm.get_sprite(f"character:{self.hair_variant1}")
        self.hair2 = sm.get_sprite(f"character:{self.hair_variant2}")

        tool_sprite_id = self.get_tool_sprite_id(self.variant)
        self.tool = sm.get_sprite_or_none(tool_sprite_id)

        # dynamics
        self.destination = None
        self.dir = None

        self.debug_arrows = []

    @staticmethod
    def get_tool_sprite_id(variant):
        if variant == "axe":
            return "character:47,1"
        if variant == "pick":
            return "character:50,1"
        return None

    def go_to(self, destination):
        # print(f"Setting destination {destination}")
        self.destination = destination

    def update(self, dt):
        self.debug_arrows = []
        if self.destination is None:
            return

        speed = self.speed * dt
        diff = self.destination - self.parent.pos
        if diff.mag() > speed:
            # print(f"moving toward {self.destination} by {speed}")
            self.parent.pos += diff.normal() * speed
        else:
            # print(f"arriving at {self.destination}")
            self.parent.pos = self.destination
            self.destination = None

        road_networks = self.get_world().find_entities_by_component("RoadNetwork")
        for road_network_entity in road_networks:
            road_network = road_network_entity.get_component("RoadNetwork")
            best_road, best_road_pos = road_network.get_closest_road(self.parent.pos)
            self.debug_arrows.append(best_road_pos)

    def render(self, engine):
        if not engine.should_render(self.parent.pos):
            return

        # body
        engine.render_sprite(self.body, self.parent.pos)
        engine.render_sprite(self.trousers, self.parent.pos)
        engine.render_sprite(self.shoes, self.parent.pos)
        engine.render_sprite(self.torso, self.parent.pos)
        engine.render_sprite(self.hair1, self.parent.pos)
        engine.render_sprite(self.hair2, self.parent.pos)
        if self.tool:
            engine.render_sprite(self.tool, self.parent.pos)

        engine.render_text(f"{self.parent.name}", self.parent.pos)
        for debug_arrow in self.debug_arrows:
            engine.render_line(self.parent.pos, debug_arrow, (200, 200, 20))
