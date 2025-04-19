import pygame
from settings import WHITE, GREEN, GROUND_Y, HEIGHT, WIDTH
from objects.obstacle import Obstacle
import os
import math

def draw_game(game_state):
    """Отрисовывает весь текущий кадр."""
    # Отрисовка фона
    if game_state.sky_image:
        game_state.screen.blit(game_state.sky_image, (0, 0))
    else:
        game_state.screen.fill(WHITE)

    # Получаем смещение камеры
    camera_offset = (0, 0)
    if game_state.current_bird:
        camera_offset = game_state.camera.get_offset(game_state.current_bird)

    # Загрузка и подготовка текстуры земли
    if not hasattr(game_state, 'ground_texture'):
        game_state.ground_texture = None
        try:
            # Ищем текстуру земли по разным путям
            paths_to_try = [
                "ground.png",
                "../ground.png", 
                os.path.join(os.path.dirname(__file__), "..", "ground.png")
            ]
            
            for path in paths_to_try:
                try:
                    texture = pygame.image.load(path).convert()
                    # Создаем текстуру на всю ширину экрана и высоту земли
                    ground_height = HEIGHT - GROUND_Y
                    game_state.ground_texture = pygame.transform.scale(
                        texture, 
                        (WIDTH, ground_height)
                    )
                    break
                except pygame.error:
                    continue
        except Exception as e:
            print(f"Ошибка загрузки текстуры: {e}")

    # Отрисовка земли с бесконечной прокруткой
    ground_height = HEIGHT - GROUND_Y
    if game_state.ground_texture:
        texture_width = game_state.ground_texture.get_width()
        # Вычисляем сколько текстур нужно для покрытия экрана
        num_tiles = math.ceil(WIDTH / texture_width) + 2
        # Позиция первой текстуры с учетом смещения камеры
        start_x = (-camera_offset[0] % texture_width) - texture_width
        
        # Рисуем все нужные текстуры земли
        for i in range(num_tiles):
            pos_x = start_x + i * texture_width
            game_state.screen.blit(
                game_state.ground_texture,
                (pos_x, GROUND_Y)
            )
    else:
        # Fallback - зеленая полоса
        pygame.draw.rect(
            game_state.screen,
            GREEN,
            (-camera_offset[0], GROUND_Y, 2 * WIDTH, ground_height)
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

    # Отрисовка линии прицеливания
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
        
        # Отображение угла
        dx = game_state.current_bird.start_pos[0] - (mouse_pos[0] + camera_offset[0])
        dy = game_state.current_bird.start_pos[1] - mouse_pos[1]
        angle = math.atan2(dy, dx)
        angle_text = game_state.font.render(f"Угол: {math.degrees(angle):.1f}°", True, (0, 0, 255))
        game_state.screen.blit(angle_text, (20, 20))

    # Отображение количества оставшихся кошек
    remaining_birds = max(0, len(game_state.birds) - game_state.current_bird_index)
    birds_text = game_state.font.render(f"Осталось кошек: {remaining_birds}", True, (0, 0, 255))
    game_state.screen.blit(birds_text, (20 + 50, 60))  # Смещаем текст на 50 пикселей вправо

    # Проверка условий завершения уровня
    level_complete = all(not pig.alive for pig in game_state.pigs)
    if level_complete:
        victory_text = game_state.font.render("Уровень пройден! Нажмите R для рестарта.", True, (0, 0, 255))
        game_state.screen.blit(victory_text, (
            (WIDTH - victory_text.get_width()) // 2,
            (HEIGHT - victory_text.get_height()) // 2
        ))
    elif game_state.game_over:
        game_over_text = game_state.font.render("Вы проиграли! Нажмите R для рестарта.", True, (0, 0, 255))
        game_state.screen.blit(game_over_text, (
            (WIDTH - game_over_text.get_width()) // 2,
            (HEIGHT - game_over_text.get_height()) // 2
        ))

    pygame.display.flip()
