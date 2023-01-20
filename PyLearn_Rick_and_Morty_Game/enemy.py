import random
import arcade


class Enemy(arcade.Sprite):
    def __init__(self, x, h, s):
        super().__init__('pictures/enemy_spaceship_low.png')
        self.center_x = x
        self.center_y = h
        self.width = 80
        self.height = 80
        self.angle = 160
        self.speed = s

    def move(self):
        self.center_y -= self.speed

    # def destruction(self):
        # arcade.play_sound(self.destruction_sound)

