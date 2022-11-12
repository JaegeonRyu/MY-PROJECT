from pico2d import *
import game_world
import game_framework

class UI:
    def __init__(self):
        self.image = load_image('DAY_1.png')
    def draw(self):
        self.image.draw(400, 580)
    def update(self):
        pass

class GUN:
    def __init__(self):
        self.image = load_image('ar.png')
    def draw(self):
        self.image.draw(70, 580)
    def update(self):
        pass
