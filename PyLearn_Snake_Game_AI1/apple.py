import random
import arcade

class Fruit(arcade.Sprite):
    def __init__(self, picture_path, game):
        super().__init__(picture_path)
        self.width = 32
        self.height = 32
        self.change_x = 0
        self.change_x = 0
        self.score = 0
        self.center_x = random.randint(game.margin, game.width - game.margin)
        self.center_y = random.randint(game.margin, game.height - game.margin)
        if game.state != 'initialize':
            game.update_full_fields()
        while game.check_for_conflict(self):
            self.center_x = random.randint(game.margin, game.width - game.margin)
            self.center_y = random.randint(game.margin, game.height - game.margin)

class Apple(Fruit):
    def __init__(self, game):
        super().__init__('pictures/apple.png', game)
        self.width = 32
        self.height = 32
        self.score = 1

class Pear(Fruit):
    def __init__(self, game):
        super().__init__('pictures/pear.png', game)
        self.width = 60
        self.height = 45
        self.score = 2

class Shit(Fruit):
    def __init__(self, game):
        super().__init__('pictures/shit.png', game)
        self.width = 32
        self.height = 32
        self.score = -1
        