import pygame
from settings import GRAVITY, GROUND_Y, RESTITUTION

class Pig:
    def __init__(self, pos, radius, color):
        # Преобразуем координаты в список, чтобы можно было изменять позицию
        self.pos = list(pos)
        self.radius = radius
        self.alive = True
        self.color = color
        self.vy = 0  # Начальная вертикальная скорость

    def reset(self):
        self.alive = True
        self.vy = 0

    def update(self, dt):
        """
        Обновляем положение свиньи, чтобы она реагировала на гравитацию.
        Если свинья не достигла земли, увеличиваем вертикальную скорость и изменяем координату Y.
        Если свинья достигает земли, фиксируем её положение.
        """
        if self.pos[1] < GROUND_Y - self.radius:
            self.vy += GRAVITY * dt
            self.pos[1] += self.vy * dt
        else:
            self.pos[1] = GROUND_Y - self.radius
            # Можно сделать небольшой отскок, если требуется (иначе можно убрать)
            self.vy = -self.vy * RESTITUTION

    def draw(self, screen):
        if self.alive:
            pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)
