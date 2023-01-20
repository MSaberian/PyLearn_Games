import arcade

class Snake(arcade.Sprite):
    def __init__(self, game):
        super().__init__()
        self.width = 32
        self.height = 32
        self.center_x = game.width // 2
        self.center_y = game.height // 2
        self.color = arcade.color.BROWN_NOSE
        self.color1 = arcade.color.KHAKI
        self.color2 = arcade.color.BROWN
        self.change_x = 0
        self.change_y = 0
        self.change_x_fake = 0
        self.change_y_fake = 0
        self.speed = 2
        self.score = 0
        self.body = []
        self.target = None
        self.counter_change_direction = 0

    def draw(self):
        output = False
        color_counter = 0
        for part in self.body:
            color_counter += 1
            if (color_counter // (self.height//self.speed) + self.score)%2:
                color = self.color1
            else:
                color = self.color2
            arcade.draw_rectangle_filled(part['x'], part['y'],
                                         self.width, self.height, color)
            if len(self.body) > 2*(self.height//self.speed) and color_counter < len(self.body) - 2*(self.height//self.speed):
                if abs(part['x'] - self.center_x) < self.width and abs(part['y'] - self.center_y) < self.height:            
                    output = True
                    
        arcade.draw_rectangle_filled(self.center_x, self.center_y,
                                     self.width, self.height, self.color)
        return output
             
    def move(self):
        self.body.append({'x':self.center_x, 'y':self.center_y})
        # while len(self.body) > self.score * (self.height//self.speed):
        while len(self.body) > self.score:
            self.body.pop(0)
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

    def eat(self, food):
        self.score += food.score
        del food