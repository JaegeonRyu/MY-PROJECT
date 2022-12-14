from pico2d import *
import game_world
import game_framework

# Bullet Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

PIXEL_PER_METER = 10.0 / 0.3
BULLET_SPEED_KPH = 30.0
BULLET_SPEED_MPM = BULLET_SPEED_KPH * 1000.0 / 60.0
BULLET_SPEED_MPS = BULLET_SPEED_MPM / 60.0
BULLET_SPEED_PPS = BULLET_SPEED_MPS * PIXEL_PER_METER

class Bullet:
    image = None

    def __init__(self, x, y, x_velocity, y_velocity):
        if Bullet.image is None:
            Bullet.image = load_image('resources\\bullet.png')

        self.x, self.y, self.x_velocity, self.y_velocity = x, y, x_velocity, y_velocity
        self.bullet_frame = 0
        self.frame = 0

        self.gun_sound = load_wav('resources\\gun.wav')
        self.gun_sound.set_volume(20)
        self.gun_sound.play()

    def return_xy(self, x, y, xd, yd):
        self.x, self.y, self.x_velocity, self.y_velocity = x, y, xd, yd

    def draw(self):
        self.bullet_frame = (self.bullet_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if self.x_velocity > 0 and self.y_velocity == 0:
            self.x += self.x_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_draw(int(self.bullet_frame) * 80, 80, 80, 80, self.x+15, self.y+15)
        elif self.x_velocity > 0 and self.y_velocity > 0:
            self.x += self.x_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.y += self.y_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_composite_draw(int(self.bullet_frame)*80, 80, 80, 80, 3.141592 / 4, '', self.x, self.y, 80, 80)
        elif self.y_velocity > 0 and self.x_velocity == 0:
            self.y += self.y_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_composite_draw(int(self.bullet_frame)*80, 80, 80, 80, 3.141592 / 2, '', self.x, self.y, 80, 80)
        elif self.x_velocity < 0 and self.y_velocity > 0:
            self.x += self.x_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.y += self.y_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_composite_draw(int(self.bullet_frame)*80, 80, 80, 80, 3.141592 * 3/4, '', self.x, self.y, 80, 80)
        elif self.x_velocity < 0 and self.y_velocity == 0:
            self.x += self.x_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_composite_draw(int(self.bullet_frame)*80, 80, 80, 80, 3.141592, '', self.x+15, self.y+15, 80, 80)
        elif self.x_velocity < 0 and self.y_velocity < 0:
            self.x += self.x_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.y += self.y_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_composite_draw(int(self.bullet_frame)*80, 80, 80, 80, -3.141592 * 3/4, '', self.x, self.y, 80, 80)
        elif self.y_velocity < 0 and self.x_velocity == 0:
            self.y += self.y_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_composite_draw(int(self.bullet_frame)*80, 80, 80, 80, -3.141592 / 2, '', self.x, self.y, 80, 80)
        elif self.x_velocity > 0 and self.y_velocity < 0:
            self.x += self.x_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.y += self.y_velocity * BULLET_SPEED_PPS * game_framework.frame_time
            self.image.clip_composite_draw(int(self.bullet_frame)*80, 80, 80, 80, -3.141592/4, '', self.x, self.y, 80, 80)

        # draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        if self.x < 0 or self.x > 800:
            game_world.remove_object(self)
        if self.y < 0 or self.y > 550:
            game_world.remove_object(self)

    def get_bb(self):
        if self.x_velocity > 0 or self.x_velocity < 0:
             return self.x+10, self.y+10, self.x + 25, self.y + 20
        if self.y_velocity > 0 or self.y_velocity < 0:
            return self.x-5, self.y, self.x + 5, self.y + 20

    def handle_collision(self, other, group):
        if group == 'bullet:mobs':
            game_world.remove_object(self)
            pass

