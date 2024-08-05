from pessimal.component import Component
from pessimal.field import Field, IntField
from pessimal.v2 import V2
from pessimal.sprite_manager import SpriteManager


class Building(Component):
    fields = [
            IntField("width", 3),
            IntField("depth", 3),
            IntField("storeys", 1),
            IntField("door_x_pos", 1),
            Field("name", "abode"),
            ]

    def __init__(self, parent, config):
        super().__init__(parent, config)

        assert self.width > 1

        sm = SpriteManager.get_manager()
        self.wall_bl = sm.get_sprite("roguelike:building_bottom_left")
        self.wall_bm = sm.get_sprite("roguelike:building_bottom")
        self.wall_br = sm.get_sprite("roguelike:building_bottom_right")
        self.wall_ml = sm.get_sprite("roguelike:building_mid_left")
        self.wall_mm = sm.get_sprite("roguelike:building_mid_mid")
        self.wall_mr = sm.get_sprite("roguelike:building_mid_right")
        self.roof_fl = sm.get_sprite("roguelike:roof45_left_far")
        self.roof_fm = sm.get_sprite("roguelike:roof0_mid_far")
        self.roof_fr = sm.get_sprite("roguelike:roof45_right_far")
        self.roof_ml = sm.get_sprite("roguelike:roof45_left_mid")
        self.roof_mm = sm.get_sprite("roguelike:roof0_mid_mid")
        self.roof_mr = sm.get_sprite("roguelike:roof45_right_mid")
        self.roof_nl = sm.get_sprite("roguelike:roof45_left_near")
        self.roof_nm = sm.get_sprite("roguelike:roof0_mid_near")
        self.roof_nr = sm.get_sprite("roguelike:roof45_right_near")
        self.door = sm.get_sprite("roguelike:door")

    def get_door_pos(self):
        return self.parent.pos + V2(16 * self.door_x_pos, 0)

    def render(self, engine):
        if not engine.should_render(self.parent.pos):
            return

        # base
        engine.render_sprite(self.wall_bl, self.parent.pos)
        for x in range(self.width - 2):
            engine.render_sprite(self.wall_bm, self.parent.pos + V2(16*(1+x),0))
        engine.render_sprite(self.wall_br, self.parent.pos + V2(16*(self.width-1),0))

        # wall
        for storey in range(self.storeys):
            startpos = self.parent.pos + V2(0, -16*(1+storey))
            engine.render_sprite(self.wall_ml, startpos)
            for x in range(self.width - 2):
                engine.render_sprite(self.wall_mm, startpos + V2(16*(1+x),0))
            engine.render_sprite(self.wall_mr, startpos + V2(16*(self.width-1),0))

        # roof
        roof_startpos = self.parent.pos + V2(0, -16*(self.storeys))
        engine.render_sprite(self.roof_nl, roof_startpos)
        for x in range(self.width - 2):
            engine.render_sprite(self.roof_nm, roof_startpos + V2(16*(1+x),0))
        engine.render_sprite(self.roof_nr, roof_startpos + V2(16*(self.width-1),0))

        for roof in range(self.depth-2):
            roof_startpos = self.parent.pos + V2(0, -16*(1+self.storeys+roof))
            engine.render_sprite(self.roof_ml, roof_startpos)
            for x in range(self.width - 2):
                engine.render_sprite(self.roof_mm, roof_startpos + V2(16*(1+x),0))
            engine.render_sprite(self.roof_mr, roof_startpos + V2(16*(self.width-1),0))

        roof_startpos = self.parent.pos + V2(0, -16*(self.storeys+self.depth-1))
        engine.render_sprite(self.roof_fl, roof_startpos)
        for x in range(self.width - 2):
            engine.render_sprite(self.roof_fm, roof_startpos + V2(16*(1+x),0))
        engine.render_sprite(self.roof_fr, roof_startpos + V2(16*(self.width-1),0))

        # door
        engine.render_sprite(self.door, self.parent.pos + V2(16 * self.door_x_pos, 0))

        engine.render_text(f"{self.parent.name}", self.parent.pos)




