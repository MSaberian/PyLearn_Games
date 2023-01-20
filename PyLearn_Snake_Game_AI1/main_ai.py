import random
import time
import arcade
from snake import Snake
from apple import Apple, Pear, Shit

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=500, height=500, title='Super Snake AI 🐍 V1')
        self.background_game = arcade.load_texture('pictures/grass.png')
        self.margin = 30
        self.full_fields = []
        self.state = 'initialize'
        self.snake = Snake(self)
        self.food = Apple(self)
        self.super_food = Pear(self)
        self.snake.target = self.super_food
        self.shit = Shit(self)
        self.state = 'initialized'
        self.debug = False

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
        elif self.state == 'pause_red':        
            arcade.draw_rectangle_outline((self.center_x_smaller + self.center_x_bigger)//2, (self.center_y_smaller + self.center_y_bigger)//2,
                     self.center_x_bigger - self.center_x_smaller, self.center_y_bigger - self.center_y_smaller, arcade.color.RED,6)
        elif self.state == 'pause_blue':        
            arcade.draw_rectangle_outline((self.center_x_smaller + self.center_x_bigger)//2, (self.center_y_smaller + self.center_y_bigger)//2,
                     self.center_x_bigger - self.center_x_smaller, self.center_y_bigger - self.center_y_smaller, arcade.color.BLUE,6)

        arcade.finish_render()

    def on_key_press(self, symbol, modifiers):
        if self.state == 'initialized':
            self.state = 'configuration'
        elif self.state == 'game_over':
            self.state = 'exit'
        elif self.state == 'pause_red' or 'pause_blue':
            self.state = 'game'
        

    def on_key_release(self, symbol, modifiers):
        ...

    def game_over(self):
        self.state = 'game_over'

    def change_xy_snake(self, x, y, Aloow_to_change:bool =False):
        if self.snake.counter_change_direction == 0 or Aloow_to_change:
            if x:
                self.snake.change_x = x
                self.snake.change_y = 0
            elif y: 
                self.snake.change_x = 0
                self.snake.change_y = y
            self.snake.counter_change_direction = self.snake.height//self.snake.speed

    def change_xy_snake_fake(self, x, y):
        if x:
            self.snake.change_x_fake = x
            self.snake.change_y_fake = 0
        elif y: 
            self.snake.change_x_fake = 0
            self.snake.change_y_fake = y

    def check_path_by_fake_direction(self, target):
        output = False
        if self.snake.center_x < target.center_x:
            self.center_x_smaller = self.snake.center_x - self.snake.width
            self.center_x_bigger = target.center_x + self.snake.width
        else:
            self.center_x_smaller = target.center_x - self.snake.width
            self.center_x_bigger = self.snake.center_x + self.snake.width
        
        if self.snake.center_y < target.center_y:
            self.center_y_smaller = self.snake.center_y - self.snake.height
            self.center_y_bigger = target.center_y + self.snake.height
        else:
            self.center_y_smaller = target.center_y - self.snake.height
            self.center_y_bigger = self.snake.center_y + self.snake.height

        if not self.snake.change_x_fake == -1:
            self.center_x_smaller += self.snake.width
        if not self.snake.change_x_fake == 1:
            self.center_x_bigger -= self.snake.width
        if not self.snake.change_y_fake == -1:
            self.center_y_smaller += self.snake.height
        if not self.snake.change_y_fake == 1:
            self.center_y_bigger -= self.snake.height

        if (self.center_x_bigger - self.center_x_smaller) < self.snake.width:
            self.center_x_bigger = (self.center_x_bigger + self.center_x_smaller)//2 + self.snake.width//2
            self.center_x_smaller = (self.center_x_bigger + self.center_x_smaller)//2 - self.snake.width//2
        if (self.center_y_bigger - self.center_y_smaller) < self.snake.height:
            self.center_y_bigger = (self.center_y_bigger + self.center_y_smaller)//2 + self.snake.height//2
            self.center_y_smaller = (self.center_y_bigger + self.center_y_smaller)//2 - self.snake.height//2

        for part in self.snake.body:
            if self.center_x_smaller < part['x'] < self.center_x_bigger and self.center_y_smaller < part['y'] < self.center_y_bigger:            
                output = True
                    
        return output    

    def update_direction_fake(self, target):
        if self.state == 'game':
            if self.snake.change_x == -1: 
                if self.snake.center_x > target.center_x: # true path
                    return
                else:
                    if self.snake.center_y > target.center_y:
                        self.change_xy_snake_fake(0,-1)
                    else:
                        self.change_xy_snake_fake(0,1)
            
            if self.snake.change_x == 1: 
                if self.snake.center_x < target.center_x: # true path
                    return
                else:
                    if self.snake.center_y > target.center_y:
                        self.change_xy_snake_fake(0,-1)
                    else:
                        self.change_xy_snake_fake(0,1)

            if self.snake.change_y == -1: 
                if self.snake.center_y > target.center_y: # true path
                    return
                else:
                    if self.snake.center_x > target.center_x:
                        self.change_xy_snake_fake(-1,0)
                    else:
                        self.change_xy_snake_fake(1,0)
                        
            if self.snake.change_y == 1: 
                if self.snake.center_y < target.center_y: # true path
                    return
                else:
                    if self.snake.center_x > target.center_x:
                        self.change_xy_snake_fake(-1,0)
                    else:
                        self.change_xy_snake_fake(1,0)

    def update_direction(self, target):
        if self.state == 'configuration':
            if self.snake.center_x > target.center_x:
                self.change_xy_snake(-1,0)
            elif self.snake.center_x < target.center_x:
                self.change_xy_snake(1,0)
            self.state = 'game'
            
        elif self.state == 'game' or self.state == 'pause_red' or self.state == 'pause_blue':
            if self.snake.change_x == -1: 
                if self.snake.center_x > target.center_x: # true path
                    return
                else:
                    if self.snake.center_y > target.center_y:
                        self.change_xy_snake(0,-1)
                    else:
                        self.change_xy_snake(0,1)
            
            if self.snake.change_x == 1: 
                if self.snake.center_x < target.center_x: # true path
                    return
                else:
                    if self.snake.center_y > target.center_y:
                        self.change_xy_snake(0,-1)
                    else:
                        self.change_xy_snake(0,1)

            if self.snake.change_y == -1: 
                if self.snake.center_y > target.center_y: # true path
                    return
                else:
                    if self.snake.center_x > target.center_x:
                        self.change_xy_snake(-1,0)
                    else:
                        self.change_xy_snake(1,0)
                        
            if self.snake.change_y == 1: 
                if self.snake.center_y < target.center_y: # true path
                    return
                else:
                    if self.snake.center_x > target.center_x:
                        self.change_xy_snake(-1,0)
                    else:
                        self.change_xy_snake(1,0)

    def update_direction_to_free_space(self):
        if self.state == 'game' or self.state == 'pause_red' or self.state == 'pause_blue':
            if self.snake.change_x != 0: 
                self.change_xy_snake(0,-1,True)
                if self.check_next_move_collision_fance() or self.check_next_move_collision_itself():
                    self.change_xy_snake(0,1)
            
            else: 
                self.change_xy_snake(-1,0,True)
                if self.check_next_move_collision_fance() or self.check_next_move_collision_itself():
                    self.change_xy_snake(1,0)


    def decide_target(self):
        self.update_direction_fake(self.super_food)
        if not self.check_path_by_fake_direction(self.super_food):
            self.snake.target = self.super_food
            if self.debug:
                self.state = 'pause_blue'
        elif not self.check_path_by_fake_direction(self.food):
            self.snake.target = self.food
            if self.debug:
                self.state = 'pause_blue'
        else:
            self.snake.target = None
            if self.debug:
                self.state = 'pause_red'

    def check_next_move_collision_fance(self):
        if self.snake.change_x == 1 and (self.snake.center_x + self.snake.width//2 + self.snake.speed >= self.width):
            return True
        elif self.snake.change_x == -1 and (self.snake.center_x - self.snake.width//2 - self.snake.speed <= 0):
            return True
        elif self.snake.change_y == 1 and (self.snake.center_y + self.snake.height//2 + self.snake.speed >= self.height):
            return True
        elif self.snake.change_y == -1 and (self.snake.center_y - self.snake.height//2 - self.snake.speed <= 0):
            return True
        return False

    def check_next_move_collision_itself(self):   
        for part in self.snake.body[:-2*(self.snake.height//self.snake.speed)]:
            if (abs(part['x'] - (self.snake.center_x + self.snake.speed*self.snake.change_x)) < self.snake.width
                    and abs(part['y'] - (self.snake.center_y + self.snake.speed*self.snake.change_y)) < self.snake.height):  
                print('part x:' ,part['x'],'self.snake.center_x',self.snake.center_x,'self.snake.speed*self.snake.change_x',self.snake.speed*self.snake.change_x,'self.snake.width',self.snake.width)
                print('part y:' ,part['y'],'self.snake.center_y',self.snake.center_y,'self.snake.speed*self.snake.change_y',self.snake.speed*self.snake.change_y,'self.snake.width',self.snake.height) 
                return True
        else:
            return False

    def on_update(self, delta_time):
        if self.snake.counter_change_direction > 0:
            self.snake.counter_change_direction -= 1
        if self.state == 'game' or self.state == 'configuration':
            self.snake.move() 
            if self.snake.target == None:
                self.decide_target()
                if self.snake.target == None:
                    if self.check_next_move_collision_fance():
                        self.update_direction(self.super_food)
                        print('fance *** ')
                        print('change x:', self.snake.change_x, '- change y:', self.snake.change_y)
                    elif self.check_next_move_collision_itself():
                        self.update_direction_to_free_space()
                        print('snake *** ')
                        print('change x:', self.snake.change_x, '- change y:', self.snake.change_y)

            else: 
                self.update_direction(self.snake.target)
        if self.state == 'game' or self.state == 'pause_red':

            if not ((self.snake.width//2 < self.snake.center_x < (self.width - self.snake.width//2)) and
                    (self.snake.height//2 < self.snake.center_y < (self.height - self.snake.height//2))):
                self.game_over()

            if arcade.check_for_collision(self.snake, self.food):
                self.snake.eat(self.food)
                self.food = Apple(self)
                self.decide_target()

            if arcade.check_for_collision(self.snake, self.super_food):
                self.snake.eat(self.super_food)
                self.super_food = Pear(self)
                self.decide_target()
                
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