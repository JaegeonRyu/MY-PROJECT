from pico2d import *
import game_world
import game_framework
import play_state
from bullet import Bullet
from mob import Mob1, Mob2

bullet = None

#1 : 이벤트 테이블 정의
RD, LD, UD, DD, RUD, LUD, RDD, LDD, RU, LU, UU, DU, RUU, LUU, RDU, LDU, SPACE, TIMER = range(18)
event_name = ['RD', 'LD', 'UD', 'DD', 'RUD', 'LUD', 'RDD', 'LDD', 'RU', 'LU', 'UU', 'DU', 'RUU', 'LUU', 'RDU', 'LDU', 'TIMER', 'SPACE']

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYDOWN, SDLK_UP): UD,
    (SDL_KEYDOWN, SDLK_DOWN): DD,
    (SDL_KEYDOWN, SDLK_w): RUD,
    (SDL_KEYDOWN, SDLK_q): LUD,
    (SDL_KEYDOWN, SDLK_s): RDD,
    (SDL_KEYDOWN, SDLK_a): LDD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYUP, SDLK_UP): UU,
    (SDL_KEYUP, SDLK_DOWN): DU,
    (SDL_KEYUP, SDLK_w): RUU,
    (SDL_KEYUP, SDLK_q): LUU,
    (SDL_KEYUP, SDLK_s): RDU,
    (SDL_KEYUP, SDLK_a): LDU
}

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

PIXEL_PER_METER = 10.0 / 0.3
RUN_SPEED_KPH = 20.0
RUN_SPEED_MPM = RUN_SPEED_KPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER


# 2. : 상태 클래스 구현
class IDLE:
    @staticmethod
    def enter(self, event):
        print('ENTER IDLE')
        self.X_dir, self.Y_dir, self.U_dir, self.D_dir = 0, 0, 0, 0

    @staticmethod
    def exit(self, event):
        print('EXIT IDLE')
        if SPACE == event:
            # self.fire_gun()
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
        elif self.Uface_dir == 1:
            self.image.clip_draw(66*2, 0, 66, 60, self.x, self.y)
        elif self.Yface_dir == 1:
            self.image.clip_draw(66*4, 0, 66, 60, self.x, self.y)
        elif self.Uface_dir == -1:
            self.image.clip_draw(66*6, 0, 66, 60, self.x, self.y)
        elif self.Xface_dir == -1:
            self.image.clip_draw(66*8, 0, 66, 60, self.x, self.y)
        elif self.Dface_dir == -1:
            self.image.clip_draw(66*10, 0, 66, 60, self.x, self.y)
        elif self.Yface_dir == -1:
            self.image.clip_draw(66*12, 0, 66, 60, self.x, self.y)
        elif self.Dface_dir == 1:
            self.image.clip_draw(66*14, 0, 66, 60, self.x, self.y)


class RUN:
    def enter(self, event):
        print('ENTER RUN')
        if event == RD:
            self.X_dir += 1
        elif event == LD:
            self.X_dir -= 1
        elif event == UD:
            self.Y_dir += 1
        elif event == DD:
            self.Y_dir -= 1
        elif event == LUD:
            self.U_dir -= 1
        elif event == RUD:
            self.U_dir += 1
        elif event == LDD:
            self.D_dir -= 1
        elif event == RDD:
            self.D_dir += 1
        elif event == RU:
            self.X_dir -= 1
        elif event == LU:
            self.X_dir += 1
        elif event == UU:
            self.Y_dir -= 1
        elif event == DU:
            self.Y_dir += 1
        elif event == LDU:
            self.D_dir += 1
        elif event == RDU:
            self.D_dir -= 1
        elif event == LUU:
            self.U_dir += 1
        elif event == RUU:
            self.U_dir -= 1

    def exit(self, event):
        print('EXIT RUN')
        self.Xface_dir = self.X_dir
        self.Yface_dir = self.Y_dir
        self.Uface_dir = self.U_dir
        self.Dface_dir = self.D_dir
        if SPACE == event:
            # self.fire_gun()
            self.fire_gun()
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        if self.X_dir == 1 or self.X_dir == -1:
            self.x += self.X_dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.Y_dir == 1 or self.Y_dir == -1:
            self.y += self.Y_dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.U_dir == 1:
            self.x += self.U_dir * RUN_SPEED_PPS * game_framework.frame_time
            self.y += self.U_dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.U_dir == -1:
            self.x += self.U_dir * RUN_SPEED_PPS * game_framework.frame_time
            self.y += -self.U_dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.D_dir == 1:
            self.x += self.D_dir * RUN_SPEED_PPS * game_framework.frame_time
            self.y += -self.D_dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.D_dir == -1:
            self.x += self.D_dir * RUN_SPEED_PPS * game_framework.frame_time
            self.y += self.D_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(10, self.x, 780)
        self.y = clamp(20, self.y, 520)

    def draw(self):
        if self.X_dir == -1:
            self.l_image.clip_draw(int(self.frame)*62, 0, 58, 60, self.x, self.y)
        elif self.U_dir == -1:
            self.lu_image.clip_draw(int(self.frame) * 49, 0, 49, 60, self.x, self.y)
        elif self.Y_dir == 1:
            self.u_image.clip_draw(int(self.frame) * 62, 0, 60, 60, self.x, self.y)
        elif self.U_dir == 1:
            self.ru_image.clip_draw(int(self.frame) * 37, 0, 37, 60, self.x, self.y)
        elif self.X_dir == 1:
            self.r_image.clip_draw(int(self.frame)*62, 0, 60, 60, self.x, self.y)
        elif self.D_dir == 1:
            self.rd_image.clip_draw(int(self.frame) * 44, 0, 44, 60, self.x, self.y)
        elif self.Y_dir == -1:
            self.d_image.clip_draw(int(self.frame)*62, 0, 60, 60, self.x, self.y)
        elif self.D_dir == -1:
            self.ld_image.clip_draw(int(self.frame) * 54, 0, 54, 60, self.x, self.y)

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
        if SPACE == event:
            # self.fire_gun()
            self.fire_gun()

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.x += self.X_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.Y_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(10, self.x, 780)
        self.y = clamp(20, self.y, 520)

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
    IDLE:  {RU: RUN,  LU: RUN,  UU: RUN,  DU: RUN, RUU: RUN,  LUU: RUN,  RDU: RUN,  LDU: RUN,  RD: RUN,  LD: RUN, UD: RUN, DD: RUN, RUD: RUN,  LUD: RUN,  RDD: RUN,  LDD: RUN, SPACE: FIRE},
    RUN:   {RU: IDLE, LU: IDLE, UU: IDLE, DU: IDLE, RUU: IDLE,  LUU: IDLE,  RDU: IDLE,  LDU: IDLE, RD: IDLE, LD: IDLE, UD: IDLE, DD: IDLE, RUD: IDLE,  LUD: IDLE,  RDD: IDLE,  LDD: IDLE, SPACE: FIRE},
    FIRE: {RU: IDLE,  LU: IDLE,  UU: IDLE,  DU: IDLE,  RD: RUN,  LD: RUN, UD: RUN,  DD: RUN, SPACE: FIRE}
}


class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.X_dir, self.Y_dir, self.Xface_dir, self.Yface_dir = 0, 0, 0, -1
        self.U_dir, self.D_dir, self.Uface_dir, self.Dface_dir = 0, 0, 0, 0
        self.timer = 100

        self.image = load_image('walk_IDLE.png')
        self.r_image = load_image('Jog_right.png')
        self.l_image = load_image('Jog_left.png')
        self.u_image = load_image('Jog_up.png')
        self.d_image = load_image('Jog_down.png')

        self.ru_image = load_image('Jog_right_up.png')
        self.rd_image = load_image('Jog_right_down.png')
        self.lu_image = load_image('Jog_left_up.png')
        self.ld_image = load_image('Jog_left_down.png')

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
        elif ((event.type, event.key), (event.type, event.key)) in key_event_table:
            key_event = key_event_table[((event.type, event.key), (event.type, event.key))]
            self.add_event(key_event)

    def draw(self):
        self.cur_state.draw(self)
        debug_print('PPPP')
        # draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def fire_gun(self):
        print('fire bullet')
        # 발사 지점에 총알 생성
        if self.Xface_dir == -1:
            bullet = [Bullet(self.x, self.y, self.Xface_dir*2, 0)]
        if self.Xface_dir == 1:
            bullet = [Bullet(self.x, self.y, self.Xface_dir*2, 0)]
        if self.Yface_dir == -1:
            bullet = [Bullet(self.x, self.y, 0, self.Yface_dir*2)]
        if self.Yface_dir == 1:
            bullet = [Bullet(self.x, self.y, 0, self.Yface_dir*2)]
        game_world.add_objects(bullet, 1)
        game_world.add_collision_group(play_state.mobs, bullet, 'bullet:mobs')

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20, self.y + 30

    def handle_collision(self, other, group):
        pass


