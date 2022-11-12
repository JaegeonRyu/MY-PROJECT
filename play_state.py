from pico2d import *
import random
import game_world
import game_framework

from field_grass import Grass
from player import Player
from mob import Mob1, Mob2

grass = None
player = None
mobs = []

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            player.handle_event(event)

def enter():
    global grass, player
    grass = Grass()
    player = Player()
    game_world.add_object(grass, 0)
    game_world.add_object(player, 1)

    global mobs
    mobs = [Mob1() for i in range(5)] + [Mob2() for i in range(5)]
    game_world.add_objects(mobs, 1)
def update():
    for game_object in game_world.all_objects():
        game_object.update()
    delay(0.01)

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

# 종료
def exit():
    game_world.clear()

def pause():
    pass

def resume():
    pass

def test_self():
    import play_state

    pico2d.open_canvas()
    game_framework.run(play_state)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()


