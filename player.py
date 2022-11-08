from pico2d import *

class Player:
    def __init__(self):
        self.x, self.y = 800, 100
        self.frame = 0
        self.image = load_image('Jog_right.png')
    def update(self):
        self.frame = (self.frame + 1) % 14
        self.x -= 10
    def draw_right(self):
        self.image.clip_draw(self.frame*61, 0, 61, 60, self.x, self.y)