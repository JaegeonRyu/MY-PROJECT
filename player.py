from pico2d import *
import game_world
import game_framework

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
        self.frame = (self.frame + 1) % 14
        self.x += self.X_dir
        self.y += self.Y_dir
        self.x = clamp(0, self.x, 800)
        self.y = clamp(0, self.y, 600)

    def draw(self):
        if self.X_dir == -1:
            self.l_image.clip_draw(self.frame*61, 0, 61, 60, self.x, self.y)
        elif self.X_dir == 1:
            self.r_image.clip_draw(self.frame*61, 0, 61, 60, self.x, self.y)
        elif self.Y_dir == -1:
            self.d_image.clip_draw(self.frame*61, 0, 61, 60, self.x, self.y)
        elif self.Y_dir == 1:
            self.u_image.clip_draw(self.frame*61, 0, 61, 60, self.x, self.y)


# 3. 상태 변환 구현
next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  UU: RUN,  DU: RUN,  RD: RUN,  LD: RUN, UD: RUN,  DD: RUN, SPACE: IDLE},
    RUN:   {RU: IDLE, LU: IDLE, UU: IDLE, DU: IDLE, RD: IDLE, LD: IDLE, UD: IDLE, DD: IDLE, SPACE: RUN}
}


class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.X_dir, self.Y_dir, self.Xface_dir, self.Yface_dir = 1, 0, 0, 0
        self.timer = 100

        self.image = load_image('walk_IDLE.png')
        self.r_image = load_image('Jog_right.png')
        self.l_image = load_image('Jog_left.png')
        self.u_image = load_image('Jog_up.png')
        self.d_image = load_image('Jog_down.png')

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.frame = (self.frame + 1) % 14

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
        #ball = Ball(self.x, self.y, self.face_dir*2)
        #game_world.add_object(ball, 1)
