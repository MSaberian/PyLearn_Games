import arcade

class Board(arcade.Sprite):
    def __init__(self,x):
        super().__init__()
        self.center_x = x
        self.center_y = 20
        self.color = arcade.color.RED
        self.change_x = 0
        self.change_y = 0
        self.width = 60
        self.height = 10
        self.speed = 10

    def move(self, game, ball):
        if self.center_y > ball.center_y:
            self.change_y = -1
        elif self.center_y < ball.center_y:
            self.change_y = 1
        
        self.center_y += self.change_y*self.speed
        
        if self.center_y < self.height:
            self.center_y = self.height
        
        if self.center_y > game.height - self.height:
            self.center_y = game.height - self.height

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y,
            self.width, self.height, self.color)