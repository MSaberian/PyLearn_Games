import random
import arcade

class Ball(arcade.Sprite):
    def __init__(self, board):
        super().__init__()
        self.radius = 7
        self.width = self.radius*2
        self.height = self.radius*2
        self.center_x = board.center_x
        self.center_y = board.center_y + board.height//2 + self.height//2
        self.color = arcade.color.BROWN
        self.change_x = random.choice([-1,1])
        self.change_y = 1
        self.speed = 2
        self.allow_hit = True


    def move(self):
        self.center_x += self.change_x*self.speed
        self.center_y += self.change_y*self.speed
        
    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, self.color)