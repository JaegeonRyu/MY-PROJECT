from pico2d import *
import game_world
import game_framework

# Bullet Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

PIXEL_PER_METER = 10.0 / 0.3
BULLET_SPEED_KPH = 100.0
BULLET_SPEED_MPM = BULLET_SPEED_KPH * 1000.0 / 60.0
BULLET_SPEED_MPS = BULLET_SPEED_MPM / 60.0
BULLET_SPEED_PPS = BULLET_SPEED_MPS * PIXEL_PER_METER

class Bullet:
    image = None

    def __init__(self, x=400, y=300, x_velocity=1, y_velocity=1):
        if Bullet.image == None:
            Bullet.image = load_image('bullet.png')
        self.x, self.y, self.x_velocity, self.y_velocity = x, y, x_velocity, y_velocity
        self.bullet_frame = 0
        self.frame = 0

    def draw(self):
        self.bullet_frame = (self.bullet_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        # self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if self.x_velocity > 0:
            self.x += self.x_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_draw(int(self.bullet_frame) * 100, 100, 100, 100, self.x, self.y)

        if self.y_velocity > 0:
            self.y += self.y_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_composite_draw(int(self.bullet_frame)*100, 100, 100, 100,
                                       3.141592 / 2, '', self.x, self.y, 100, 100)

        if self.x_velocity < 0:
            self.x += self.x_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_composite_draw(int(self.bullet_frame)*100, 100, 100, 100,
                                       3.141592, '', self.x, self.y, 100, 100)

        if self.y_velocity < 0:
            self.y += self.y_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_composite_draw(int(self.bullet_frame)*100, 100, 100, 100,
                                       -3.141592 / 2, '', self.x, self.y, 100, 100)


    def update(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        if self.x < 0 or self.x > 800:
            game_world.remove_object(self)
        if self.y < 0 or self.y > 600:
            game_world.remove_object(self)