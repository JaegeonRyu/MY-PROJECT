from pico2d import *
import game_world
import game_framework
from bullet import Bullet

#1 : 이벤트 테이블 정의
RD, LD, UD, DD, RU, LU, UU, DU, SPACE, TIMER = range(10)
event_name = ['RD', 'LD', 'UD', 'DD', 'RU', 'LU', 'UU', 'DU', 'TIMER', 'SPACE']

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYDOWN, SDLK_UP): UD,
    (SDL_KEYDOWN, SDLK_DOWN): DD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYUP, SDLK_UP): UU,
    (SDL_KEYUP, SDLK_DOWN): DU
}

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

PIXEL_PER_METER = 10.0 / 0.3
RUN_SPEED_KPH = 25.0
RUN_SPEED_MPM = RUN_SPEED_KPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

# 2. : 상태 클래스 구현
class IDLE:
    @staticmethod
    def enter(self, event):
        print('ENTER IDLE')
        self.X_dir, self.Y_dir = 0, 0

    @staticmethod
    def exit(self, event):
        print('EXIT IDLE')
        if SPACE == event:
            self.fire_gun()

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 14
        self.timer -= 1
        if self.timer == 0:
            self.add_event(TIMER)

    @staticmethod
    def draw(self):
        if self.Xface_dir == 1:
            self.image.clip_draw(0, 0, 66, 60, self.x, self.y)
        elif self.Yface_dir == 1:
            self.image.clip_draw(66*4, 0, 66, 60, self.x, self.y)
        elif self.Xface_dir == -1:
            self.image.clip_draw(66*8, 0, 66, 60, self.x, self.y)
        elif self.Yface_dir == -1:
            self.image.clip_draw(66*12, 0, 66, 60, self.x, self.y)

class RUN:
    def enter(self, event):
        print('ENTER RUN')
        if event == RD:
            self.X_dir += 1
        elif event == LD:
            self.X_dir -= 1
        elif event == RU:
            self.X_dir -= 1
        elif event == LU:
            self.X_dir += 1
        elif event == UD:
            self.Y_dir += 1
        elif event == DD:
            self.Y_dir -= 1
        elif event == UU:
            self.Y_dir -= 1
        elif event == DU:
            self.Y_dir += 1

    def exit(self, event):
        print('EXIT RUN')
        self.Xface_dir = self.X_dir
        self.Yface_dir = self.Y_dir
        if SPACE == event:
            self.fire_gun()

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        self.x += self.X_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.Y_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(0, self.x, 800)
        self.y = clamp(0, self.y, 600)

    def draw(self):
        if self.X_dir == -1:
            self.l_image.clip_draw(int(self.frame)*62, 0, 58, 60, self.x, self.y)
        elif self.X_dir == 1:
            self.r_image.clip_draw(int(self.frame)*62, 0, 60, 60, self.x, self.y)
        elif self.Y_dir == -1:
            self.d_image.clip_draw(int(self.frame)*62, 0, 60, 60, self.x, self.y)
        elif self.Y_dir == 1:
            self.u_image.clip_draw(int(self.frame)*62, 0, 60, 60, self.x, self.y)

class FIRE:

    def enter(self, event):
        print('ENTER FIRE')
        self.frame = 0

        if event == RD:
            self.X_dir += 1
        elif event == LD:
            self.X_dir -= 1
        elif event == RU:
            self.X_dir -= 1
        elif event == LU:
            self.X_dir += 1
        elif event == UD:
            self.Y_dir += 1
        elif event == DD:
            self.Y_dir -= 1
        elif event == UU:
            self.Y_dir -= 1
        elif event == DU:
            self.Y_dir += 1

    def exit(self, event):
        # self.Xface_dir = self.X_dir
        # self.Yface_dir = self.Y_dir
        pass

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.x += self.X_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.Y_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(0, self.x, 800)
        self.y = clamp(0, self.y, 600)

    def draw(self):
        if self.Xface_dir == -1:
            self.l_fire_image.clip_draw(int(self.frame) * 59, 0, 59, 60, self.x, self.y)
        if self.Xface_dir == 1:
            self.r_fire_image.clip_draw(int(self.frame) * 59, 0, 59, 59, self.x, self.y)
        if self.Yface_dir == -1:
            self.d_fire_image.clip_draw(int(self.frame) * 37, 0, 37, 60, self.x, self.y)
        if self.Yface_dir == 1:
            self.u_fire_image.clip_draw(int(self.frame) * 32, 0, 32, 60, self.x, self.y)


# 3. 상태 변환 구현
next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  UU: RUN,  DU: RUN,  RD: RUN,  LD: RUN, UD: RUN,  DD: RUN, SPACE: FIRE},
    RUN:   {RU: IDLE, LU: IDLE, UU: IDLE, DU: IDLE, RD: IDLE, LD: IDLE, UD: IDLE, DD: IDLE, SPACE: FIRE},
    FIRE: {RU: IDLE,  LU: IDLE,  UU: IDLE,  DU: IDLE,  RD: RUN,  LD: RUN, UD: RUN,  DD: RUN, SPACE: FIRE}
}


class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.X_dir, self.Y_dir, self.Xface_dir, self.Yface_dir = 0, 0, 0, -1
        self.timer = 100

        self.image = load_image('walk_IDLE.png')
        self.r_image = load_image('Jog_right.png')
        self.l_image = load_image('Jog_left.png')
        self.u_image = load_image('Jog_up.png')
        self.d_image = load_image('Jog_down.png')
        self.r_fire_image = load_image('Fire_right.png')
        self.l_fire_image = load_image('Fire_left.png')
        self.u_fire_image = load_image('Fire_up.png')
        self.d_fire_image = load_image('Fire_down.png')

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]  # 예외처리
            except KeyError:
                print('ERROR: ', self.cur_state.__name__, '', event_name[event])

            self.cur_state.enter(self, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def draw(self):
        self.cur_state.draw(self)
        debug_print('PPPP')

    def add_event(self, event):
        self.event_que.insert(0, event)

    def fire_gun(self):
        print('fire ball')
        # 발사 지점에 총알 생성
        if self.Xface_dir == -1:
            bullet = Bullet(self.x, self.y, self.Xface_dir*2, 0)
        if self.Xface_dir == 1:
            bullet = Bullet(self.x, self.y, self.Xface_dir*2, 0)
        if self.Yface_dir == -1:
            bullet = Bullet(self.x, self.y, 0, self.Yface_dir*2)
        if self.Yface_dir == 1:
            bullet = Bullet(self.x, self.y, 0, self.Yface_dir*2)
        game_world.add_object(bullet, 1)
