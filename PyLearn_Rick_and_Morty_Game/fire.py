import arcade

class Fire(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__('pictures/fire.png')
        self.center_x = x
        self.center_y = y
        self.width = 80
        self.height = 80
        self.duration = 10
        self.destruction_sound = arcade.Sound('voice/destruction.mp3')
        arcade.play_sound(self.destruction_sound)

