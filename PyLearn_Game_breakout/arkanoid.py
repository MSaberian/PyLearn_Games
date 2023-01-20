import random
import arcade
from ball import Ball
from board import Board
from brick import Brick

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=400, height=500, title= 'arkanoid 🎆🎇')
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.board = Board(self.width//2)
        self.ball = Ball(self.board)
        self.bricks = []
        self.brickList = arcade.SpriteList()
        self.score = 0
        self.heart = 3
        self.level = 1
        self.state = 'game'
        self.Laying_bricks_2()

    def Laying_bricks_0(self):
        for row in range(0,6,2):
            for com in range(6):
                x = 60*com + 50
                y = 30*row + 250
                self.bricks.append(Brick(x, y))
                self.brickList.append(self.bricks[-1])
                
    def Laying_bricks_1(self):
        for row in range(6):
            for com in range(0,6,2):
                x = 60*com + 80
                y = 30*row + 250
                self.bricks.append(Brick(x, y))
                self.brickList.append(self.bricks[-1])

    def Laying_bricks_2(self):
        for row in range(6):
            for com in range(6):
                if (row + com)%2:
                    x = 60*com + 50
                    y = 30*row + 250
                    self.bricks.append(Brick(x, y))
                    self.brickList.append(self.bricks[-1])

    def Laying_bricks_3(self):
        for row in range(6):
            for com in range(6):
                x = 60*com + 50
                y = 30*row + 200
                self.bricks.append(Brick(x, y))
                self.brickList.append(self.bricks[-1])


    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_outline(self.width//2, self.height//2 - 15, self.width - 10, self.height-40,
            arcade.color.SONIC_SILVER, border_width=10)
        self.board.draw()
        arcade.draw_text(f'Score: {self.score}  Level: {self.level}',\
                         10, self.height - 22, arcade.color.BLACK, 15, 1, 'left',"calibri",True)
        for brick in self.bricks:
            arcade.draw_rectangle_filled(brick.center_x, brick.center_y, brick.width, brick.height, brick.color)
        for i in range(self.heart):
            arcade.draw_rectangle_filled(self.width - 25*(i+1), self.height - 15, 20, 8, arcade.color.RED)
        if self.state == 'game':
            self.ball.draw()
        elif self.state == 'game_over':
            arcade.draw_text('Game Over', self.width//2 - 158, self.height//2, arcade.color.RED, 50, 1,'left', 'calibri', True)

        arcade.finish_render()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.board.width//2 + 10 < x < self.width - self.board.width//2 - 10:
            self.board.center_x = x

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.board.center_x -= self.board.speed
        elif symbol == arcade.key.RIGHT:
            self.board.center_x += self.board.speed
        if self.state == 'game_over':
            self.state = 'exit'

    def on_update(self, delta_time):
        if self.state == 'game':
            self.ball.move()

            if self.ball.center_x < 20:
                self.ball.change_x = 1
            elif self.ball.center_x > self.width - 20:
                self.ball.change_x = -1
                
            if self.ball.center_y > self.height - 50:
                self.ball.change_y *= -1

            if self.ball.center_y > 80:
                self.ball.allow_hit = True

            if arcade.check_for_collision(self.ball, self.board) and self.ball.allow_hit:
                self.ball.change_y *= -1
                self.ball.allow_hit = False

            brick_collision_List = arcade.check_for_collision_with_list(self.ball, self.brickList)
            for brick in brick_collision_List:
                self.brickList.remove(brick) 
                self.bricks.remove(brick) 
                self.score += self.level

                if self.ball.center_y < brick.center_y - brick.height//2:
                    self.ball.change_y = -1                    
                elif self.ball.center_y > brick.center_y + brick.height//2:
                    self.ball.change_y = 1                 
                elif self.ball.center_x > brick.center_x + brick.width//2:
                    self.ball.change_x = 1                 
                else:
                    self.ball.change_x = -1

                if len(self.bricks) == 0:
                    self.level += 1
                    del self.ball
                    self.ball = Ball(self.board)
                    self.ball.speed += self.level - 1
                    plot_number = self.level%4
                    if plot_number == 0:
                        self.Laying_bricks_3()
                    elif plot_number == 1:
                        self.Laying_bricks_0()
                    elif plot_number == 2:
                        self.Laying_bricks_1()
                    elif plot_number == 3:
                        self.Laying_bricks_2()

            if self.ball.center_y < 0:
                self.heart -= 1
                del self.ball
                if self.heart > 0:
                    self.ball = Ball(self.board)
                    self.ball.speed += self.level - 1
                else:
                    self.state = 'game_over'

        if self.state == 'exit':
            exit(0)


game = Game()
arcade.run()