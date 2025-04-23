# Размеры окна
WIDTH = 1600
HEIGHT = 900

# Параметры земли
GROUND_Y = 800

# Параметры птицы
BIRD_RADIUS = 10
START_POS = (200, 750)  # позиция рогатки

# Физика
OBSTACLE_SLOWDOWN_FACTOR = 0.8
GRAVITY = 400
LAUNCH_FACTOR = 3.0
RESTITUTION = 0.7
BREAK_THRESHOLD = 200

# Параметры препятствий
OBSTACLE_MIN_HEIGHT = 300  # Минимальная высота высоких препятствий
OBSTACLE_MAX_HEIGHT = 450  # Максимальная высота 
OBSTACLE_WIDTH = 100       # Ширина основания

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)       # птица
GREEN = (0, 200, 0)     # земля
PIG_COLOR = (0, 180, 0) # свиньи
BLUE = (0, 0, 255)      # текст
BROWN = (139, 69, 19)   # препятствия

IMAGE_PATHS = {
    "bird": "design_assets/game_assets/characters/eva.png",
    "bird_fly": "design_assets/game_assets/characters/eva_fly.png",
    "ground": "design_assets/game_assets/environment/ground.png",
    "sky": "design_assets/game_assets/environment/sky.png",
    "cucumber": "design_assets/game_assets/items/cucumber.png"
}