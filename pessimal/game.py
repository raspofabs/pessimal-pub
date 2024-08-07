import pygame
import yaml
from pessimal.v2 import V2
from pessimal.world import World
from pessimal.input_manager import InputManager
from pessimal.engine import EngineDependent, SystemStatus

import pygame_gui
from enum import Enum

BG_COLOUR = (40, 40, 40)

STATUS_MAP = {
    SystemStatus.EDITING: (40, 175, 200),
    SystemStatus.RUNNING: (100, 200, 40),
    SystemStatus.PAUSED: (220, 70, 60),
}
FG_STATUS = (200, 40, 40)


class Game(EngineDependent):
    def __init__(self, engine, *, config: dict = None):
        super().__init__(engine)
        self.status = engine.status
        self.time_step = 0.01
        self.time_accum = 0.0
        self.config = config or {}
        self.last_loaded_world = None
        self.init_game()

    def get_starting_world(self):
        return self.config.get("start_world", "data/setup.yaml")

    def init_game(self):
        self.world = World()
        self.input = InputManager()

        self.scale = 1.0
        self.pos = V2(0, 0)

        self.last_loaded_world = self.get_starting_world()
        print("Loading setup...")
        with open(self.last_loaded_world) as yaml_fh:
            setup_data = yaml.safe_load(yaml_fh)

        for entity in setup_data.get("entities", []):
            self.world.add_entity(entity)

    def save_config(self):
        print("Serialising...")
        config = {"entities": []}
        self.world.save_out(config)
        print("Writing setup...")
        with open(self.last_loaded_world, "wt") as yaml_fh:
            yaml.dump(config, yaml_fh)
        pass

    def start(self):
        self.world.start()

    def stop(self):
        self.world.stop()

    def update(self, dt):
        self.time_accum += dt

        if self.input.quitting:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        if self.input.reload:
            self.input.reload = False
            self.init_game()
            self.time_accum = self.time_step

        while self.time_accum > self.time_step:
            self.time_accum -= self.time_step
            if self.input.zoom_in:
                self.scale *= 1.01
            if self.input.zoom_out:
                self.scale /= 1.01
            if self.engine.status == SystemStatus.RUNNING:
                self.world.update(self.time_step)
            self.pos += self.input.direction * 1.0

    def process_event(self, event):
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            self.input.handle_event(event)

    def render(self, engine):
        status_text = ""
        engine.clear_screen(BG_COLOUR)

        status_colour = STATUS_MAP[engine.status]

        engine.render_ui_rect((2, 2, 10, 20), status_colour)

        engine.camera.centre_on(self.pos, self.scale)

        mx, my = pygame.mouse.get_pos()
        wx, wy = engine.get_window_pos()
        status_text = status_text + f"M: {mx}, {my} @ {wx}, {wy}"
        status_text = status_text + f" FPS: {engine.get_fps():.1f}"

        engine.render_ui_text(status_text, (14, 2))
        self.world.render(engine)
