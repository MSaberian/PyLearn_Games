import arcade


class Heart(arcade.Sprite):
    def __init__(self, index):
        super().__init__('pictures/heart.png')
        self.center_x = 30 + index*40
        self.center_y = 60
        self.width = 30
        self.height = 30