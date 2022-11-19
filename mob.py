from pico2d import *
import random
import game_framework
import game_world

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 12

# 좀비 1
PIXEL_PER_METER = 10.0 / 0.3
RUN1_SPEED_KPH = 4.0
RUN1_SPEED_MPM = RUN1_SPEED_KPH * 1000.0 / 60.0
RUN1_SPEED_MPS = RUN1_SPEED_MPM / 60.0
RUN1_SPEED_PPS = RUN1_SPEED_MPS * PIXEL_PER_METER

# 좀비 2
RUN2_SPEED_KPH = 6.0
RUN2_SPEED_MPM = RUN2_SPEED_KPH * 1000.0 / 60.0
RUN2_SPEED_MPS = RUN2_SPEED_MPM / 60.0
RUN2_SPEED_PPS = RUN2_SPEED_MPS * PIXEL_PER_METER

# 일반몹-1 클래스
class Mob1:
    image = None
    def __init__(self):
        if Mob1.image == None:
            Mob1.image = load_image('zombie_1.png')

        self.x, self.y = random.randint(50, 750), random.randint(50, 500)
        self.frame = random.randint(0, 11)
        self.die_frame = 28
        self.dir = random.randint(1, 8)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        if self.dir == 1:  # 왼쪽
            self.x += -1 * RUN1_SPEED_PPS * game_framework.frame_time
            if self.x <= 20:
                self.dir = random.randint(1, 8)
        if self.dir == 2:  # 왼쪽 위
            self.x += -1 * RUN1_SPEED_PPS * game_framework.frame_time
            self.y += 1 * RUN1_SPEED_PPS * game_framework.frame_time
            if self.x <= 20 or self.y >= 500:
                self.dir = random.randint(1, 8)
        if self.dir == 3:  # 위
            self.y += 1 * RUN1_SPEED_PPS * game_framework.frame_time
            if self.y >= 500:
                self.dir = random.randint(1, 8)
        if self.dir == 4:  # 오른쪽 위
            self.x += 1 * RUN1_SPEED_PPS * game_framework.frame_time
            self.y += 1 * RUN1_SPEED_PPS * game_framework.frame_time
            if self.x >= 780 or self.y >= 500:
                self.dir = random.randint(1, 8)
        if self.dir == 5:  # 오른쪽
            self.x += 1 * RUN1_SPEED_PPS * game_framework.frame_time
            if self.x >= 780:
                self.dir = random.randint(1, 8)
        if self.dir == 6:  # 오른쪽 아래
            self.x += 1 * RUN1_SPEED_PPS * game_framework.frame_time
            self.y += -1 * RUN1_SPEED_PPS * game_framework.frame_time
            if self.x >= 780 or self.y <= 40:
                self.dir = random.randint(1, 8)
        if self.dir == 7:  # 아래
            self.y += -1 * RUN1_SPEED_PPS * game_framework.frame_time
            if self.y <= 40:
                self.dir = random.randint(1, 8)
        if self.dir == 8:  # 왼쪽 아래
            self.x += -1 * RUN1_SPEED_PPS * game_framework.frame_time
            self.y += -1 * RUN1_SPEED_PPS * game_framework.frame_time
            if self.x <= 20 or self.y <= 40:
                self.dir = random.randint(1, 8)

    def draw(self):
        if self.dir == 1:  # 왼쪽
            self.image.clip_draw(int(self.frame)*128, 128*7, 128, 128, self.x, self.y)
        if self.dir == 2:  # 왼쪽 위
            self.image.clip_draw(int(self.frame)*128, 128*6, 128, 128, self.x, self.y)
        if self.dir == 3:  # 위
            self.image.clip_draw(int(self.frame)*128, 128*5, 128, 128, self.x, self.y)
        if self.dir == 4:  # 오른쪽 위
            self.image.clip_draw(int(self.frame)*128, 128*4, 128, 128, self.x, self.y)
        if self.dir == 5:  # 오른쪽
            self.image.clip_draw(int(self.frame)*128, 128*3, 128, 128, self.x, self.y)
        if self.dir == 6:  # 오른쪽 아래
            self.image.clip_draw(int(self.frame)*128, 128*2, 128, 128, self.x, self.y)
        if self.dir == 7:  # 아래
            self.image.clip_draw(int(self.frame)*128, 128*1, 128, 128, self.x, self.y)
        if self.dir == 8:  # 왼쪽 아래
            self.image.clip_draw(int(self.frame)*128, 128*0, 128, 128, self.x, self.y)
        # draw_rectangle(*self.get_bb())


    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y + 20

    def handle_collision(self, other, group):
        print('bullet meet mob1')
        if group == 'bullet:mobs':
            game_world.remove_object(self)



# 일반몹-2 클래스
class Mob2:
    image = None
    def __init__(self):
        if Mob2.image == None:
            Mob2.image = load_image('zombie_2.png')

        self.x, self.y = random.randint(50, 750), random.randint(50, 500)
        self.frame = random.randint(0, 11)
        self.die_frame = 28
        self.dir = random.randint(1, 8)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if self.dir == 1:  # 왼쪽
            self.x += -1 * RUN2_SPEED_PPS * game_framework.frame_time
            if self.x <= 20:
                self.dir = random.randint(1, 8)
        if self.dir == 2:  # 왼쪽 위
            self.x += -1 * RUN2_SPEED_PPS * game_framework.frame_time
            self.y += 1 * RUN2_SPEED_PPS * game_framework.frame_time
            if self.x <= 20 or self.y >= 500:
                self.dir = random.randint(1, 8)
        if self.dir == 3:  # 위
            self.y += 1 * RUN2_SPEED_PPS * game_framework.frame_time
            if self.y >= 500:
                self.dir = random.randint(1, 8)
        if self.dir == 4:  # 오른쪽 위
            self.x += 1 * RUN2_SPEED_PPS * game_framework.frame_time
            self.y += 1 * RUN2_SPEED_PPS * game_framework.frame_time
            if self.x >= 780 or self.y >= 500:
                self.dir = random.randint(1, 8)
        if self.dir == 5:  # 오른쪽
            self.x += 1 * RUN2_SPEED_PPS * game_framework.frame_time
            if self.x >= 780:
                self.dir = random.randint(1, 8)
        if self.dir == 6:  # 오른쪽 아래
            self.x += 1 * RUN2_SPEED_PPS * game_framework.frame_time
            self.y += -1 * RUN2_SPEED_PPS * game_framework.frame_time
            if self.x >= 780 or self.y <= 40:
                self.dir = random.randint(1, 8)
        if self.dir == 7:  # 아래
            self.y += -1 * RUN2_SPEED_PPS * game_framework.frame_time
            if self.y <= 40:
                self.dir = random.randint(1, 8)
        if self.dir == 8:  # 왼쪽 아래
            self.x += -1 * RUN2_SPEED_PPS * game_framework.frame_time
            self.y += -1 * RUN2_SPEED_PPS * game_framework.frame_time
            if self.x <= 20 or self.y <= 40:
                self.dir = random.randint(1, 8)

    def draw(self):
        if self.dir == 1:  # 왼쪽
            self.image.clip_draw(int(self.frame)*128, 128*7, 128, 128, self.x, self.y)
        if self.dir == 2:  # 왼쪽 위
            self.image.clip_draw(int(self.frame)*128, 128*6, 128, 128, self.x, self.y)
        if self.dir == 3:  # 위
            self.image.clip_draw(int(self.frame)*128, 128*5, 128, 128, self.x, self.y)
        if self.dir == 4:  # 오른쪽 위
            self.image.clip_draw(int(self.frame)*128, 128*4, 128, 128, self.x, self.y)
        if self.dir == 5:  # 오른쪽
            self.image.clip_draw(int(self.frame)*128, 128*3, 128, 128, self.x, self.y)
        if self.dir == 6:  # 오른쪽 아래
            self.image.clip_draw(int(self.frame)*128, 128*2, 128, 128, self.x, self.y)
        if self.dir == 7:  # 아래
            self.image.clip_draw(int(self.frame)*128, 128*1, 128, 128, self.x, self.y)
        if self.dir == 8:  # 왼쪽 아래
            self.image.clip_draw(int(self.frame)*128, 128*0, 128, 128, self.x, self.y)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y + 20

    def handle_collision(self, other, group):
        print('bullet meet mob2')
        if group == 'bullet:mobs':
            for die_frame in range(27, 36):
                if self.dir == 1:  # 왼쪽
                    self.image.clip_draw(int(self.die_frame) * 128, 128 * 7, 128, 128, self.x, self.y)
                if self.dir == 2:  # 왼쪽 위
                    self.image.clip_draw(int(self.die_frame) * 128, 128 * 6, 128, 128, self.x, self.y)
                if self.dir == 3:  # 위
                    self.image.clip_draw(int(self.die_frame) * 128, 128 * 5, 128, 128, self.x, self.y)
                if self.dir == 4:  # 오른쪽 위
                    self.image.clip_draw(int(self.die_frame) * 128, 128 * 4, 128, 128, self.x, self.y)
                if self.dir == 5:  # 오른쪽
                    self.image.clip_draw(int(self.die_frame) * 128, 128 * 3, 128, 128, self.x, self.y)
                if self.dir == 6:  # 오른쪽 아래
                    self.image.clip_draw(int(self.die_frame) * 128, 128 * 2, 128, 128, self.x, self.y)
                if self.dir == 7:  # 아래
                    self.image.clip_draw(int(self.die_frame) * 128, 128 * 1, 128, 128, self.x, self.y)
                if self.dir == 8:  # 왼쪽 아래
                    self.image.clip_draw(int(self.die_frame) * 128, 128 * 0, 128, 128, self.x, self.y)
            game_world.remove_object(self)




