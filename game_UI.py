from pico2d import *
import game_world
import game_framework

class UI:
    def __init__(self):
        self.image = load_image('resources\\DAY_1.png')
    def draw(self):
        self.image.draw(400, 570)
    def update(self):
        pass

class GUN:
    def __init__(self):
        self.ar_image = load_image('resources\\ar.png')
    def draw(self):
        self.ar_image.draw(70, 570)
    def update(self):
        pass
