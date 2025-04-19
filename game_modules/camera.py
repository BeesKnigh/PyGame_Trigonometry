class Camera:
    def __init__(self, follow_margin=200):
        self.follow_margin = follow_margin

    def get_offset(self, bird):
        """
        Возвращает смещение камеры в зависимости от состояния птицы.
        Если птица запущена – камера следует за ней,
        иначе камера зафиксирована на рогатке (начальной позиции птицы).
        """
        if bird.launched:
            offset_x = bird.pos[0] - self.follow_margin
        else:
            offset_x = bird.start_pos[0] - self.follow_margin
        return (offset_x, 0)
