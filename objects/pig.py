import pygame
from settings import GRAVITY, GROUND_Y, RESTITUTION

class Pig:
    def __init__(self, pos, radius, color):
        self.pos = list(pos)
        self.radius = radius
        self.alive = True
        self.color = color
        self.vy = 0

    def reset(self):
        self.alive = True
        self.vy = 0

    def update(self, dt):
        if self.pos[1] < GROUND_Y - self.radius:
            self.vy += GRAVITY * dt
            self.pos[1] += self.vy * dt
        else:
            self.pos[1] = GROUND_Y - self.radius
            self.vy = -self.vy * RESTITUTION

    def draw(self, screen, offset=(0, 0)):
        if self.alive:
            pos_on_screen = (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]))
            pygame.draw.circle(screen, self.color, pos_on_screen, self.radius)
