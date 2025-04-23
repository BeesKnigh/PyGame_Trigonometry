import math
import pygame
from settings import RESTITUTION
from utils import circle_rect_collision, circle_collision

def handle_events(game_state, dt):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_state.game_over and game_state.current_bird:
            if not game_state.current_bird.launched:
                mouse_pos = pygame.mouse.get_pos()
                camera_offset = game_state.camera.get_offset(game_state.current_bird)
                adjusted_mouse_pos = (mouse_pos[0] + camera_offset[0], mouse_pos[1])
                dist = math.hypot(
                    adjusted_mouse_pos[0] - game_state.current_bird.pos[0],
                    adjusted_mouse_pos[1] - game_state.current_bird.pos[1]
                )
                if dist < game_state.current_bird.radius:
                    game_state.current_bird.dragging = True

        if event.type == pygame.MOUSEBUTTONUP and not game_state.game_over and game_state.current_bird:
            if game_state.current_bird.dragging:
                game_state.current_bird.dragging = False
                mouse_pos = pygame.mouse.get_pos()
                camera_offset = game_state.camera.get_offset(game_state.current_bird)
                adjusted_mouse_pos = (mouse_pos[0] + camera_offset[0], mouse_pos[1])
                game_state.current_bird.launch(adjusted_mouse_pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_state.reset_level()
