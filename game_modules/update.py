import math
from settings import (
    BREAK_THRESHOLD, 
    RESTITUTION, 
    OBSTACLE_SLOWDOWN_FACTOR,
    GRAVITY,
    GROUND_Y
)
from settings import BREAK_THRESHOLD, RESTITUTION, OBSTACLE_SLOWDOWN_FACTOR
from utils import circle_collision, circle_rect_collision

def update_game(game_state, dt):
    for pig in game_state.pigs:
        pig.update(dt)

    level_complete = all(not pig.alive for pig in game_state.pigs)

    if (game_state.current_bird and 
        game_state.current_bird.launched and 
        not level_complete and 
        not game_state.game_over):
        
        bird = game_state.current_bird
        bird.update(dt)

        for obstacle in game_state.obstacles[:]:
            if circle_rect_collision(bird.pos[0], bird.pos[1], bird.radius, obstacle.rect):
                impact_speed = math.hypot(bird.vx, bird.vy)
                if impact_speed > BREAK_THRESHOLD:
                    obstacle.health -= impact_speed * 0.1
                    if obstacle.is_destroyed():
                        game_state.obstacles.remove(obstacle)
                else:
                    bird.vx = -bird.vx * RESTITUTION
                    bird.vy = -bird.vy * RESTITUTION

                bird.vx *= OBSTACLE_SLOWDOWN_FACTOR
                bird.vy *= OBSTACLE_SLOWDOWN_FACTOR

        for pig in game_state.pigs:
            if pig.alive and circle_collision(
                bird.pos[0], bird.pos[1], bird.radius,
                pig.pos[0], pig.pos[1], pig.radius
            ):
                pig.alive = False

        if abs(bird.vx) < 5 and abs(bird.vy) < 5:
            game_state.current_bird_index += 1
            if game_state.current_bird_index < len(game_state.birds):
                game_state.current_bird = game_state.birds[game_state.current_bird_index]
            else:
                game_state.game_over = True
                game_state.current_bird = None

    if level_complete:
        pass
