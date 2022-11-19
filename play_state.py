from pico2d import *
import random
import game_world
import game_framework

from field_grass import Grass
from player import Player
from bullet import Bullet
from mob import Mob1, Mob2
from game_UI import UI, GUN

grass = None
player = None
bullet = None
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
    global grass, player, bullet, ui, gun
    grass = Grass()
    player = Player()
    ui = UI()
    gun = GUN()

    game_world.add_object(grass, 0)
    game_world.add_object(player, 1)
    # game_world.add_object(bullet, 1)
    game_world.add_object(ui, 1)
    game_world.add_object(gun, 2)

    global mobs
    mobs = [Mob1() for i in range(10)] + [Mob2() for i in range(10)]
    game_world.add_objects(mobs, 1)
    

    # game_world.add_collision_group(player, mobs, 'player:mobs')

def update():
    for game_object in game_world.all_objects():
        game_object.update()
    delay(0.01)

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('collision by ', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True

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


