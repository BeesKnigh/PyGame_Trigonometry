import pygame
import random
import os
from settings import IMAGE_PATHS

class Obstacle:
    def __init__(self, rect, health=100, color=None, texture_path=None):
        self.rect = pygame.Rect(rect)
        self.health = health
        self.color = self._validate_color(color) if color else self._generate_random_color()
        self.texture = self._create_texture()

    def _validate_color(self, color):
        return (
            max(0, min(255, color[0])),
            max(0, min(255, color[1])),
            max(0, min(255, color[2]))
        )
    
    def _generate_random_color(self):
        return (
            random.randint(120, 160),
            random.randint(50, 80),
            random.randint(10, 30))
    
    def _create_texture(self):
        try:
            texture = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            texture.fill(self.color)
            
            if self.rect.width > 20 and self.rect.height > 20:
                brick_w = max(10, self.rect.width // 4)
                brick_h = max(10, self.rect.height // 8)
                
                darker_color = (
                    max(0, self.color[0]-20),
                    max(0, self.color[1]-20),
                    max(0, self.color[2]-20))
                
                for row in range(8):
                    for col in range(5):
                        offset = brick_w // 2 if row % 2 else 0
                        pos_x = col * brick_w + offset
                        pos_y = row * brick_h
                        
                        if pos_x < self.rect.width and pos_y < self.rect.height:
                            pygame.draw.rect(
                                texture,
                                darker_color,
                                (
                                    pos_x, 
                                    pos_y, 
                                    min(brick_w-2, self.rect.width-pos_x-1), 
                                    min(brick_h-2, self.rect.height-pos_y-1)
                                ),
                                0
                            )
            return texture
        except Exception as e:
            print(f"Ошибка создания текстуры: {e}")
            fallback = pygame.Surface((self.rect.width, self.rect.height))
            fallback.fill((139, 69, 19))
            return fallback

    def is_destroyed(self):
        return self.health <= 0

    def draw(self, screen, offset=(0, 0)):
        pos = (self.rect.x - offset[0], self.rect.y - offset[1])
        
        screen.blit(self.texture, pos)
        
        pygame.draw.rect(
            screen, 
            (0, 0, 0), 
            (*pos, self.rect.width, self.rect.height), 
            2
        )
        
        if self.health < 100:
            health_width = max(5, (self.rect.width * self.health) // 100)
            health_color = (
                min(255, 255 * (100 - self.health) // 50),
                min(255, 255 * self.health // 100),
                0
            )
            pygame.draw.rect(
                screen, 
                health_color, 
                (pos[0], pos[1] - 8, health_width, 5)
            )
