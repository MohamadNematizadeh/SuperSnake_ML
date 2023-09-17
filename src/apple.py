import random
import arcade
from src.color import  Color
class Apple(arcade.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()
        self.width = 16
        self.height = 16
        self.center_x = random.randint(1, SCREEN_WIDTH) //16 * 16  
        self.center_y = random.randint(1, SCREEN_HEIGHT) //16 * 16
        self.radius = 8
        self.change_x = 0
        self.change_y = 0
        self.color = Color.red

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, self.color)        
