import sys
import math
import pygame
from settings import (
    WIDTH, HEIGHT, GROUND_Y, WHITE, BLACK, RED, GREEN, BLUE, BROWN,
    START_POS, BIRD_RADIUS, BREAK_THRESHOLD, RESTITUTION,
    OBSTACLE_SLOWDOWN_FACTOR
)
from utils import circle_collision, circle_rect_collision
from objects.bird import Bird
from objects.pig import Pig
from objects.obstacle import Obstacle
from game_modules.camera import Camera

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angry Birds: Модульная версия")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

camera = Camera(follow_margin=200)

# Список птиц
birds = [
    Bird(START_POS, BIRD_RADIUS, RED),
    Bird(START_POS, BIRD_RADIUS, (255, 100, 0)),
    Bird(START_POS, BIRD_RADIUS, (200, 0, 0))
]
current_bird_index = 0
current_bird = birds[current_bird_index]

# Список свиней
pigs = [
    Pig([1200, 820], 15, GREEN),
    Pig([1250, 820], 15, GREEN),
    Pig([1225, 780], 15, GREEN)
]

# Список препятствий
obstacles = [
    Obstacle(pygame.Rect(900, 800, 50, 50), 100, BROWN),
    Obstacle(pygame.Rect(950, 750, 50, 120), 150, BROWN)
]

game_over = False
running = True

while running:
    dt = clock.tick(60) / 1000.0
    camera_offset = camera.get_offset(current_bird) if current_bird else (0, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Начало перетаскивания – только если птица еще не была запущена
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_bird:
            if not current_bird.launched:  # <-- проверяем, что птица еще не запущена
                mouse_pos = pygame.mouse.get_pos()
                adjusted_mouse_pos = (mouse_pos[0] + camera_offset[0], mouse_pos[1])
                # Проверяем, попали ли мы в круг птицы
                if math.hypot(adjusted_mouse_pos[0] - current_bird.pos[0], 
                              adjusted_mouse_pos[1] - current_bird.pos[1]) < current_bird.radius:
                    current_bird.dragging = True

        # Отпускание мыши – запуск птицы
        if event.type == pygame.MOUSEBUTTONUP and not game_over and current_bird and current_bird.dragging:
            current_bird.dragging = False
            mouse_pos = pygame.mouse.get_pos()
            adjusted_mouse_pos = (mouse_pos[0] + camera_offset[0], mouse_pos[1])
            current_bird.launch(adjusted_mouse_pos)

        # Сброс (R)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                for bird in birds:
                    bird.reset()
                current_bird_index = 0
                current_bird = birds[current_bird_index]
                for pig in pigs:
                    pig.reset()
                obstacles = [
                    Obstacle(pygame.Rect(900, 800, 50, 50), 100, BROWN),
                    Obstacle(pygame.Rect(950, 750, 50, 120), 150, BROWN)
                ]
                game_over = False

    # Если птица перетаскивается, обновляем её позицию
    if current_bird and current_bird.dragging:
        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse_pos = (mouse_pos[0] + camera_offset[0], mouse_pos[1])
        current_bird.pos = list(adjusted_mouse_pos)

    # Обновление свиней
    for pig in pigs:
        pig.update(dt)

    level_complete = all(not pig.alive for pig in pigs)

    # Полёт птицы
    if current_bird and current_bird.launched and not level_complete and not game_over:
        current_bird.update(dt)

        # Столкновения с препятствиями
        for obstacle in obstacles[:]:
            if circle_rect_collision(current_bird.pos[0], current_bird.pos[1], current_bird.radius, obstacle.rect):
                impact_speed = math.hypot(current_bird.vx, current_bird.vy)
                if impact_speed > BREAK_THRESHOLD:
                    obstacle.health -= impact_speed * 0.1
                    if obstacle.is_destroyed():
                        obstacles.remove(obstacle)
                else:
                    current_bird.vx = -current_bird.vx * RESTITUTION
                    current_bird.vy = -current_bird.vy * RESTITUTION

                # Замедляем птицу
                current_bird.vx *= OBSTACLE_SLOWDOWN_FACTOR
                current_bird.vy *= OBSTACLE_SLOWDOWN_FACTOR

        # Столкновения со свиньями
        for pig in pigs:
            if pig.alive and circle_collision(
                current_bird.pos[0], current_bird.pos[1], current_bird.radius,
                pig.pos[0], pig.pos[1], pig.radius
            ):
                pig.alive = False

        # Если птица остановилась
        if abs(current_bird.vx) < 5 and abs(current_bird.vy) < 5:
            current_bird_index += 1
            if current_bird_index < len(birds):
                current_bird = birds[current_bird_index]
            else:
                game_over = True
                current_bird = None

    # Рисуем фон
    screen.fill(WHITE)

    # «Бесконечная» земля
    ground_x = -10_000
    ground_width = 20_000
    pygame.draw.rect(
        screen,
        GREEN,
        (ground_x - camera_offset[0], GROUND_Y, ground_width, HEIGHT - GROUND_Y)
    )

    # Отрисовка препятствий, свиней и птицы
    for obstacle in obstacles:
        obstacle.draw(screen, camera_offset)
    for pig in pigs:
        pig.draw(screen, camera_offset)
    if current_bird:
        current_bird.draw(screen, camera_offset)

    # Линия рогатки и угол
    if current_bird and current_bird.dragging:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, BLACK,
                         (current_bird.start_pos[0] - camera_offset[0], current_bird.start_pos[1]),
                         mouse_pos, 3)
        dx = current_bird.start_pos[0] - (mouse_pos[0] + camera_offset[0])
        dy = current_bird.start_pos[1] - mouse_pos[1]
        angle = math.atan2(dy, dx)
        angle_text = font.render(f"Угол: {math.degrees(angle):.1f}°", True, BLUE)
        screen.blit(angle_text, (20, 20))

    # Количество оставшихся птиц
    remaining_birds = max(0, len(birds) - current_bird_index)
    birds_text = font.render(f"Осталось птиц: {remaining_birds}", True, BLUE)
    screen.blit(birds_text, (20, 60))

    # Выводим сообщение о победе или поражении
    if level_complete:
        victory_text = font.render("Уровень пройден! Нажмите R для рестарта.", True, BLUE)
        screen.blit(victory_text, ((WIDTH - victory_text.get_width()) // 2,
                                   (HEIGHT - victory_text.get_height()) // 2))
    elif game_over:
        game_over_text = font.render("Вы проиграли! Нажмите R для рестарта.", True, BLUE)
        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2,
                                     (HEIGHT - game_over_text.get_height()) // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
