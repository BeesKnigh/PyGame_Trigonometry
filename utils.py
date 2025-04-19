import math
import pygame


# Проверяет столкновение двух кругов.
def circle_collision(x1, y1, r1, x2, y2, r2):
    return math.hypot(x1 - x2, y1 - y2) < (r1 + r2)

# Проверяет столкновение круга с прямоугольником.
def circle_rect_collision(cx, cy, radius, rect):
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    distance = math.hypot(cx - closest_x, cy - closest_y)
    return distance < radius
