from pico2d import *
import random

# 일반몹-2 클래스
class Mob2:
    def __init__(self):
        self.x, self.y = random.randint(50, 750), random.randint(50, 500)
        self.die_x, self.die_y = 0, 0
        self.frame = random.randint(0, 11)
        self.die_frame = 28
        self.dir = random.randint(1, 8)
        self.image = load_image('zombie_2.png')
    def update(self):
        self.frame = (self.frame + 1) % 12
        if self.dir == 1:  # 왼쪽
            self.x -= 4
            if self.x <= 20:
                self.dir = random.randint(1, 8)
        if self.dir == 2:  # 왼쪽 위
            self.x -= 3
            self.y += 3
            if self.x <= 20 or self.y >= 550:
                self.dir = random.randint(1, 8)
        if self.dir == 3:  # 위
            self.y += 3
            if self.y >= 550:
                self.dir = random.randint(1, 8)
        if self.dir == 4:  # 오른쪽 위
            self.x += 3
            self.y += 3
            if self.x >= 780 or self.y >= 550:
                self.dir = random.randint(1, 8)
        if self.dir == 5:  # 오른쪽
            self.x += 4
            if self.x >= 780:
                self.dir = random.randint(1, 8)
        if self.dir == 6:  # 오른쪽 아래
            self.x += 3
            self.y -= 3
            if self.x >= 780 or self.y <= 40:
                self.dir = random.randint(1, 8)
        if self.dir == 7:  # 아래
            self.y -= 3
            if self.y <= 40:
                self.dir = random.randint(1, 8)
        if self.dir == 8:  # 왼쪽 아래
            self.x -= 3
            self.y -= 3
            if self.x <= 20 or self.y <= 40:
                self.dir = random.randint(1, 8)

    def draw(self):
        if self.dir == 1:  # 왼쪽
            self.image.clip_draw(self.frame*128, 128*7, 128, 128, self.x, self.y)
        if self.dir == 2:  # 왼쪽 위
            self.image.clip_draw(self.frame*128, 128*6, 128, 128, self.x, self.y)
        if self.dir == 3:  # 위
            self.image.clip_draw(self.frame*128, 128*5, 128, 128, self.x, self.y)
        if self.dir == 4:  # 오른쪽 위
            self.image.clip_draw(self.frame*128, 128*4, 128, 128, self.x, self.y)
        if self.dir == 5:  # 오른쪽
            self.image.clip_draw(self.frame*128, 128*3, 128, 128, self.x, self.y)
        if self.dir == 6:  # 오른쪽 아래
            self.image.clip_draw(self.frame*128, 128*2, 128, 128, self.x, self.y)
        if self.dir == 7:  # 아래
            self.image.clip_draw(self.frame*128, 128*1, 128, 128, self.x, self.y)
        if self.dir == 8:  # 왼쪽 아래
            self.image.clip_draw(self.frame*128, 128*0, 128, 128, self.x, self.y)

    def die(self):
        events = get_events()
        for event in events:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                self.die_x, self.die_y = self.x, self.y
                self.die_frame = (self.die_frame + 1) % 28
                self.image.clip_draw(self.die_frame * 128, 128 * 7, 128, 128, self.die_x, self.die_y)