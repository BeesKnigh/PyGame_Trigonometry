import pygame
import math
from settings import (
    WIDTH, HEIGHT, BIRD_RADIUS, START_POS, RED, BROWN, GREEN
)
from objects.bird import Bird
from objects.pig import Pig
from objects.obstacle import Obstacle
from game_modules.camera import Camera

class GameState:
    def __init__(self):
        pygame.display.set_caption("Angry Birds: Модульная версия")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.camera = Camera(follow_margin=200)

        # Списки птиц, свиней, препятствий
        self.birds = [
            Bird(START_POS, BIRD_RADIUS, RED),
            Bird(START_POS, BIRD_RADIUS, (255, 100, 0)),
            Bird(START_POS, BIRD_RADIUS, (200, 0, 0))
        ]
        self.current_bird_index = 0
        self.current_bird = self.birds[self.current_bird_index]

        self.pigs = [
            Pig([1200, 820], 15, GREEN),
            Pig([1250, 820], 15, GREEN),
            Pig([1225, 780], 15, GREEN)
        ]

        self.obstacles = [
            Obstacle(pygame.Rect(900, 800, 50, 50), 100, BROWN),
            Obstacle(pygame.Rect(950, 750, 50, 120), 150, BROWN)
        ]

        self.game_over = False
        self.running = True

    def reset_level(self):
        """Сбрасывает игру к начальному состоянию."""
        for bird in self.birds:
            bird.reset()
        self.current_bird_index = 0
        self.current_bird = self.birds[self.current_bird_index]

        for pig in self.pigs:
            pig.reset()

        # Заново создаём препятствия (или можно хранить исходные)
        self.obstacles = [
            Obstacle(pygame.Rect(900, 800, 50, 50), 100, BROWN),
            Obstacle(pygame.Rect(950, 750, 50, 120), 150, BROWN)
        ]

        self.game_over = False
