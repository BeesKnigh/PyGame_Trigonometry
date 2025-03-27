import math
import pygame
from settings import GRAVITY, GROUND_Y, RESTITUTION, LAUNCH_FACTOR

class Bird:
    def __init__(self, start_pos, radius, color):
        self.start_pos = start_pos
        self.pos = list(start_pos)
        self.radius = radius
        self.color = color
        self.launch_factor = LAUNCH_FACTOR
        self.dragging = False
        self.launched = False
        self.vx = 0
        self.vy = 0

    def reset(self):
        self.pos = list(self.start_pos)
        self.vx = 0
        self.vy = 0
        self.launched = False
        self.dragging = False

    def launch(self, mouse_pos):
        # Расчет направления и силы запуска на основе позиции мыши
        dx = self.start_pos[0] - mouse_pos[0]
        dy = self.start_pos[1] - mouse_pos[1]
        angle = math.atan2(dy, dx)
        power = math.hypot(dx, dy) * self.launch_factor
        self.vx = power * math.cos(angle)
        self.vy = power * math.sin(angle)
        self.launched = True

    def update(self, dt):
        if self.launched:
            self.pos[0] += self.vx * dt
            self.pos[1] += self.vy * dt
            self.vy += GRAVITY * dt
            # Столкновение с землей
            if self.pos[1] >= GROUND_Y - self.radius:
                self.pos[1] = GROUND_Y - self.radius
                self.vy = -self.vy * RESTITUTION
                self.vx *= 0.9
                if abs(self.vy) < 10:
                    self.vy = 0
                if abs(self.vx) < 10:
                    self.vx = 0

    def draw(self, screen, offset=(0, 0)):
        # Отрисовка с учетом смещения камеры
        pos_on_screen = (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]))
        pygame.draw.circle(screen, self.color, pos_on_screen, self.radius)
