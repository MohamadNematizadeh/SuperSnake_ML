
import arcade
import tensorflow as tf
import pandas as pd
import numpy as np
from scr.apple import Apple
from scr.snake import Snake
from scr.poo import  Poo
from scr.color import  Color
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
class Game(arcade.Window):
    def __init__(self):
        super().__init__(width =SCREEN_WIDTH , height =SCREEN_HEIGHT,title="SuperSnake V2 🐍")
        arcade.set_background_color(Color.khaki)
        self.snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.poo = Poo(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.model = tf.keras.models.load_model('weights/SuperSnake.h5')
        self.game_status="run"

    def on_draw(self):
        arcade.start_render()
        self.snake.draw()
        self.apple.draw()
        self.poo.draw()
        arcade.draw_text("Score:", 20 , SCREEN_HEIGHT - 25, Color.black,font_name="calibri")
        arcade.draw_text(str(self.snake.score), 100, SCREEN_HEIGHT -25, Color.black,font_name="calibri")
        if self.game_status=="Game Over":
            arcade.draw_lrtb_rectangle_filled(0, self.width, self.height, 0, arcade.color.BLACK)
            arcade.draw_text("GAME OVER!", self.width//5, self.height//2, arcade.color.RED, 30)
        
        
    def on_update(self, delta_time):
        data = {'w0':None,
                'w1':None,
                'w2':None,
                'w3':None,
                'a0':None,
                'a1':None,
                'a2':None,
                'a3':None,
                'b0':None,
                'b1':None,
                'b2':None,
                'b3':None}
                
        if self.snake.center_x == self.apple.center_x and self.snake.center_y < self.apple.center_y:
            data['a0'] = 1  
            data['a1'] = 0  
            data['a2'] = 0
            data['a3'] = 0
        elif self.snake.center_x == self.apple.center_x and self.snake.center_y > self.apple.center_y:    
            data['a0'] = 0
            data['a1'] = 0
            data['a2'] = 1
            data['a3'] = 0
        elif self.snake.center_x < self.apple.center_x and self.snake.center_y == self.apple.center_y:
            data['a0'] = 0
            data['a1'] = 1
            data['a2'] = 0
            data['a3'] = 0
        elif self.snake.center_x > self.apple.center_x and self.snake.center_y == self.apple.center_y:    
            data['a0'] = 0
            data['a1'] = 0
            data['a2'] = 0
            data['a3'] = 1

        data['w0'] = SCREEN_HEIGHT - self.snake.center_y 
        data['w1'] = SCREEN_WIDTH - self.snake.center_x  
        data['w2'] = self.snake.center_y
        data['w3'] = self.snake.center_x

        for part in self.snake.body:
            if self.snake.center_x == part['x'] and self.snake.center_y < part['y']:
                data['b0'] = 1
                data['b1'] = 0
                data['b2'] = 0
                data['b3'] = 0
            elif self.snake.center_x == part['x'] and self.snake.center_y > part['y']:
                data['b0'] = 0
                data['b1'] = 0
                data['b2'] = 1
                data['b3'] = 0   
            elif self.snake.center_x < part['x'] and self.snake.center_y == part['y']:
                data['b0'] = 0
                data['b1'] = 1
                data['b2'] = 0
                data['b3'] = 0   
            elif self.snake.center_x > part['x'] and self.snake.center_y == part['y']:
                data['b0'] = 0
                data['b1'] = 0
                data['b2'] = 0
                data['b3'] = 1  

        data = pd.DataFrame(data, index=[1])
        data.fillna(0, inplace=True)
        data = data.values

        output = self.model.predict(data) 
        direction = output.argmax()

        if direction == 0:
            self.snake.change_x = 0
            self.snake.change_y = 1
        elif direction == 1:
            self.snake.change_x = 1
            self.snake.change_y = 0
        elif direction == 2:
            self.snake.change_x = 0
            self.snake.change_y = -1   
        elif direction == 3:
            self.snake.change_x = -1
            self.snake.change_y = 0       


        self.snake.on_update(delta_time)
        self.apple.on_update()

        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat()
            self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat()
            self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)
        if arcade.check_for_collision(self.snake, self.poo):
            self.snake.eat_poo(self.poo)
            self.poo = Poo(SCREEN_WIDTH, SCREEN_HEIGHT)
       
if __name__ == "__main__":
    window = Game()
    arcade.run()
