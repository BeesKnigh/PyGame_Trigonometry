import math
import pygame
import os
from settings import GRAVITY, GROUND_Y, RESTITUTION, LAUNCH_FACTOR, IMAGE_PATHS

class Bird:
    def __init__(self, start_pos, radius, color, image_path=None, fly_image_path=None, size_multiplier=5.0):
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

        # Загрузка изображений
        base_size = int(2 * self.radius)
        new_width = int(base_size * self.size_multiplier)
        new_height = int(base_size * self.size_multiplier)

        self.image_idle = None
        self.image_flying = None
        self.image = None
        
        # Если пути не переданы, используем стандартные
        image_path = image_path or IMAGE_PATHS["bird"]
        fly_image_path = fly_image_path or IMAGE_PATHS["bird_fly"]

        try:
            self.image_idle = self._load_image(image_path, new_width, new_height)
            self.image_flying = self._load_image(fly_image_path, new_width, new_height)
            self.image = self.image_idle
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self._create_fallback_surface(new_width, new_height)

    def _load_image(self, path, width, height):
        """Загружает и масштабирует изображение"""
        try:
            possible_paths = [
                path,
                os.path.join(os.path.dirname(__file__), path),
                os.path.join(os.path.dirname(__file__), "..", path)
            ]
            
            for p in possible_paths:
                try:
                    img = pygame.image.load(p).convert_alpha()
                    return pygame.transform.smoothscale(img, (width, height))
                except pygame.error:
                    continue
            raise FileNotFoundError(f"Не удалось загрузить изображение: {path}")
        except Exception as e:
            raise e

    def _create_fallback_surface(self, width, height):
        """Создает поверхность-заглушку если изображения не загрузились"""
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, 128), (width//2, height//2), width//2)
        self.image_idle = surf
        self.image_flying = surf
        self.image = surf

    def reset(self):
        self.pos = list(self.start_pos)
        self.vx = 0
        self.vy = 0
        self.launched = False
        self.dragging = False
        self.image = self.image_idle

    def launch(self, mouse_pos):
        dx = self.start_pos[0] - mouse_pos[0]
        dy = self.start_pos[1] - mouse_pos[1]
        angle = math.atan2(dy, dx)
        power = math.hypot(dx, dy) * self.launch_factor
        self.vx = power * math.cos(angle)
        self.vy = power * math.sin(angle)
        self.launched = True
        self.image = self.image_flying

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
                    self.image = self.image_idle

    def draw(self, screen, offset=(0, 0)):
        pos_on_screen = (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]))

        if self.image:
            img_rect = self.image.get_rect(center=pos_on_screen)

            if self.launched and (self.vx != 0 or self.vy != 0):
                angle = math.degrees(math.atan2(-self.vy, self.vx)) - 90
                rotated_img = pygame.transform.rotate(self.image, angle)
                img_rect = rotated_img.get_rect(center=pos_on_screen)
                screen.blit(rotated_img, img_rect)
            else:
                screen.blit(self.image, img_rect)