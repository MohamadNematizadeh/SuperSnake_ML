import random
import arcade
from scr.color import  Color
class Poo(arcade.Sprite):
    def __init__(self, SCREEN_WIDTH,SCREEN_HEIGHT):
        super().__init__()
        self.width = 16
        self.height = 16
        self.color = arcade.color.BROWN
        self.r = 8
        self.center_x = random.randint(10, SCREEN_WIDTH - 10)
        self.center_y = random.randint(10 , SCREEN_HEIGHT - 10)

    def draw(self):
        arcade.draw_circle_filled(self.center_x , self.center_y ,self.r ,self.color)