import math
import pygame
import os
from settings import GRAVITY, GROUND_Y, RESTITUTION, LAUNCH_FACTOR

class Bird:
    def __init__(self, start_pos, radius, color, image_path="../eva.png", fly_image_path="../eva_fly.png", size_multiplier=5.0):
        self.start_pos = start_pos
        self.pos = list(start_pos)
        self.radius = radius
        self.color = color
        self.launch_factor = LAUNCH_FACTOR
        self.dragging = False
        self.launched = False
        self.vx = 0
        self.vy = 0
        self.size_multiplier = size_multiplier

        base_size = int(2 * self.radius)
        new_width = int(base_size * self.size_multiplier)
        new_height = int(base_size * self.size_multiplier)

        try:
            full_path_idle = os.path.join(os.path.dirname(__file__), image_path)
            full_path_fly = os.path.join(os.path.dirname(__file__), fly_image_path)

            original_image = pygame.image.load(full_path_idle).convert_alpha()
            fly_image = pygame.image.load(full_path_fly).convert_alpha()

            self.image_idle = pygame.transform.smoothscale(original_image, (new_width, new_height))
            self.image_flying = pygame.transform.smoothscale(fly_image, (new_width, new_height))
            self.image = self.image_idle

            print(f"Изображения загружены: {full_path_idle} и {full_path_fly}")
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image_idle = None
            self.image_flying = None
            self.image = None

    def reset(self):
        self.pos = list(self.start_pos)
        self.vx = 0
        self.vy = 0
        self.launched = False
        self.dragging = False

    def launch(self, mouse_pos):
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

            if self.pos[1] >= GROUND_Y - self.radius:
                self.pos[1] = GROUND_Y - self.radius
                self.vy = -self.vy * RESTITUTION
                self.vx *= 0.9
                if abs(self.vy) < 10:
                    self.vy = 0
                if abs(self.vx) < 10:
                    self.vx = 0

    def draw(self, screen, offset=(0, 0)):
        pos_on_screen = (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]))
        self.image = self.image_flying if self.launched else self.image_idle

        if self.image:
            img_rect = self.image.get_rect(center=pos_on_screen)

            if self.launched and (self.vx != 0 or self.vy != 0):
                angle = math.degrees(math.atan2(-self.vy, self.vx)) - 90
                rotated_img = pygame.transform.rotate(self.image, angle)
                img_rect = rotated_img.get_rect(center=pos_on_screen)
                screen.blit(rotated_img, img_rect)
            else:
                screen.blit(self.image, img_rect)
        else:
            pygame.draw.circle(screen, self.color, pos_on_screen, self.radius)
