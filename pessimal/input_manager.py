import pygame
from pessimal.v2 import V2

class InputManager:
    def __init__(self):
        self.direction = V2(0,0)
        self.zoom_in = False
        self.zoom_out = False
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.quitting = False
        self.reload = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.quitting = True
            if event.key == pygame.K_ESCAPE:
                self.quitting = True
            if event.key == pygame.K_F5:
                self.reload = True

        if event.key == pygame.K_EQUALS:
            self.zoom_in = event.type == pygame.KEYDOWN
        if event.key == pygame.K_MINUS:
            self.zoom_out = event.type == pygame.KEYDOWN
        if event.key == pygame.K_UP:
            self.up = event.type == pygame.KEYDOWN
        if event.key == pygame.K_DOWN:
            self.down = event.type == pygame.KEYDOWN
        if event.key == pygame.K_LEFT:
            self.left = event.type == pygame.KEYDOWN
        if event.key == pygame.K_RIGHT:
            self.right = event.type == pygame.KEYDOWN

        axial = {
                (False, False): 0.0,
                (False, True): 1.0,
                (True, False): -1.0,
                (True, True): 0.0,
                }

        # update interpretation
        self.direction = V2(axial[self.left, self.right], axial[self.up, self.down])

