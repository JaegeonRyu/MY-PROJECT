from pico2d import *
import random
import game_world
import game_framework
import server

from field_grass import Grass
from bullet import Bullet
from player import Player
from mob import Mob1, Mob2, Mob3
from game_UI import UI, GUN
from blood import Blood

mob_count = 20
all_mob_count = mob_count * 3
grass = None
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
            server.player.handle_event(event)

def enter():
    global grass, player, bullet, ui, gun, mobs, blood

    ui = UI()
    gun = GUN()

    grass = Grass()
    game_world.add_object(grass, 0)

    server.player = Player()
    game_world.add_object(server.player, 2)

    game_world.add_object(ui, 1)
    game_world.add_object(gun, 2)

    mobs = [Mob1() for i in range(mob_count)] + [Mob2() for i in range(mob_count)] + [Mob3() for i in range(mob_count)]
    game_world.add_objects(mobs, 1)
    game_world.add_collision_pairs(server.player, mobs, 'player:mobs')
    # game_world.add_collision_pairs(mobs, zom, 'mobs:mobs')

def update():
    for game_object in game_world.all_objects():
        game_object.update()
    delay(0.01)

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b, group):
            # print('collide ', group)
            if group == 'bullet:mobs' or group == 'mobs:mobs':
                a.handle_collision(b, group)
                b.handle_collision(a, group)
            elif group == 'player:mobs':
                a.collision_zombie_player(b, group)
                b.collision_zombie_player(a, group)

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def collide(a, b, group):
    if group == 'bullet:mobs':
        la, ba, ra, ta = a.get_bb()
        lb, bb, rb, tb = b.get_bb()

    elif group == 'player:mobs':
        la, ba, ra, ta = a.get_bb()
        lb, bb, rb, tb = b.get_attack_bb()

    else:
        pass

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True

def collision_zombie(a, b):
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


