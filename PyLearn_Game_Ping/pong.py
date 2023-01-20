import random
import arcade
from ball import Ball
from rocket import Rocket

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=800, height=500, title= 'ping 2023 🏓')
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.player_1 = Rocket(40, self.height//2, arcade.color.RED, 'mamad')
        self.player_2 = Rocket(self.width - 40, self.height//2, arcade.color.CYAN, 'sajjad')
        self.ball = Ball(self)
        self.playerList = arcade.SpriteList()
        self.playerList.append(self.player_1)
        self.playerList.append(self.player_2)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_outline(self.width//2, self.height//2,
            self.width - 30, self.height-30,
            arcade.color.WHITE, border_width=10)
        arcade.draw_line(self.width//2, 30, self.width//2, self.height -30,
            arcade.color.WHITE, line_width=10)
        self.player_1.draw()
        self.player_2.draw()
        self.ball.draw()
        arcade.draw_text(f'Player Score: {self.player_1.score}             Computer Score: {self.player_2.score}',\
                         30, 30, arcade.color.BLACK, 30, 1, 'left',"calibri",True)

        arcade.finish_render()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.player_1.height < y < self.height - self.player_1.height:
            self.player_1.center_y = y

    def on_update(self, delta_time):
        self.ball.move()
        self.player_2.move(self, self.ball)

        if self.ball.center_y < 30 or self.ball.center_y > self.height - 30:
            self.ball.change_y *= -1

        if abs(self.ball.center_x - self.width//2) < self.width//4:
            self.ball.allow_hit = True
    
        if arcade.check_for_collision_with_list(self.ball, self.playerList) and self.ball.allow_hit:
            self.ball.change_x *= -1
            self.ball.allow_hit = False

        if self.ball.center_x < 0:
            self.player_2.score += 1
            del self.ball
            self.ball = Ball(self)

        if self.ball.center_x > self.width:
            self.player_1.score += 1
            del self.ball
            self.ball = Ball(self)

game = Game()
arcade.run()