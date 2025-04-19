import pygame
import random

class Obstacle:
    def __init__(self, rect, health=100, color=None):
        self.rect = pygame.Rect(rect)
        self.health = health
        # Гарантируем, что цвет будет валидным
        self.color = self._validate_color(color) if color else self._generate_random_color()
        self.texture = self._create_texture()
    
    def _validate_color(self, color):
        """Проверяет и корректирует значения цвета"""
        return (
            max(0, min(255, color[0])),
            max(0, min(255, color[1])),
            max(0, min(255, color[2]))
        )
    
    def _generate_random_color(self):
        """Генерирует случайный коричневый цвет с проверкой диапазона"""
        return (
            random.randint(120, 160),  # R
            random.randint(50, 80),    # G
            random.randint(10, 30)     # B
        )
    
    def _create_texture(self):
        """Создает текстуру для препятствия с защитой от ошибок"""
        try:
            texture = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            texture.fill(self.color)
            
            if self.rect.width > 10 and self.rect.height > 10:
                brick_width = max(10, self.rect.width // 4)
                brick_height = max(10, self.rect.height // 8)
                
                darker_color = (
                    max(0, self.color[0]-20),
                    max(0, self.color[1]-20),
                    max(0, self.color[2]-20)
                )
                
                for row in range(8):
                    for col in range(5):
                        offset = brick_width // 2 if row % 2 else 0
                        pos_x = col * brick_width + offset
                        pos_y = row * brick_height
                        
                        if (pos_x < self.rect.width and pos_y < self.rect.height and
                            brick_width > 2 and brick_height > 2):
                            pygame.draw.rect(
                                texture,
                                darker_color,
                                (
                                    pos_x, 
                                    pos_y, 
                                    min(brick_width-2, self.rect.width-pos_x-1), 
                                    min(brick_height-2, self.rect.height-pos_y-1)
                                )
                            )
            return texture
        except Exception as e:
            print(f"Ошибка создания текстуры: {e}")
            # Возвращаем простую поверхность в случае ошибки
            texture = pygame.Surface((self.rect.width, self.rect.height))
            texture.fill((139, 69, 19))  # Стандартный коричневый
            return texture

    def is_destroyed(self):
        """Проверяет, разрушено ли препятствие"""
        return self.health <= 0

    def draw(self, screen, offset=(0, 0)):
        """Отрисовка препятствия на экране с учетом смещения"""
        pos = (self.rect.x - offset[0], self.rect.y - offset[1])
        screen.blit(self.texture, pos)
        pygame.draw.rect(screen, (0, 0, 0), (*pos, self.rect.width, self.rect.height), 2)
        
        if self.health < 100:
            health_width = max(5, (self.rect.width * self.health) // 100)
            health_color = (
                min(255, 255 * (100 - self.health) // 100),
                min(255, 255 * self.health // 100),
                0
            )
            pygame.draw.rect(screen, health_color, (pos[0], pos[1] - 8, health_width, 5))
