from random import randint
import arcade

class Brick(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.color = randint(0, 255) , randint(0, 255) , randint(0, 255)
        self.change_x = 0
        self.change_y = 0
        self.width = 58
        self.height = 28
