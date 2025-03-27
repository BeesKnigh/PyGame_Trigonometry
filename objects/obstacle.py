import pygame

class Obstacle:
    def __init__(self, rect, health, color):
        self.rect = rect
        self.health = health
        self.color = color

    def is_destroyed(self):
        return self.health <= 0

    def draw(self, screen, offset=(0, 0)):
        # Применяем смещение к прямоугольнику препятствия
        rect_with_offset = self.rect.move(-offset[0], -offset[1])
        pygame.draw.rect(screen, self.color, rect_with_offset)
