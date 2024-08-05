from pessimal.engine import Engine
import pytest
import os
import sys
import pygame


class MockEngine:
    def __init__(self, config_override: dict = None):
        self.config = config_override or {} 
        pygame.display.init()
        self.screen = pygame.display.set_mode((1,1))
        self.reset()

    def __del__(self):
        self.screen = None
        pygame.quit()

    def reset(self):
        self.depdendents = []
        self.num_sprites = 0
        self.num_texts = 0
        self.num_lines = 0
        self.num_rects = 0
        self.num_circles = 0

    def add_dependent(self, dependent):
        self.depdendents.append(dependent)
        pass

    def toggle_culling(self):
        self.config["should_render"] = not self.should_render(None)

    def should_render(self, position):
        return self.config.get("should_render", True)

    def render_sprite(self, sprite, position):
        self.num_sprites += 1

    def render_text(self, text, position):
        self.num_texts += 1

    def render_line(self, start, end, colour):
        self.num_lines += 1

    def render_rect(self, top_left, bottom_right, colour):
        self.num_rects += 1

    def render_circle(self, centre, radius, colour):
        self.num_circles += 1


@pytest.fixture
def f_mock_engine(monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    return MockEngine()
