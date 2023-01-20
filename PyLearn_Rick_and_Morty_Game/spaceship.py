import arcade
from bullet import Bullet

class Spaceship(arcade.Sprite):
    def __init__(self, w, name: str):
        super().__init__('pictures/rick spaceship_low.png')
        self.center_x = w // 2
        self.center_y = 80
        self.change_x = 0# 1 0 -1
        self.change_y = 0# 1 0 -1
        self.width = 100
        self.height = 60
        self.name = name
        self.speed = 4
        self.game_width = w
        self.margin_x = 30
        self.margin_y = 200
        self.bullets = []

    def move(self):
        if self.change_x == -1 and self.center_x > self.margin_x:
            self.center_x -= self.speed
        elif self.change_x == 1 and self.center_x < (self.game_width - self.margin_x):
            self.center_x += self.speed
        if self.change_y == -1 and self.center_y > self.margin_x:
            self.center_y -= self.speed
        elif self.change_y == 1 and self.center_y < self.margin_y:
            self.center_y += self.speed

    def fire(self):
        new_bullet = Bullet(self)
        self.bullets.append(new_bullet)