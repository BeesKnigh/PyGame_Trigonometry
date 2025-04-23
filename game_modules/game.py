import pygame
import sys

from game_modules.game_state import GameState
from game_modules.events import handle_events
from game_modules.update import update_game
from game_modules.render import draw_game

def run_game():
    pygame.init()

    game_state = GameState()

    while game_state.running:
        dt = game_state.clock.tick(60) / 1000.0

        handle_events(game_state, dt)

        update_game(game_state, dt)

        draw_game(game_state)

    pygame.quit()
    return 0
