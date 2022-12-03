from pico2d import *
import game_world
import game_framework
import play_state
import server
from bullet import Bullet
from mob import Mob1, Mob2

bullet = None

#1 : 이벤트 테이블 정의
RIGHTKEY_DOWN, LEFTKEY_DOWN, UPKEY_DOWN, DOWNKEY_DOWN, RIGHTKEY_UP, LEFTKEY_UP, UPKEY_UP, DOWNKEY_UP, SPACE = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHTKEY_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFTKEY_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UPKEY_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWNKEY_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHTKEY_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFTKEY_UP,
    (SDL_KEYUP, SDLK_UP): UPKEY_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWNKEY_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
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
    def enter(player, event):
        print('ENTER IDLE')
        player.Xface_dir, player.Yface_dir = 0, 0

    @staticmethod
    def exit(player, event):
        print('EXIT IDLE')
        if SPACE == event:
            # self.fire_gun()
            player.fire_gun()

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 14

    @staticmethod
    def draw(player):
        if player.Xface_dir == 1:
            player.image.clip_draw(0, 0, 66, 60, player.x, player.y)
            if player.Yface_dir == 1:
                player.image.clip_draw(66*2, 0, 66, 60, player.x, player.y)
            elif player.Yface_dir == -1:
                player.image.clip_draw(66 * 14, 0, 66, 60, player.x, player.y)

        elif player.Xface_dir == -1:
            player.image.clip_draw(66 * 8, 0, 66, 60, player.x, player.y)
            if player.Yface_dir == 1:
                player.image.clip_draw(66 * 6, 0, 66, 60, player.x, player.y)
            elif player.Yface_dir == -1:
                player.image.clip_draw(66 * 10, 0, 66, 60, player.x, player.y)

        elif player.Yface_dir == 1:
            player.image.clip_draw(66*4, 0, 66, 60, player.x, player.y)
        elif player.Yface_dir == -1:
            player.image.clip_draw(66*12, 0, 66, 60, player.x, player.y)


class RUN:
    def enter(player, event):
        print('ENTER RUN')
        if event == RIGHTKEY_DOWN:
            player.x_velocity += RUN_SPEED_PPS
            player.Xface_dir += 1
        elif event == RIGHTKEY_UP:
            player.x_velocity -= RUN_SPEED_PPS
            player.Xface_dir -= 1
        if event == LEFTKEY_DOWN:
            player.x_velocity -= RUN_SPEED_PPS
            player.Xface_dir -= 1
        elif event == LEFTKEY_UP:
            player.x_velocity += RUN_SPEED_PPS
            player.Xface_dir += 1

        if event == UPKEY_DOWN:
            player.y_velocity += RUN_SPEED_PPS
            player.Yface_dir += 1
        elif event == UPKEY_UP:
            player.y_velocity -= RUN_SPEED_PPS
            player.Yface_dir -= 1
        if event == DOWNKEY_DOWN:
            player.y_velocity -= RUN_SPEED_PPS
            player.Yface_dir -= 1
        elif event == DOWNKEY_UP:
            player.y_velocity += RUN_SPEED_PPS
            player.Yface_dir += 1

    def exit(player, event):
        print('EXIT RUN')
        player.Xface_dir = player.Xface_dir
        player.Yface_dir = player.Yface_dir
        if SPACE == event:
            # self.fire_gun()
            player.fire_gun()

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        player.x += player.x_velocity * game_framework.frame_time
        player.y += player.y_velocity * game_framework.frame_time
        player.x = clamp(10, player.x, 780)
        player.y = clamp(20, player.y, 520)

    def draw(player):
        if player.x_velocity < 0 and player.Yface_dir == 0:
            player.l_image.clip_draw(int(player.frame)*62, 0, 58, 60, player.x, player.y)
            player.Xface_dir = -1
        elif player.x_velocity > 0 and player.Yface_dir == 0:
            player.r_image.clip_draw(int(player.frame)*62, 0, 60, 60, player.x, player.y)
        else:
            if player.y_velocity < 0 and player.Yface_dir == -1:
                if player.Xface_dir == -1:
                    player.ld_image.clip_draw(int(player.frame) * 54, 0, 54, 60, player.x, player.y)
                elif player.Xface_dir == 1:
                    player.rd_image.clip_draw(int(player.frame) * 44, 0, 44, 60, player.x, player.y)
                else:
                    player.d_image.clip_draw(int(player.frame) * 62, 0, 60, 60, player.x, player.y)

            elif player.y_velocity > 0 and player.Yface_dir == 1:
                if player.Xface_dir == -1:
                    player.lu_image.clip_draw(int(player.frame) * 49, 0, 49, 60, player.x, player.y)
                elif player.Xface_dir == 1:
                    player.ru_image.clip_draw(int(player.frame) * 37, 0, 37, 60, player.x, player.y)
                else:
                    player.u_image.clip_draw(int(player.frame) * 62, 0, 60, 60, player.x, player.y)

class FIRE:

    def enter(player, event):
        print('ENTER FIRE')
        player.frame = 0

        if event == RIGHTKEY_DOWN:
            player.Xface_dir += 1
        elif event == LEFTKEY_DOWN:
            player.Xface_dir -= 1
        elif event == RIGHTKEY_UP:
            player.Xface_dir -= 1
        elif event == LEFTKEY_UP:
            player.Xface_dir += 1
        elif event == UPKEY_DOWN:
            player.Yface_dir += 1
        elif event == DOWNKEY_DOWN:
            player.Yface_dir -= 1
        elif event == UPKEY_UP:
            player.Yface_dir -= 1
        elif event == DOWNKEY_UP:
            player.Yface_dir += 1

    def exit(player, event):
        if SPACE == event:
            player.fire_gun()

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        player.x += player.x_velocity * game_framework.frame_time
        player.y += player.y_velocity * game_framework.frame_time
        player.x = clamp(10, player.x, 780)
        player.y = clamp(20, player.y, 520)

    def draw(player):
        if player.Xface_dir == -1:
            player.l_fire_image.clip_draw(int(player.frame) * 59, 0, 59, 60, player.x, player.y)
        if player.Xface_dir == 1:
            player.r_fire_image.clip_draw(int(player.frame) * 59, 0, 59, 59, player.x, player.y)
        if player.Yface_dir == -1:
            player.d_fire_image.clip_draw(int(player.frame) * 37, 0, 37, 60, player.x, player.y)
        if player.Yface_dir == 1:
            player.u_fire_image.clip_draw(int(player.frame) * 32, 0, 32, 60, player.x, player.y)


# 3. 상태 변환 구현

next_state = {
    IDLE:  {RIGHTKEY_UP: RUN,  LEFTKEY_UP: RUN,  UPKEY_UP: RUN,  DOWNKEY_UP: RUN, RIGHTKEY_DOWN: RUN,  LEFTKEY_DOWN: RUN, UPKEY_DOWN: RUN, DOWNKEY_DOWN: RUN, SPACE: FIRE},
    RUN:   {RIGHTKEY_UP: IDLE, LEFTKEY_UP: IDLE, UPKEY_UP: IDLE, DOWNKEY_UP: IDLE, RIGHTKEY_DOWN: IDLE, LEFTKEY_DOWN: IDLE, UPKEY_DOWN: IDLE, DOWNKEY_DOWN: IDLE, SPACE: FIRE},
    FIRE: {RIGHTKEY_UP: IDLE,  LEFTKEY_UP: IDLE,  UPKEY_UP: IDLE,  DOWNKEY_UP: IDLE,  RIGHTKEY_DOWN: RUN,  LEFTKEY_DOWN: RUN, UPKEY_DOWN: RUN,  DOWNKEY_DOWN: RUN, SPACE: FIRE}
}


class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.X_dir, self.Y_dir, self.Xface_dir, self.Yface_dir = 0, 0, 0, -1
        self.x_velocity, self.y_velocity = 0, 0
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


