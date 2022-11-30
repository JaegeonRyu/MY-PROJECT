from pico2d import *
import random
import game_framework
import game_world
import server
import math
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 12
FRAMES_PER_DEATH_ACTION = 8

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
    blood_image = None
    def __init__(self):
        if Mob1.image == None:
            Mob1.image = load_image('zombie_1.png')
        if Mob1.blood_image == None:
            Mob1.blood_image = load_image('blood_2.png')

        self.x, self.y = random.randint(50, 750), random.randint(50, 500)
        self.death_x, self.death_y = self.x, self.y
        self.frame = random.randint(0, 11)
        self.dir = random.random()*2*math.pi
        self.death_dir = self.dir
        self.build_behavior_tree()
        self.HP = 1.0
        self.state = 'live'
        self.death_frame = 28
        self.speed = RUN1_SPEED_PPS

    def update(self):
        self.bt.run()

        if self.state == 'live':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12

        elif self.state == 'dead':
            self.death_frame = (self.death_frame + FRAMES_PER_DEATH_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 36
            if self.death_frame >= 35:
                self.death_frame = 35

        # 왼쪽
        if -math.pi <= self.dir < -math.pi*7/8 or math.pi*7/8 < self.dir <= math.pi:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        # 왼쪽 위
        elif math.pi*5/8 < self.dir < math.pi*7/8:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # 위
        elif math.pi*3/8 < self.dir < math.pi*5/8:
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # 오른쪽 위
        elif math.pi*1/8 < self.dir < math.pi*3/8:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # 오른쪽
        elif 0.0 <= self.dir < math.pi*1/8 or -math.pi*1/8 < self.dir <= 0:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        # 오른쪽 아래
        elif -math.pi*3/8 < self.dir < -math.pi*1/8:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # 아래
        elif -math.pi*5/8 < self.dir < -math.pi*3/8:
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # 왼쪽 아래
        elif -math.pi*7/8 < self.dir < -math.pi*5/8:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, 750)
        self.y = clamp(50, self.y, 550)

    def draw(self):
        if self.state == 'live':
            # 왼쪽
            if -math.pi <= self.dir <= -math.pi*7/8 or math.pi*7/8 < self.dir <= math.pi:
                self.image.clip_draw(int(self.frame)*128, 128*7, 128, 128, self.x, self.y)
            # 왼쪽 위
            elif math.pi*5/8 < self.dir < math.pi*7/8:
                self.image.clip_draw(int(self.frame)*128, 128*6, 128, 128, self.x, self.y)
            # 위
            elif math.pi*3/8 < self.dir < math.pi*5/8:
                self.image.clip_draw(int(self.frame)*128, 128*5, 128, 128, self.x, self.y)
            # 오른쪽 위
            elif math.pi*1/8 < self.dir < math.pi*3/8:
                self.image.clip_draw(int(self.frame)*128, 128*4, 128, 128, self.x, self.y)
            # 오른쪽
            elif 0.0 <= self.dir < math.pi*1/8 or -math.pi*1/8 < self.dir <= 0:
                self.image.clip_draw(int(self.frame)*128, 128*3, 128, 128, self.x, self.y)
            # 오른쪽 아래
            elif -math.pi*3/8 < self.dir < -math.pi*1/8:
                self.image.clip_draw(int(self.frame)*128, 128*2, 128, 128, self.x, self.y)
            # 아래
            elif -math.pi*5/8 < self.dir < -math.pi*3/8:
                self.image.clip_draw(int(self.frame)*128, 128*1, 128, 128, self.x, self.y)
            # 왼쪽 아래
            elif -math.pi*7/8 < self.dir < -math.pi*5/8:
                self.image.clip_draw(int(self.frame)*128, 128*0, 128, 128, self.x, self.y)

        if self.state == 'dead':
            if -math.pi <= self.death_dir <= -math.pi * 7/8 or math.pi * 7/8 < self.death_dir <= math.pi:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 7, 128, 128, self.x, self.y)
            elif math.pi * 5/8 < self.death_dir < math.pi * 7/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 6, 128, 128, self.x, self.y)
            elif math.pi * 3/8 < self.death_dir < math.pi * 5/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 5, 128, 128, self.x, self.y)
            elif math.pi * 1/8 < self.death_dir < math.pi * 3/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 4, 128, 128, self.x, self.y)
            elif 0.0 <= self.death_dir < math.pi * 1/8 or -math.pi * 1/8 < self.death_dir <= 0:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 3, 128, 128, self.x, self.y)
            elif -math.pi * 3/8 < self.death_dir < -math.pi * 1/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 2, 128, 128, self.x, self.y)
            elif -math.pi * 5/8 < self.death_dir < -math.pi * 3/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 1, 128, 128, self.x, self.y)
            elif -math.pi * 7/8 < self.death_dir < -math.pi * 5/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 0, 128, 128, self.x, self.y)
        draw_rectangle(*self.get_bb())


    def find_player(self):
        # fill here
        distance = (server.player.x - self.x) ** 2 + (server.player.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 30) ** 2:
            return BehaviorTree.SUCCESS

    def move_to_player(self):
        # fill here
        self.dir = math.atan2(server.player.y - self.y, server.player.x - self.x)
        return BehaviorTree.SUCCESS  # 일단 소년 쪽으로 움직이기만 해도 성공으로 간주

    def build_behavior_tree(self):
        # fill here
        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)

        self.bt = BehaviorTree(chase_node)

    def get_bb(self):
        if self.state == 'live':
            return self.x - 10, self.y - 30, self.x + 10, self.y + 15
        else:
            return -10, -10, 0, 0

    def handle_collision(self, other, group):
        print('bullet meet mob1')
        if group == 'bullet:mobs':
            self.HP = self.HP - 0.4

            # 피격 시 넉백
            if server.player.Xface_dir < 0:
                self.x -= 20
                self.blood_image.draw(self.x, self.y)
            elif server.player.Xface_dir > 0:
                self.x += 20
            elif server.player.Yface_dir < 0:
                self.y -= 15
            elif server.player.Yface_dir > 0:
                self.y += 15

            # 체력이 0이하가 되면 사망
            if self.HP <= 0.0:
                self.state = 'dead'
                self.speed = 0
                self.death_dir = self.dir
                # self.x, self.y = 800, 600
                # game_world.remove_object(self)

        elif group == 'mobs:mobs':
            self.get_bb()
            pass



# 일반몹-2 클래스
class Mob2:
    image = None
    def __init__(self):
        if Mob2.image == None:
            Mob2.image = load_image('zombie_2.png')

        self.x, self.y = random.randint(50, 750), random.randint(50, 500)
        self.death_x, self.death_y = self.x, self.y
        self.frame = random.randint(0, 11)
        self.dir = random.random()*2*math.pi
        self.death_dir = self.dir
        self.build_behavior_tree()
        self.HP = 1.0
        self.state = 'live'
        self.death_frame = 28
        self.speed = RUN2_SPEED_PPS

    def update(self):
        self.bt.run()

        if self.state == 'live':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12

        elif self.state == 'dead':
            self.death_frame = (self.death_frame + FRAMES_PER_DEATH_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 36
            if self.death_frame >= 35:
                self.death_frame = 35

        # 왼쪽
        if -math.pi <= self.dir < -math.pi*7/8 or math.pi*7/8 < self.dir <= math.pi:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        # 왼쪽 위
        elif math.pi*5/8 < self.dir < math.pi*7/8:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # 위
        elif math.pi*3/8 < self.dir < math.pi*5/8:
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # 오른쪽 위
        elif math.pi*1/8 < self.dir < math.pi*3/8:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # 오른쪽
        elif 0.0 <= self.dir < math.pi*1/8 or -math.pi*1/8 < self.dir <= 0:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        # 오른쪽 아래
        elif -math.pi*3/8 < self.dir < -math.pi*1/8:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # 아래
        elif -math.pi*5/8 < self.dir < -math.pi*3/8:
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # 왼쪽 아래
        elif -math.pi*7/8 < self.dir < -math.pi*5/8:
            self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
            self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, 750)
        self.y = clamp(50, self.y, 550)

    def draw(self):
        if self.state == 'live':
            # 왼쪽
            if -math.pi <= self.dir <= -math.pi*7/8 or math.pi*7/8 < self.dir <= math.pi:
                self.image.clip_draw(int(self.frame)*128, 128*7, 128, 128, self.x, self.y)
            # 왼쪽 위
            elif math.pi*5/8 < self.dir < math.pi*7/8:
                self.image.clip_draw(int(self.frame)*128, 128*6, 128, 128, self.x, self.y)
            # 위
            elif math.pi*3/8 < self.dir < math.pi*5/8:
                self.image.clip_draw(int(self.frame)*128, 128*5, 128, 128, self.x, self.y)
            # 오른쪽 위
            elif math.pi*1/8 < self.dir < math.pi*3/8:
                self.image.clip_draw(int(self.frame)*128, 128*4, 128, 128, self.x, self.y)
            # 오른쪽
            elif 0.0 <= self.dir < math.pi*1/8 or -math.pi*1/8 < self.dir <= 0:
                self.image.clip_draw(int(self.frame)*128, 128*3, 128, 128, self.x, self.y)
            # 오른쪽 아래
            elif -math.pi*3/8 < self.dir < -math.pi*1/8:
                self.image.clip_draw(int(self.frame)*128, 128*2, 128, 128, self.x, self.y)
            # 아래
            elif -math.pi*5/8 < self.dir < -math.pi*3/8:
                self.image.clip_draw(int(self.frame)*128, 128*1, 128, 128, self.x, self.y)
            # 왼쪽 아래
            elif -math.pi*7/8 < self.dir < -math.pi*5/8:
                self.image.clip_draw(int(self.frame)*128, 128*0, 128, 128, self.x, self.y)

        if self.state == 'dead':
            if -math.pi <= self.death_dir <= -math.pi * 7/8 or math.pi * 7/8 < self.death_dir <= math.pi:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 7, 128, 128, self.x, self.y)
            elif math.pi * 5/8 < self.death_dir < math.pi * 7/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 6, 128, 128, self.x, self.y)
            elif math.pi * 3/8 < self.death_dir < math.pi * 5/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 5, 128, 128, self.x, self.y)
            elif math.pi * 1/8 < self.death_dir < math.pi * 3/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 4, 128, 128, self.x, self.y)
            elif 0.0 <= self.death_dir < math.pi * 1/8 or -math.pi * 1/8 < self.death_dir <= 0:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 3, 128, 128, self.x, self.y)
            elif -math.pi * 3/8 < self.death_dir < -math.pi * 1/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 2, 128, 128, self.x, self.y)
            elif -math.pi * 5/8 < self.death_dir < -math.pi * 3/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 1, 128, 128, self.x, self.y)
            elif -math.pi * 7/8 < self.death_dir < -math.pi * 5/8:
                self.image.clip_draw(int(self.death_frame) * 128, 128 * 0, 128, 128, self.x, self.y)
        draw_rectangle(*self.get_bb())


    def find_player(self):
        # fill here
        distance = (server.player.x - self.x) ** 2 + (server.player.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 30) ** 2:
            return BehaviorTree.SUCCESS

    def move_to_player(self):
        # fill here
        self.dir = math.atan2(server.player.y - self.y, server.player.x - self.x)
        return BehaviorTree.SUCCESS  # 일단 소년 쪽으로 움직이기만 해도 성공으로 간주

    def build_behavior_tree(self):
        # fill here
        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)

        self.bt = BehaviorTree(chase_node)

    def get_bb(self):
        if self.state == 'live':
            return self.x - 10, self.y - 30, self.x + 10, self.y + 15
        else:
            return -100, -100, 0, 0

    def handle_collision(self, other, group):
        print('bullet meet mob1')
        if group == 'bullet:mobs':
            self.HP = self.HP - 0.5

            # 피격 시 넉백
            if server.player.Xface_dir < 0:
                self.x -= 20
            elif server.player.Xface_dir > 0:
                self.x += 20
            elif server.player.Yface_dir < 0:
                self.y -= 15
            elif server.player.Yface_dir > 0:
                self.y += 15

            # 체력이 0이하가 되면 사망
            if self.HP <= 0.0:
                self.state = 'dead'
                self.speed = 0
                self.death_dir = self.dir
                # self.x, self.y = 800, 600
                # game_world.remove_object(self)

        elif group == 'mobs:mobs':
            self.get_bb()
            pass






