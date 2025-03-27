import sys
import math
import pygame
from settings import WIDTH, HEIGHT, GROUND_Y, WHITE, BLACK, RED, GREEN, BLUE, BROWN, START_POS, BIRD_RADIUS, BREAK_THRESHOLD, RESTITUTION
from utils import circle_collision, circle_rect_collision
from objects.bird import Bird
from objects.pig import Pig
from objects.obstacle import Obstacle

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angry Birds: Модульная версия")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Создаем объекты птицы, свиней и препятствий
bird = Bird(START_POS, BIRD_RADIUS, RED)

pigs = [
    Pig([1200, 820], 15, GREEN),
    Pig([1250, 820], 15, GREEN),
    Pig([1225, 780], 15, GREEN)
]

obstacles = [
    Obstacle(pygame.Rect(900, 800, 50, 50), 100, BROWN),
    Obstacle(pygame.Rect(950, 750, 50, 120), 150, BROWN)
]

running = True
while running:
    dt = clock.tick(60) / 1000.0  # Время между кадрами (в секундах)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Начало перетаскивания птицы
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if math.hypot(mouse_pos[0] - bird.pos[0], mouse_pos[1] - bird.pos[1]) < bird.radius:
                bird.dragging = True
                bird.launched = False

        # Отпускание мыши – запуск птицы
        if event.type == pygame.MOUSEBUTTONUP:
            if bird.dragging:
                bird.dragging = False
                mouse_pos = pygame.mouse.get_pos()
                bird.launch(mouse_pos)

        # Сброс игры – клавиша R
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                bird.reset()
                for pig in pigs:
                    pig.reset()
                obstacles = [
                    Obstacle(pygame.Rect(900, 800, 50, 50), 100, BROWN),
                    Obstacle(pygame.Rect(950, 750, 50, 120), 150, BROWN)
                ]

    # Пока птица перетаскивается, она следует за курсором
    if bird.dragging:
        bird.pos = list(pygame.mouse.get_pos())

    # Обновляем физику свиней: они реагируют на гравитацию и "падают"
    for pig in pigs:
        pig.update(dt)

    # Проверка завершения уровня: все свиньи уничтожены
    level_complete = all(not pig.alive for pig in pigs)

    # Обновляем физику птицы, если она запущена и уровень не завершён
    if bird.launched and not level_complete:
        bird.update(dt)

        # Проверка столкновений с препятствиями
        for obstacle in obstacles[:]:
            if circle_rect_collision(bird.pos[0], bird.pos[1], bird.radius, obstacle.rect):
                impact_speed = math.hypot(bird.vx, bird.vy)
                if impact_speed > BREAK_THRESHOLD:
                    obstacle.health -= impact_speed * 0.1
                    if obstacle.is_destroyed():
                        obstacles.remove(obstacle)
                else:
                    bird.vx = -bird.vx * RESTITUTION
                    bird.vy = -bird.vy * RESTITUTION

        # Проверка столкновений со свиньями
        for pig in pigs:
            if pig.alive and circle_collision(bird.pos[0], bird.pos[1], bird.radius,
                                               pig.pos[0], pig.pos[1], pig.radius):
                pig.alive = False
                # При столкновении со свиньей скорость птицы не изменяется

    # Отрисовка
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))  # Земля

    # Рисуем препятствия
    for obstacle in obstacles:
        obstacle.draw(screen)

    # Рисуем свиней
    for pig in pigs:
        pig.draw(screen)

    # Если птица перетаскивается, рисуем линию рогатки и отображаем угол выстрела
    if bird.dragging:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, BLACK, bird.start_pos, mouse_pos, 3)
        dx = bird.start_pos[0] - mouse_pos[0]
        dy = bird.start_pos[1] - mouse_pos[1]
        angle = math.atan2(dy, dx)
        angle_text = font.render(f"Угол: {math.degrees(angle):.1f}°", True, BLUE)
        screen.blit(angle_text, (20, 20))

    # Рисуем птицу
    bird.draw(screen)

    # Если уровень завершён, выводим сообщение
    if level_complete:
        victory_text = font.render("Уровень пройден! Нажмите R для рестарта.", True, BLUE)
        screen.blit(victory_text, ((WIDTH - victory_text.get_width()) // 2,
                                   (HEIGHT - victory_text.get_height()) // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
