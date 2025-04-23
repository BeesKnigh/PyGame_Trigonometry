import pygame
import os
from settings import GRAVITY, GROUND_Y, RESTITUTION

class Pig:
    def __init__(self, pos, radius, color, image_path=None, size_multiplier=5.0):
        self.pos = list(pos)
        self.radius = radius
        self.alive = True
        self.color = color
        self.vy = 0
        self.size_multiplier = size_multiplier
        
        if image_path is None:
            image_path = os.path.join("design_assets", "game_assets", "items", "cucumber.png")
        
        possible_paths = [
            image_path,
            os.path.join(os.path.dirname(__file__), image_path),
            os.path.join(os.path.dirname(__file__), "..", image_path)
        ]
        
        self.image = None
        
        for path in possible_paths:
            try:
                original_image = pygame.image.load(path).convert_alpha()
                new_size = int(2 * self.radius * self.size_multiplier)
                self.image = pygame.transform.smoothscale(
                    original_image, 
                    (new_size, new_size)
                )
                print(f"Изображение свиньи загружено: {path}")
                break
            except pygame.error as e:
                print(f"Ошибка загрузки {path}: {e}")
                continue
        
        if self.image is None:
            print("Не удалось загрузить изображение, будет использован простой круг")

    def reset(self):
        self.alive = True
        self.vy = 0

    def update(self, dt):
        if not self.alive:
            return
            
        if self.pos[1] < GROUND_Y - self.radius:
            self.vy += GRAVITY * dt
            self.pos[1] += self.vy * dt
        else:
            self.pos[1] = GROUND_Y - self.radius
            self.vy = -self.vy * RESTITUTION
            
            if abs(self.vy) < 1:
                self.vy = 0

    def draw(self, screen, offset=(0, 0)):
        if not self.alive:
            return
            
        pos_on_screen = (
            int(self.pos[0] - offset[0]), 
            int(self.pos[1] - offset[1])
        )

        if self.image:
            img_rect = self.image.get_rect(center=pos_on_screen)
            screen.blit(self.image, img_rect)
        else:
            pygame.draw.circle(
                screen, 
                self.color, 
                pos_on_screen, 
                int(self.radius * self.size_multiplier)
            )
            
            eye_pos1 = (
                pos_on_screen[0] - int(self.radius * 0.3 * self.size_multiplier),
                pos_on_screen[1] - int(self.radius * 0.2 * self.size_multiplier)
            )
            eye_pos2 = (
                pos_on_screen[0] + int(self.radius * 0.3 * self.size_multiplier),
                pos_on_screen[1] - int(self.radius * 0.2 * self.size_multiplier)
            )
            
            pygame.draw.circle(screen, (255, 255, 255), eye_pos1, int(self.radius * 0.2))
            pygame.draw.circle(screen, (255, 255, 255), eye_pos2, int(self.radius * 0.2))
