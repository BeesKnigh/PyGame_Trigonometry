import pygame
import os
import math
from settings import WHITE, GREEN, GROUND_Y, HEIGHT, WIDTH
from objects.obstacle import Obstacle

def draw_game(game_state):
    if game_state.sky_image:
        game_state.screen.blit(game_state.sky_image, (0, 0))
    else:
        game_state.screen.fill(WHITE)

    camera_offset = game_state.camera.get_offset(game_state.current_bird) if game_state.current_bird else (0, 0)


    if not hasattr(game_state, 'ground_texture'):
        game_state.ground_texture = None
        try:
            paths_to_try = [
                "ground.png",
                "../ground.png",
                os.path.join(os.path.dirname(__file__), "..", "ground.png")
            ]
            for path in paths_to_try:
                try:
                    texture = pygame.image.load(path).convert()
                    ground_height = HEIGHT - GROUND_Y
                    game_state.ground_texture = pygame.transform.scale(texture, (WIDTH, ground_height))
                    break
                except pygame.error:
                    continue
        except Exception as e:
            print(f"Ошибка загрузки текстуры земли: {e}")

    ground_height = HEIGHT - GROUND_Y
    if game_state.ground_texture:
        texture_width = game_state.ground_texture.get_width()
        num_tiles = math.ceil(WIDTH / texture_width) + 2
        start_x = (-camera_offset[0] % texture_width) - texture_width

        for i in range(num_tiles):
            pos_x = start_x + i * texture_width
            game_state.screen.blit(game_state.ground_texture, (pos_x, GROUND_Y))
    else:
        pygame.draw.rect(
            game_state.screen,
            GREEN,
            (-camera_offset[0], GROUND_Y, 2 * WIDTH, ground_height)
        )

    for obstacle in game_state.obstacles:
        obstacle.draw(game_state.screen, camera_offset)

    for pig in game_state.pigs:
        pig.draw(game_state.screen, camera_offset)

    if game_state.current_bird:
        game_state.current_bird.draw(game_state.screen, camera_offset)

        if game_state.current_bird.dragging:
            mouse_pos = pygame.mouse.get_pos()
            start_pos = game_state.current_bird.start_pos

            pygame.draw.line(
                game_state.screen,
                (0, 0, 0),
                (start_pos[0] - camera_offset[0], start_pos[1]),
                mouse_pos,
                3
            )

            dx = start_pos[0] - (mouse_pos[0] + camera_offset[0])
            dy = start_pos[1] - mouse_pos[1]
            angle = math.atan2(dy, dx)
            angle_text = game_state.font.render(f"Угол: {math.degrees(angle):.1f}°", True, (0, 0, 255))
            game_state.screen.blit(angle_text, (70, 20))

    remaining_birds = max(0, len(game_state.birds) - game_state.current_bird_index)
    birds_text = game_state.font.render(f"Осталось кошек: {remaining_birds}", True, (0, 0, 255))
    game_state.screen.blit(birds_text, (70, 60))

    if all(not pig.alive for pig in game_state.pigs):
        victory_text = game_state.font.render("Уровень пройден! Нажмите R для рестарта.", True, (0, 0, 255))
        game_state.screen.blit(
            victory_text,
            (
                (WIDTH - victory_text.get_width()) // 2,
                (HEIGHT - victory_text.get_height()) // 2
            )
        )
    elif game_state.game_over:
        game_over_text = game_state.font.render("Вы проиграли! Нажмите R для рестарта.", True, (0, 0, 255))
        game_state.screen.blit(
            game_over_text,
            (
                (WIDTH - game_over_text.get_width()) // 2,
                (HEIGHT - game_over_text.get_height()) // 2
            )
        )

    pygame.display.flip()

