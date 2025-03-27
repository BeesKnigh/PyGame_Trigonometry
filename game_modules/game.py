import pygame
import sys

from game_modules.game_state import GameState
from game_modules.events import handle_events
from game_modules.update import update_game
from game_modules.render import draw_game

def run_game():
    """Главная функция, запускающая игру."""
    pygame.init()

    # Создаём состояние игры
    game_state = GameState()

    # Основной игровой цикл
    while game_state.running:
        dt = game_state.clock.tick(60) / 1000.0

        # 1) Обрабатываем события
        handle_events(game_state, dt)

        # 2) Обновляем логику
        update_game(game_state, dt)

        # 3) Отрисовываем кадр
        draw_game(game_state)

    pygame.quit()
    return 0
