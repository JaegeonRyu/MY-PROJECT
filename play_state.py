from pico2d import *

# 게임 필드 클래스 정의
class Field:
    def __init__(self):
        self.image = load_image('grass03.png')

    def draw(self):
        self.image.draw(400, 300)

class Player:
    def __init__(self):
        self.x, self.y = 100, 100
        self.frame = 0
        self.image = load_image('Jog_right.png')
    def update(self):
        self.frame = (self.frame + 1) % 14
        self.x += 5
    def draw_right(self):
        self.image.clip_draw(self.frame*97, 0, 100, 128, self.x, self.y)

# 일반몹-1 클래스 정의
class Mob1:
    def __init__(self):
        self.x, self.y = 580, 300
        self.frame = 0
        self.image = load_image('zombie_0.png')
    def update(self):
        self.frame = (self.frame + 1) % 12
        self.x -= 4
    def draw(self):
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

running = True
open_canvas()
field = Field()
player = Player()
mob1 = Mob1()

while running:
    handle_events()

    player.update()
    mob1.update()

    clear_canvas()
    field.draw()
    player.draw_right()
    mob1.draw()
    update_canvas()

    delay(0.1)

close_canvas()