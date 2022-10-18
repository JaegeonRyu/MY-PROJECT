from pico2d import *
import random

# 게임 필드 클래스 정의
class Field:
    def __init__(self):
        self.image = load_image('grass03.png')

    def draw(self):
        self.image.draw(400, 300)

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
        self.x, self.y = random.randint(50, 750), random.randint(50, 550)
        self.frame = random.randint(0, 11)
        self.image = load_image('zombie_0.png')
    def update(self):
        self.frame = (self.frame + 1) % 12
        self.x -= 4
    def draw_right(self):
        self.image.clip_draw(self.frame*128, 896, 128, 128, self.x, self.y)


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
# Wave1(5)
Wave1 = [Mob1() for i in range(5)]

while running:
    handle_events()
    player.update()
    for mob1 in Wave1:
        mob1.update()

    clear_canvas()
    field.draw()
    # player.draw_right()
    for mob1 in Wave1:
        mob1.draw_right()
    update_canvas()

    delay(0.05)

close_canvas()