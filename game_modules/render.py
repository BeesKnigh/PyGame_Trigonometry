import pygame
from settings import WHITE, GREEN, GROUND_Y, HEIGHT
from objects.obstacle import Obstacle

def draw_game(game_state):
    """Отрисовывает весь текущий кадр."""
    game_state.screen.fill(WHITE)

    # Вычисление смещения камеры
    camera_offset = (0, 0)
    if game_state.current_bird:
        camera_offset = game_state.camera.get_offset(game_state.current_bird)

    # «Бесконечная» земля
    ground_x = -10_000
    ground_width = 20_000
    pygame.draw.rect(
        game_state.screen,
        GREEN,
        (ground_x - camera_offset[0], GROUND_Y, ground_width, HEIGHT - GROUND_Y)
    )

    # Отрисовка препятствий
    for obstacle in game_state.obstacles:
        obstacle.draw(game_state.screen, camera_offset)

    # Отрисовка свиней
    for pig in game_state.pigs:
        pig.draw(game_state.screen, camera_offset)

    # Отрисовка текущей птицы
    if game_state.current_bird:
        game_state.current_bird.draw(game_state.screen, camera_offset)

    # Если птица перетаскивается, рисуем линию рогатки и угол
    if game_state.current_bird and game_state.current_bird.dragging:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(
            game_state.screen,
            (0, 0, 0),
            (game_state.current_bird.start_pos[0] - camera_offset[0],
             game_state.current_bird.start_pos[1]),
            mouse_pos,
            3
        )

        dx = game_state.current_bird.start_pos[0] - (mouse_pos[0] + camera_offset[0])
        dy = game_state.current_bird.start_pos[1] - mouse_pos[1]
        import math
        angle = math.atan2(dy, dx)
        angle_text = game_state.font.render(f"Угол: {math.degrees(angle):.1f}°", True, (0, 0, 255))
        game_state.screen.blit(angle_text, (20, 20))

    # Количество оставшихся птиц
    remaining_birds = max(0, len(game_state.birds) - game_state.current_bird_index)
    birds_text = game_state.font.render(f"Осталось птиц: {remaining_birds}", True, (0, 0, 255))
    game_state.screen.blit(birds_text, (20, 60))

    # Проверка победы/поражения
    level_complete = all(not pig.alive for pig in game_state.pigs)
    if level_complete:
        victory_text = game_state.font.render("Уровень пройден! Нажмите R для рестарта.", True, (0, 0, 255))
        game_state.screen.blit(victory_text, (
            (game_state.screen.get_width() - victory_text.get_width()) // 2,
            (game_state.screen.get_height() - victory_text.get_height()) // 2
        ))
    elif game_state.game_over:
        game_over_text = game_state.font.render("Вы проиграли! Нажмите R для рестарта.", True, (0, 0, 255))
        game_state.screen.blit(game_over_text, (
            (game_state.screen.get_width() - game_over_text.get_width()) // 2,
            (game_state.screen.get_height() - game_over_text.get_height()) // 2
        ))

    pygame.display.flip()