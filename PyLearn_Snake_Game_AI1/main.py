import random
import arcade
from snake import Snake
from apple import Apple, Pear, Shit

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=500, height=500, title='Super Snake 🐍 V1')
        self.background_game = arcade.load_texture('pictures/grass.png')
        self.margin = 30
        self.full_fields = []
        self.state = 'initialize'
        self.snake = Snake(self)
        self.food = Apple(self)
        self.super_food = Pear(self)
        self.shit = Shit(self)
        self.state = 'start'

    def update_full_fields(self):
        self.full_fields = []
        self.full_fields.append({'x':self.food.center_x, 'y':self.food.center_y, 'w':self.food.width, 'h':self.food.height})
        self.full_fields.append({'x':self.super_food.center_x, 'y':self.super_food.center_y, 'w':self.super_food.width, 'h':self.super_food.height})
        self.full_fields.append({'x':self.shit.center_x, 'y':self.shit.center_y, 'w':self.shit.width, 'h':self.shit.height})
        self.full_fields.append({'x':self.snake.center_x, 'y':self.snake.center_y, 'w':self.snake.width, 'h':self.snake.height})
        for part in self.snake.body:
            self.full_fields.append({'x':part['x'], 'y':part['y'], 'w':self.snake.width, 'h':self.snake.height})
             
    def check_for_conflict(self, object):
        for thing in self.full_fields:
            if abs(thing['x'] - object.center_x) < (thing['w'] + object.width)//2 and abs(thing['y'] - object.center_y) < (thing['h'] + object.height)//2:
                return True
        else:
            return False

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background_game)
        self.food.draw()
        self.super_food.draw()
        if self.snake.draw():
            self.game_over()
        self.shit.draw()
        arcade.draw_text(f'Score: {self.snake.score}', 10, 10, arcade.color.BLACK, 15, 1, 'left',"calibri",True)
        if self.state == 'game_over' :
            arcade.draw_text('Game Over', self.width//2 - 150, self.height//2, arcade.color.RED, 50, 1,'left', 'calibri', True)
        arcade.finish_render()

    def on_key_press(self, symbol, modifiers):
        if self.state == 'game_over':
            self.state = 'exit'

    def on_key_release(self, symbol, modifiers):
        if self.state != 'game_over':
            if symbol == arcade.key.UP and (self.snake.change_x != 0 or self.state == 'start'):
                self.snake.change_x = 0
                self.snake.change_y = 1
            elif symbol == arcade.key.DOWN and (self.snake.change_x != 0 or self.state == 'start'):
                self.snake.change_x = 0
                self.snake.change_y = -1
            elif symbol == arcade.key.LEFT and (self.snake.change_y != 0 or self.state == 'start'):
                self.snake.change_x = -1
                self.snake.change_y = 0
            elif symbol == arcade.key.RIGHT and (self.snake.change_y != 0 or self.state == 'start'):
                self.snake.change_x = 1
                self.snake.change_y = 0
            if self.snake.change_x + self.snake.change_y:
                self.state = 'game'

    def game_over(self):
        self.state = 'game_over'

    def on_update(self, delta_time):
        if self.state == 'game':
            self.snake.move()

            if not ((self.snake.width//2 < self.snake.center_x < (self.width - self.snake.width//2)) and
                    (self.snake.height//2 < self.snake.center_y < (self.height - self.snake.height//2))):
                self.game_over()

            if arcade.check_for_collision(self.snake, self.food):
                self.snake.eat(self.food)
                self.food = Apple(self)

            if arcade.check_for_collision(self.snake, self.super_food):
                self.snake.eat(self.super_food)
                self.super_food = Pear(self)
                
            if arcade.check_for_collision(self.snake, self.shit):
                if self.snake.score > 0:
                    self.snake.eat(self.shit)
                    self.shit = Shit(self)
                    if self.snake.score == 0:
                        self.game_over()
                else:
                    self.game_over()

        elif self.state == 'exit':
            exit(0)


if __name__ == '__main__':
    game = Game()
    arcade.run()