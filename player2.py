from pico2d import *
import game_world
import game_framework
import play_state
import server
import gameover_state
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
class WalkingState:
    @staticmethod
    def enter(player, event):

        player.X_dir, player.Y_dir = 0, 0

        if event == RIGHTKEY_DOWN:
            player.x_velocity += RUN_SPEED_PPS
            player.X_dir += 1
        elif event == RIGHTKEY_UP:
            player.x_velocity -= RUN_SPEED_PPS
            player.X_dir -= 1
        if event == LEFTKEY_DOWN:
            player.x_velocity -= RUN_SPEED_PPS
            player.X_dir -= 1
        elif event == LEFTKEY_UP:
            player.x_velocity += RUN_SPEED_PPS
            player.X_dir += 1

        if event == UPKEY_DOWN:
            player.y_velocity += RUN_SPEED_PPS
            player.Y_dir += 1
        elif event == UPKEY_UP:
            player.y_velocity -= RUN_SPEED_PPS
            player.Y_dir -= 1
        if event == DOWNKEY_DOWN:
            player.y_velocity -= RUN_SPEED_PPS
            player.Y_dir -= 1
        elif event == DOWNKEY_UP:
            player.y_velocity += RUN_SPEED_PPS
            player.Y_dir += 1

    @staticmethod
    def exit(player, event):
        print('EXIT WalkingState')
        player.Xface_dir = player.X_dir
        player.Yface_dir = player.Y_dir
        if SPACE == event:
            player.fire_gun()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        player.x += player.x_velocity * game_framework.frame_time
        player.y += player.y_velocity * game_framework.frame_time
        player.x = clamp(10, player.x, 780)
        player.y = clamp(20, player.y, 520)

    @staticmethod
    def draw(player):
        if player.x_velocity < 0 and player.y_velocity == 0:
            player.l_image.clip_draw(int(player.frame) * 62, 0, 58, 60, player.x, player.y)
        elif player.x_velocity > 0 and player.y_velocity == 0:
            player.r_image.clip_draw(int(player.frame) * 62, 0, 60, 60, player.x, player.y)
        elif player.y_velocity < 0 and player.x_velocity == 0:
            player.d_image.clip_draw(int(player.frame) * 62, 0, 60, 60, player.x, player.y)
        elif player.y_velocity > 0 and player.x_velocity == 0:
            player.u_image.clip_draw(int(player.frame) * 62, 0, 60, 60, player.x, player.y)
        elif player.x_velocity < 0 and player.y_velocity < 0:
            player.ld_image.clip_draw(int(player.frame) * 54, 0, 54, 60, player.x, player.y)
            player.cross = 3
        elif player.x_velocity > 0 and player.y_velocity < 0:
            player.rd_image.clip_draw(int(player.frame) * 44, 0, 44, 60, player.x, player.y)
            player.cross = 4
        elif player.x_velocity < 0 and player.y_velocity > 0:
            player.lu_image.clip_draw(int(player.frame) * 49, 0, 49, 60, player.x, player.y)
            player.cross = 2
        elif player.x_velocity > 0 and player.y_velocity > 0:
            player.ru_image.clip_draw(int(player.frame) * 37, 0, 37, 60, player.x, player.y)
            player.cross = 1
        else:
            if player.Xface_dir == 1:
                player.image.clip_draw(0, 0, 66, 60, player.x, player.y)
            elif player.cross == 1:
                player.image.clip_draw(66 * 2, 0, 66, 60, player.x, player.y)
            elif player.Yface_dir == 1:
                player.image.clip_draw(66 * 4, 0, 66, 60, player.x, player.y)
            elif player.cross == 2:
                player.image.clip_draw(66 * 6, 0, 66, 60, player.x, player.y)
            elif player.Xface_dir == -1:
                player.image.clip_draw(66 * 8, 0, 66, 60, player.x, player.y)
            elif player.cross == 3:
                player.image.clip_draw(66 * 10, 0, 66, 60, player.x, player.y)
            elif player.Yface_dir == -1:
                player.image.clip_draw(66 * 12, 0, 66, 60, player.x, player.y)
            elif player.cross == 4:
                player.image.clip_draw(66 * 14, 0, 66, 60, player.x, player.y)


class FIRE:

    def enter(player, event):
        print('ENTER FIRE')
        player.frame = 0
        if event == RIGHTKEY_DOWN:
            player.x_velocity += RUN_SPEED_PPS
            player.X_dir += 1
        elif event == RIGHTKEY_UP:
            player.x_velocity -= RUN_SPEED_PPS
            player.X_dir -= 1
        if event == LEFTKEY_DOWN:
            player.x_velocity -= RUN_SPEED_PPS
            player.X_dir -= 1
        elif event == LEFTKEY_UP:
            player.x_velocity += RUN_SPEED_PPS
            player.X_dir += 1

        if event == UPKEY_DOWN:
            player.y_velocity += RUN_SPEED_PPS
            player.Y_dir += 1
        elif event == UPKEY_UP:
            player.y_velocity -= RUN_SPEED_PPS
            player.Y_dir -= 1
        if event == DOWNKEY_DOWN:
            player.y_velocity -= RUN_SPEED_PPS
            player.Y_dir -= 1
        elif event == DOWNKEY_UP:
            player.y_velocity += RUN_SPEED_PPS
            player.Y_dir += 1

    def exit(player, event):
        player.Xface_dir = player.X_dir
        player.Yface_dir = player.Y_dir
        if SPACE == event:
            player.fire_gun()

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        player.x += player.x_velocity * game_framework.frame_time
        player.y += player.y_velocity * game_framework.frame_time
        player.x = clamp(10, player.x, 780)
        player.y = clamp(20, player.y, 520)

    def draw(player):
        if player.Xface_dir == -1 and player.y_velocity == 0:
            player.l_fire_image.clip_draw(int(player.frame) * 59, 0, 59, 60, player.x, player.y)
        elif player.Xface_dir == 1 and player.y_velocity == 0:
            player.r_fire_image.clip_draw(int(player.frame) * 59, 0, 59, 59, player.x, player.y)
        elif player.Yface_dir == -1 and player.x_velocity == 0:
            player.d_fire_image.clip_draw(int(player.frame) * 37, 0, 37, 60, player.x, player.y)
        elif player.Yface_dir == 1 and player.x_velocity == 0:
            player.u_fire_image.clip_draw(int(player.frame) * 32, 0, 32, 60, player.x, player.y)
        elif player.x_velocity > 0 and player.y_velocity > 0:
            player.ru_fire_image.clip_draw(int(player.frame) * 49, 0, 49, 60, player.x, player.y)
        elif player.x_velocity > 0 and player.y_velocity < 0:
            player.rd_fire_image.clip_draw(int(player.frame) * 49, 0, 49, 60, player.x, player.y)
        elif player.x_velocity < 0 and player.y_velocity > 0:
            player.lu_fire_image.clip_draw(int(player.frame) * 49, 0, 49, 60, player.x, player.y)
        elif player.x_velocity < 0 and player.y_velocity < 0:
            player.ld_fire_image.clip_draw(int(player.frame) * 49, 0, 49, 60, player.x, player.y)


# 3. 상태 변환 구현

next_state = {
    WalkingState:  {RIGHTKEY_UP: WalkingState,  LEFTKEY_UP: WalkingState,  UPKEY_UP: WalkingState,  DOWNKEY_UP: WalkingState, RIGHTKEY_DOWN: WalkingState,  LEFTKEY_DOWN: WalkingState, UPKEY_DOWN: WalkingState, DOWNKEY_DOWN: WalkingState, SPACE: FIRE},
    FIRE: {RIGHTKEY_UP: WalkingState,  LEFTKEY_UP: WalkingState,  UPKEY_UP: WalkingState,  DOWNKEY_UP: WalkingState,  RIGHTKEY_DOWN: WalkingState,  LEFTKEY_DOWN: WalkingState, UPKEY_DOWN: WalkingState,  DOWNKEY_DOWN: WalkingState, SPACE: FIRE}
}


class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.X_dir, self.Y_dir, self.Xface_dir, self.Yface_dir = 0, 0, 0, -1
        self.x_velocity, self.y_velocity = 0, 0
        self.timer = 100
        self.HP = 1.0 * 100
        self.cross = 0
        self.font = load_font('resources\\ENCR10B.TTF', 16)

        self.image = load_image('resources\\walk_IDLE.png')
        self.r_image = load_image('resources\\Jog_right.png')
        self.l_image = load_image('resources\\Jog_left.png')
        self.u_image = load_image('resources\\Jog_up.png')
        self.d_image = load_image('resources\\Jog_down.png')
        self.ru_image = load_image('resources\\Jog_right_up.png')
        self.rd_image = load_image('resources\\Jog_right_down.png')
        self.lu_image = load_image('resources\\Jog_left_up.png')
        self.ld_image = load_image('resources\\Jog_left_down.png')

        self.r_fire_image = load_image('resources\\Fire_right.png')
        self.l_fire_image = load_image('resources\\Fire_left.png')
        self.u_fire_image = load_image('resources\\Fire_up.png')
        self.d_fire_image = load_image('resources\\Fire_down.png')
        self.ru_fire_image = load_image('resources\\Fire_right_up.png')
        self.rd_fire_image = load_image('resources\\Fire_right_down.png')
        self.lu_fire_image = load_image('resources\\Fire_left_up.png')
        self.ld_fire_image = load_image('resources\\Fire_left_down.png')

        self.event_que = []
        self.cur_state = WalkingState
        self.cur_state.enter(self, None)


    def update(self):
        self.cur_state.do(self)

        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state[self.cur_state][event]
            self.cur_state.enter(self, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        elif ((event.type, event.key), (event.type, event.key)) in key_event_table:
            key_event = key_event_table[((event.type, event.key), (event.type, event.key))]
            self.add_event(key_event)

    def draw(self):
        self.font.draw(self.x - 20, self.y + 50, 'HP: %d ' % (self.HP), (255, 0, 0))
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
        elif self.Xface_dir == 1:
            bullet = [Bullet(self.x, self.y, self.Xface_dir*2, 0)]
        elif self.Yface_dir == -1:
            bullet = [Bullet(self.x, self.y, 0, self.Yface_dir*2)]
        elif self.Yface_dir == 1:
            bullet = [Bullet(self.x, self.y, 0, self.Yface_dir*2)]
        elif self.cross == 1:
            bullet = [Bullet(self.x, self.y, self.Xface_dir*2, self.Yface_dir*2)]
        elif self.cross == 2:
            bullet = [Bullet(self.x, self.y, self.Xface_dir*2, self.Yface_dir*2)]
        elif self.cross == 3:
            bullet = [Bullet(self.x, self.y, self.Xface_dir*2, self.Yface_dir*2)]
        elif self.cross == 4:
            bullet = [Bullet(self.x, self.y, self.Xface_dir*2, self.Yface_dir*2)]

        game_world.add_objects(bullet, 1)
        game_world.add_collision_pairs(play_state.mobs, bullet, 'bullet:mobs')

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20, self.y + 30

    def get_attack_bb(self):
        return self.x, self.y - 25, self.x + 30, self.y + 25

    def handle_collision(self, other, group):
        pass

    def collision_zombie_player(self, other, group):
        if group == 'player:mobs':
            self.HP -= 0.1
            print(self.HP)
            if self.HP <= 0:
                game_world.remove_object(self)
                game_framework.change_state(gameover_state)


