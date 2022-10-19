from pico2d import *
import random
import game_framework

# 게임 필드 클래스 정의
class Field:
    def __init__(self):
        self.image = load_image('grass03.png')
    def draw(self):
        self.image.draw(400, 300)

class Wave1_UI:
    def __init__(self):
        self.image = load_image('Wave1_UI.png')
    def draw(self):
        self.image.draw(400, 580)

class Player:
    def __init__(self):
        self.x, self.y = 800, 100
        self.frame = 0
        self.image = load_image('Jog_left.png')
    def update(self):
        self.frame = (self.frame + 1) % 14
        self.x -= 10
    def draw_right(self):
        self.image.clip_draw(self.frame*129, 0, 129, 128, self.x, self.y)


# 일반몹-1 클래스 정의
class Mob1:
    def __init__(self):
        self.x, self.y = random.randint(50, 750), random.randint(50, 500)
        self.frame = random.randint(0, 11)
        self.dir = random.randint(1, 8)
        self.image = load_image('zombie_1.png')
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

# 키 이벤트
def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

WinW = 800
WinH = 600
running = True
open_canvas(WinW, WinH)
field = Field()
player = Player()
mob1 = Mob1()
wave1_UI = Wave1_UI()
# Wave1(5)
Wave1 = [Mob1() for i in range(10)]

while running:
    handle_events()
    player.update()
    for mob1 in Wave1:
        mob1.update()

    clear_canvas()
    field.draw()
    wave1_UI.draw()
    # player.draw_right()
    for mob1 in Wave1:
        mob1.draw()
    update_canvas()

    delay(0.07)

close_canvas()