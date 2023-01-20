import random
import arcade
from datetime import datetime
from spaceship import Spaceship
from enemy import Enemy
from bullet import Bullet
from heart import Heart
from fire import Fire

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=400, height=600, title='Rick and Morty game')
        self.background_game = arcade.load_texture('pictures/rick-and-morty-outer-space.jpg')
        self.start_picture = arcade.load_texture('pictures/rick_and_morty.jpg')
        self.game_over_picture = arcade.load_texture('pictures/game_over.jpg')
        self.rick = Spaceship(self.width, 'mamad')
        self.enemies = []
        self.fires = []
        self.state = 'initial'
        self.counter_time = 0
        self.counter_level = 0
        self.heart = 0
        self.hearts = []
        self.level = 1
        self.score = 0
        self.difficaulty = 2 # 1 or 2 or 3
        self.collision_sound = arcade.Sound('voice/collision_enemy.mp3')
        self.fault_key_sound = arcade.Sound('voice/fault_key_sound.mp3')
        self.game_over_sound = arcade.load_sound('voice/game_over.mp3')
        self.theme_sound = arcade.load_sound('voice/theme.mp3')
        self.game_sound = arcade.load_sound('voice/game.mp3')
        self.play_theme_sound = arcade.play_sound(self.theme_sound,1,0,True)
        f = open('database/score.txt',"r")
        self.highest_score_easy =  int(f.readline())
        self.highest_score_normal =  int(f.readline())
        self.highest_score_hard =  int(f.readline())
        f.close()
        self.h_score = 0
        self.first_enemy = True

    def on_draw(self):
        arcade.start_render()
        if self.state == 'initial':
            arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.start_picture) 
            arcade.draw_text('Rick and Morty', 65, 130, arcade.color.DARK_BLUE, 40, 1, 'left', 'Brush Script MT', True)
            arcade.draw_text('Welcome to MoSa game', 40, 90, arcade.color.DARK_BLUE, 30, 1, 'left', 'Brush Script MT', True)
            arcade.draw_text('press number key to play', 40, 45, arcade.color.BLACK, 20, 1, 'left', 'arial', True)
            arcade.draw_text('1: easy   2: normal   3: hard', 15, 15, arcade.color.BLACK, 20, 1, 'left', 'arial', True)
        elif self.state == 'game':
            arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background_game)     

            self.rick.draw()

            for enemy in self.enemies:
                enemy.draw()

            for bullet in self.rick.bullets:
                bullet.draw()

            for fire in self.fires:
                fire.draw()

            for i in range(self.heart):
                self.hearts[i].draw()

            arcade.draw_text(f'Level: {self.level}', 15, 10, arcade.color.BLACK, 15, 1, 'left',"calibri",True)
            arcade.draw_text(f'Score: {self.score}', 100, 10, arcade.color.BLACK, 15, 1, 'left',"calibri",True)
            arcade.draw_text(f'Highest: {self.h_score}', 230, 10, arcade.color.BLACK, 15, 1, 'left',"calibri",True)
        elif self.state == 'game_over':
            arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.game_over_picture) 
            arcade.draw_text('Game Over', 35, 150, arcade.color.RED, 50, 1, 'left', 'calibri', True)
        
        arcade.finish_render()

    def on_key_press(self, symbol: int, modifiers: int):
        if self.state == 'initial':
            if symbol == arcade.key.KEY_1:
                self.heart = 5
                self.h_score = self.highest_score_easy
                self.difficaulty = 1
            elif symbol == arcade.key.KEY_2:
                self.heart = 3
                self.h_score = self.highest_score_normal
                self.difficaulty = 2
            elif symbol == arcade.key.KEY_3:
                self.heart = 2
                self.h_score = self.highest_score_hard
                self.difficaulty = 3
            else:
                arcade.play_sound(self.fault_key_sound)
            if self.heart:
                for i in range(self.heart):
                    self.hearts.append(Heart(i))
                self.state = 'game'
                self.play_theme_sound.delete()
                self.play_game_sound = arcade.play_sound(self.game_sound,1,0,True)
        elif self.state == 'game':
            if symbol == arcade.key.A or symbol == arcade.key.LEFT: 
                self.rick.change_x = -1
            elif symbol == arcade.key.D or symbol == arcade.key.RIGHT:
                self.rick.change_x = 1
            elif symbol == arcade.key.W or symbol == arcade.key.UP:
                self.rick.change_y = 1
            elif symbol == arcade.key.S or symbol == arcade.key.DOWN: 
                self.rick.change_y = -1
            elif symbol == arcade.key.SPACE or symbol == arcade.key.F:
                self.rick.fire()
            else:
                arcade.play_sound(self.fault_key_sound)
        elif self.state == 'game_over':
            exit(0)
        
    def on_key_release(self, symbol, modifiers):
        self.rick.change_x = 0
        self.rick.change_y = 0

    def on_update(self, delta_time):
        if self.state == 'game':
            # arcade.stop_sound(play_theme_sound)
            for enemy in self.enemies:
                if arcade.check_for_collision(self.rick, enemy):
                    self.game_over()
            
            for enemy in self.enemies:
                for bullet in self.rick.bullets:
                    if arcade.check_for_collision(enemy, bullet):
                        self.fires.append(new_fire)
                        self.enemies.remove(enemy)
                        new_fire = Fire(enemy.center_x, enemy.center_y)
                        self.rick.bullets.remove(bullet)
                        self.score += self.level*10
                        if self.score > self.h_score:
                            self.h_score = self.score

            self.rick.move()

            for bullet in self.rick.bullets:
                bullet.move()  
                if bullet.center_y > self.height:
                    self.rick.bullets.remove(bullet)

            for enemy in self.enemies:
                enemy.move()   
                if enemy.center_y < 0:
                    self.enemies.remove(enemy)
                    self.heart -= 1
                    arcade.play_sound(self.collision_sound)
                    if self.heart == 0:
                        self.game_over()
                    
            for fire in self.fires:
                fire.duration -= 1
                if fire.duration == 0:
                    self.fires.remove(fire)

            self.time_now = datetime.now()
            if self.first_enemy:
                self.first_enemy = False
                self.last_time = self.time_now
            if (self.time_now - self.last_time).total_seconds() > (5 - self.difficaulty):
                self.new_enemy = Enemy(random.randint(100,self.width-100),self.height + 120, self.level)
                self.enemies.append(self.new_enemy)
                self.last_time = self.time_now

            self.counter_level += 1
            if self.counter_level == 3000:
                self.counter_level = 0
                if self.level < 10:
                    self.level += 1
 
    def game_over(self):
        open('database/score.txt', 'w').close()
        file_object = open('database/score.txt', 'a')
        if self.difficaulty == 1:
            self.highest_score_easy = self.h_score
        elif self.difficaulty == 2:
            self.highest_score_normal = self.h_score
        elif self.difficaulty == 3:
            self.highest_score_hard = self.h_score
        temp_string = str(self.highest_score_easy) + '\n'
        temp_string += str(self.highest_score_normal) + '\n'
        temp_string += str(self.highest_score_hard)
        file_object.write(temp_string)
        file_object.close()
        print('Game over 👩🏻‍🏭')
        self.state = 'game_over'
        self.play_game_sound.delete()
        arcade.play_sound(self.game_over_sound,1,0,True)

window = Game()
arcade.run()