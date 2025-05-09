import pygame
import os
import math
from settings import (
    WIDTH, HEIGHT, BIRD_RADIUS, START_POS, RED, BROWN, GREEN, GROUND_Y, IMAGE_PATHS
)
from objects.bird import Bird
from objects.pig import Pig
from objects.obstacle import Obstacle
from game_modules.camera import Camera

class GameState:
    def __init__(self):
        pygame.display.set_caption("Angry Eva: Модульная версия")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.camera = Camera(follow_margin=200)

        self.sky_image = self._load_image(IMAGE_PATHS["sky"], (WIDTH, HEIGHT))
        self.ground_texture = self._load_image(IMAGE_PATHS["ground"])
        self.ground_height = HEIGHT - GROUND_Y

        self.birds = [
            Bird(START_POS, BIRD_RADIUS, RED),
            Bird(START_POS, BIRD_RADIUS, (255, 100, 0)),
            Bird(START_POS, BIRD_RADIUS, (200, 0, 0))
        ]
        self.current_bird_index = 0
        self.current_bird = self.birds[self.current_bird_index]

        self.obstacles, self.pigs = self._create_towers_with_cucumbers()

        self.game_over = False
        self.running = True

    def _load_image(self, path, size=None):
        try:
            possible_paths = [
                path,
                os.path.join(os.path.dirname(__file__), path),
                os.path.join(os.path.dirname(__file__), "..", path)
            ]

            for img_path in possible_paths:
                try:
                    image = pygame.image.load(img_path).convert_alpha()
                    if size:
                        return pygame.transform.scale(image, size)
                    return image
                except pygame.error:
                    continue

            print(f"Не удалось загрузить изображение: {path}")
            surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.rect(surf, (255, 0, 255, 128), (0, 0, 50, 50))
            return surf
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            return None

    def _create_towers_with_cucumbers(self):
        towers = [
            {"x": 700, "width": 120, "height": 200, "health": 200, 
             "color": (139, 69, 19), "cucumber": {"size": 3.0}},
            {"x": 1150, "width": 80, "height": 450, "health": 180, 
             "color": (160, 82, 45), "cucumber": {"size": 3.0}},
            {"x": 1450, "width": 100, "height": 380, "health": 220, 
             "color": (139, 69, 19), "cucumber": {"size": 3.0}}
        ]

        obstacles = []
        pigs = []
        cucumber_offset = 50

        for i, tower in enumerate(towers):
            obstacle_rect = pygame.Rect(
                tower["x"],
                GROUND_Y - tower["height"],
                tower["width"],
                tower["height"]
            )
            obstacle = Obstacle(obstacle_rect, tower["health"], tower["color"])
            obstacles.append(obstacle)

            base_radius = 15
            size_multiplier = tower["cucumber"]["size"]
            
            if i == 0:
                center_x = tower["x"] + tower["width"] + cucumber_offset + 100
            elif i == 2:
                center_x = towers[0]["x"] + towers[0]["width"] + cucumber_offset + 180
            else:
                center_x = tower["x"] + tower["width"] + cucumber_offset + 40

            center_y = GROUND_Y - (base_radius * size_multiplier)

            pig = Pig(
                pos=[center_x, center_y],
                radius=base_radius,
                color=GREEN,
                size_multiplier=size_multiplier
            )
            pigs.append(pig)

        return obstacles, pigs

    def _draw_ground(self):
        camera_offset = self.camera.get_offset()

        if self.ground_texture:
            scaled_texture = pygame.transform.scale(
                self.ground_texture,
                (WIDTH, self.ground_height)
            )
            num_tiles = math.ceil(WIDTH / WIDTH) + 2
            start_x = (-camera_offset[0] % WIDTH) - WIDTH

            for i in range(num_tiles):
                x = start_x + i * WIDTH
                self.screen.blit(scaled_texture, (x, GROUND_Y))
        else:
            pygame.draw.rect(
                self.screen,
                GREEN,
                (0, GROUND_Y, WIDTH, self.ground_height)
            )

    def reset_level(self):
        for bird in self.birds:
            bird.reset()
        self.current_bird_index = 0
        self.current_bird = self.birds[self.current_bird_index]
        self.obstacles, self.pigs = self._create_towers_with_cucumbers()
        self.game_over = False

    def update(self, dt):
        self.current_bird.update(dt)
        for pig in self.pigs:
            pig.update(dt)

    def draw(self):
        if self.sky_image:
            self.screen.blit(self.sky_image, (0, 0))
        else:
            self.screen.fill((135, 206, 250))

        self._draw_ground()

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for pig in self.pigs:
            pig.draw(self.screen, offset=self.camera.get_offset())

        self.current_bird.draw(self.screen)
        self.camera.update(self.current_bird)

        if self.current_bird and self.current_bird.dragging:
            self._draw_aiming_line()

        self._draw_ui()
        pygame.display.flip()

    def _draw_aiming_line(self):
        mouse_pos = pygame.mouse.get_pos()
        camera_offset = self.camera.get_offset()

        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (self.current_bird.start_pos[0] - camera_offset[0],
             self.current_bird.start_pos[1]),
            mouse_pos,
            3
        )

        dx = self.current_bird.start_pos[0] - (mouse_pos[0] + camera_offset[0])
        dy = self.current_bird.start_pos[1] - mouse_pos[1]
        angle = math.atan2(dy, dx)
        angle_text = self.font.render(f"Угол: {math.degrees(angle):.1f}°", True, (0, 0, 255))
        self.screen.blit(angle_text, (20, 20))

    def _draw_ui(self):
        remaining_birds = max(0, len(self.birds) - self.current_bird_index)
        birds_text = self.font.render(f"Осталось птиц: {remaining_birds}", True, (0, 0, 255))
        self.screen.blit(birds_text, (20, 60))

        if all(not pig.alive for pig in self.pigs):
            victory_text = self.font.render("Уровень пройден! Нажмите R для рестарта.", True, (0, 0, 255))
            self.screen.blit(victory_text, (
                (WIDTH - victory_text.get_width()) // 2,
                (HEIGHT - victory_text.get_height()) // 2
            ))
        elif self.game_over:
            game_over_text = self.font.render("Вы проиграли! Нажмите R для рестарта.", True, (0, 0, 255))
            self.screen.blit(game_over_text, (
                (WIDTH - game_over_text.get_width()) // 2,
                (HEIGHT - game_over_text.get_height()) // 2
            ))

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.update(dt)
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    game_state = GameState()
    game_state.run()