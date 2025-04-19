import pygame
import os
from settings import GRAVITY, GROUND_Y, RESTITUTION

class Pig:
    def __init__(self, pos, radius, color, image_path="../cucumber.png", size_multiplier=5.0):  # Увеличил size_multiplier до 5.0
        self.pos = list(pos)
        self.radius = radius
        self.alive = True
        self.color = color
        self.vy = 0
        self.size_multiplier = size_multiplier  # Множитель для увеличения размера

        # Получаем абсолютный путь к изображению
        full_path = os.path.join(os.path.dirname(__file__), image_path)
        
        print(f"Пытаемся загрузить изображение по пути: {full_path}")
        print(f"Файл существует: {os.path.exists(full_path)}")
        
        try:
            # Загружаем изображение
            original_image = pygame.image.load(full_path).convert_alpha()
            
            # Увеличиваем размер изображения (size_multiplier * стандартный размер)
            new_width = int(2 * self.radius * self.size_multiplier)
            new_height = int(2 * self.radius * self.size_multiplier)
            self.image = pygame.transform.smoothscale(original_image, (new_width, new_height))
            
            print(f"Изображение успешно загружено и масштабировано до {new_width}x{new_height}")
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image = None

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
        if not self.alive:
            return

        pos_on_screen = (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]))

        if self.image:
            # Центрируем увеличенное изображение
            img_rect = self.image.get_rect(center=pos_on_screen)
            screen.blit(self.image, img_rect)
        else:
            pygame.draw.circle(screen, self.color, pos_on_screen, self.radius)
