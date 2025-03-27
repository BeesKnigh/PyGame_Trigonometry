import pygame

class Obstacle:
    def __init__(self, rect, health, color):
        self.rect = rect
        self.health = health
        self.color = color

    def is_destroyed(self):
        return self.health <= 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
