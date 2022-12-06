from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('resources\\grass.png')
        self.bgm = load_music('resources\\z_bgm.mp3')
        self.bgm.set_volume(60)
        self.bgm.repeat_play()

    def draw(self):
        self.image.draw(400, 300)

    def update(self):
        pass