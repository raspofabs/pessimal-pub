import pygame
import yaml
from collections import defaultdict
from ast import literal_eval
from pessimal.thirdparty.spritesheet import spritesheet


class SpriteManager:
    default_manager = None

    def __init__(self):
        SpriteManager.default_manager = self
        with open("data/sprites.yaml") as yaml_fh:
            self.sprite_data = yaml.safe_load(yaml_fh)
        self.defined_spritesheets = defaultdict(dict)
        self.sprite_sheets = {}
        assert self.sprite_data.get("sheets") is not None
        for sheet in self.sprite_data.get("sheets"):
            name = sheet.get("name")
            path = sheet.get("path")
            tilesize_x, tilesize_y = literal_eval(sheet.get("tilesize"))
            padding = int(sheet.get("padding"))
            tiles_x, tiles_y = literal_eval(sheet.get("tiles"))
            sprites = sheet.get("sprites", {})

            # load the image
            sprite_sheet = spritesheet(path)
            self.sprite_sheets[name] = sprite_sheet, tilesize_x, tilesize_y, padding

            # set up sprite dictionary if there are sprites
            for spritename, coords in sprites.items():
                # parse logical location
                lx, ly = literal_eval(coords)

                px = lx * (tilesize_x + padding)
                py = ly * (tilesize_y + padding)
                self.defined_spritesheets[name][spritename] = sprite_sheet.image_at((px, py, tilesize_x, tilesize_y))


    @classmethod
    def get_manager(cls):
        if cls.default_manager is None:
            cls.default_manager = cls()
        return cls.default_manager
    
    def get_sprite_or_none(self, sprite_id):
        if sprite_id is None:
            return None
        return self.get_sprite(sprite_id)

    def get_sprite(self, sprite_id):
        assert sprite_id is not None
        if ":" not in sprite_id:
            return None
        sheetname, spritename = sprite_id.split(":")
        if sheetname not in self.sprite_sheets:
            return None
        sheet = self.defined_spritesheets.get(sheetname, {})
        #assert sheet is not None, f"Sheet is None: {sheetname} : {spritename}"
        sprite = sheet.get(spritename)
        if sprite is None:
            try:
                x, y = literal_eval(spritename)
                sprite_sheet, tilesize_x, tilesize_y, padding = self.sprite_sheets[sheetname]
                px = x * (tilesize_x + padding)
                py = y * (tilesize_y + padding)
                sprite = sprite_sheet.image_at((px, py, tilesize_x, tilesize_y))
                return sprite
            except:
                return None

        assert sprite is not None, f"Sprite is None: {sheetname} : {spritename}"
        return sprite
