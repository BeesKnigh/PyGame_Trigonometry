class Camera:
    def __init__(self, follow_margin=200):
        self.follow_margin = follow_margin

    def get_offset(self, bird):
        if bird.launched:
            offset_x = bird.pos[0] - self.follow_margin
        else:
            offset_x = bird.start_pos[0] - self.follow_margin
        return (offset_x, 0)
