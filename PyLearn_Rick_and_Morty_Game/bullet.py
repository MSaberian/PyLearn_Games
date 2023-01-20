import arcade
from playsound import playsound

class Bullet(arcade.Sprite):
    def __init__(self, host):
        super().__init__('pictures/bullet.png')
        self.width = 20
        self.height = 40
        self.center_x = host.center_x
        self.center_y = host.center_y + self.height//2
        self.speed = 3
        self.change_x = 0
        self.change_y = 1
        self.fire_sound = arcade.Sound('voice/fire.mp3')
        arcade.play_sound(self.fire_sound)
    
    def move(self):
        self.center_y += self.speed