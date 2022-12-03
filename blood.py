from pico2d import *
import random
import game_framework
import game_world
import server

class Blood:
    image = None
    def __init__(self, x=0, y=0):
        if Blood.image == None:
            Blood.image = load_image('resources\\blood_2.png')
            self.x, self.y = x, y

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass